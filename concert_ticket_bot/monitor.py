"""頁面抓取與釋票偵測。

這個模組只做「讀取公開頁面 + 判斷文字變化」，不會登入、不會送出表單、
不會加入購物車，也不會下單。
"""

from __future__ import annotations

import asyncio
import hashlib
import re
import time
from dataclasses import dataclass, field, asdict
from urllib import robotparser
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

USER_AGENT = "ConcertReleaseNotifier/1.0 (notify-only bot; never purchases tickets)"

# 合規相關的硬性限制
MIN_INTERVAL_SECONDS = 60          # 每個監控最短檢查間隔
MAX_BACKOFF_SECONDS = 3600         # 連續失敗時最長等待
PER_HOST_GAP_SECONDS = 10          # 同一網站兩次請求之間至少間隔
ROBOTS_CACHE_SECONDS = 6 * 3600
MAX_PAGE_BYTES = 3 * 1024 * 1024
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=20)

DEFAULT_KEYWORDS = ["立即購買", "立即訂購", "釋票", "加開", "可購買", "Buy Now", "Buy Tickets"]
DEFAULT_SOLDOUT_KEYWORDS = ["已售完", "售完", "完售", "Sold Out", "暫無票券", "選購一空"]


@dataclass
class PageState:
    found_keywords: list[str] = field(default_factory=list)
    found_soldout: list[str] = field(default_factory=list)
    digest: str = ""
    snippet: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict | None) -> "PageState | None":
        if not data:
            return None
        return cls(**{k: data.get(k, v) for k, v in asdict(cls()).items()})


class FetchError(Exception):
    def __init__(self, message: str, retry_after: float | None = None, permanent: bool = False):
        super().__init__(message)
        self.retry_after = retry_after
        self.permanent = permanent


def extract_text(html: str, selector: str | None = None) -> str:
    """取出頁面可見文字；有 selector 時只取該區塊。"""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()
    if selector:
        nodes = soup.select(selector)
        if not nodes:
            return ""
        text = " ".join(n.get_text(" ", strip=True) for n in nodes)
    else:
        text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def _find(text: str, words: list[str]) -> list[str]:
    lowered = text.lower()
    return [w for w in words if w and w.lower() in lowered]


def _snippet(text: str, word: str, radius: int = 40) -> str:
    idx = text.lower().find(word.lower())
    if idx < 0:
        return ""
    start, end = max(0, idx - radius), min(len(text), idx + len(word) + radius)
    return ("…" if start else "") + text[start:end] + ("…" if end < len(text) else "")


def analyze(text: str, keywords: list[str], soldout_keywords: list[str]) -> PageState:
    found = _find(text, keywords)
    soldout = _find(text, soldout_keywords)
    snippet = _snippet(text, found[0]) if found else text[:120]
    return PageState(
        found_keywords=found,
        found_soldout=soldout,
        digest=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        snippet=snippet,
    )


def decide_alerts(prev: PageState | None, cur: PageState, notify_on_change: bool) -> list[str]:
    """比較前後兩次狀態，回傳需要通知的原因。第一次檢查只建立基準，不通知。"""
    if prev is None:
        return []
    reasons: list[str] = []
    new_kw = [k for k in cur.found_keywords if k not in prev.found_keywords]
    if new_kw:
        reasons.append("出現關鍵字：" + "、".join(new_kw))
    if prev.found_soldout and not cur.found_soldout:
        reasons.append("「" + "、".join(prev.found_soldout) + "」字樣消失了，可能有票釋出")
    if notify_on_change and cur.digest != prev.digest and not reasons:
        reasons.append("頁面內容有變動")
    return reasons


def normalize_url(url: str) -> str:
    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("網址必須以 http:// 或 https:// 開頭")
    return url


class Fetcher:
    """有禮貌的抓取器：遵守 robots.txt、同網站限速、處理 429 Retry-After。"""

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None
        self._robots: dict[str, tuple[float, robotparser.RobotFileParser | None]] = {}
        self._host_last: dict[str, float] = {}
        self._host_locks: dict[str, asyncio.Lock] = {}

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=REQUEST_TIMEOUT,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8"},
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def _throttle(self, host: str) -> None:
        lock = self._host_locks.setdefault(host, asyncio.Lock())
        async with lock:
            wait = self._host_last.get(host, 0) + PER_HOST_GAP_SECONDS - time.monotonic()
            if wait > 0:
                await asyncio.sleep(wait)
            self._host_last[host] = time.monotonic()

    async def _robots_for(self, url: str) -> robotparser.RobotFileParser | None:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        cached = self._robots.get(origin)
        if cached and time.monotonic() - cached[0] < ROBOTS_CACHE_SECONDS:
            return cached[1]

        rp = robotparser.RobotFileParser()
        session = await self._get_session()
        await self._throttle(p.netloc)
        try:
            async with session.get(origin + "/robots.txt") as resp:
                if resp.status in (401, 403):
                    rp.disallow_all = True
                elif resp.status >= 500:
                    raise FetchError(f"robots.txt 暫時無法讀取（HTTP {resp.status}）")
                elif resp.status >= 400:
                    rp.allow_all = True
                else:
                    body = await resp.text(errors="replace")
                    rp.parse(body.splitlines())
        except aiohttp.ClientError as e:
            raise FetchError(f"無法讀取 robots.txt：{e}") from e
        self._robots[origin] = (time.monotonic(), rp)
        return rp

    async def allowed(self, url: str) -> bool:
        rp = await self._robots_for(url)
        return rp is None or rp.can_fetch(USER_AGENT, url)

    async def fetch(self, url: str) -> str:
        if not await self.allowed(url):
            raise FetchError("此網站的 robots.txt 不允許自動程式讀取這個頁面，已停止監控", permanent=True)

        session = await self._get_session()
        await self._throttle(urlparse(url).netloc)
        try:
            async with session.get(url, allow_redirects=True) as resp:
                if resp.status == 429:
                    retry = resp.headers.get("Retry-After", "")
                    raise FetchError("網站要求降低頻率（HTTP 429）",
                                     retry_after=float(retry) if retry.isdigit() else None)
                if resp.status in (401, 403):
                    raise FetchError(f"網站拒絕存取（HTTP {resp.status}），可能禁止自動程式")
                if resp.status >= 400:
                    raise FetchError(f"HTTP {resp.status}")
                raw = await resp.content.read(MAX_PAGE_BYTES)
                return raw.decode(resp.charset or "utf-8", errors="replace")
        except aiohttp.ClientError as e:
            raise FetchError(f"連線失敗：{e}") from e
        except asyncio.TimeoutError as e:
            raise FetchError("連線逾時") from e


def backoff_seconds(interval: int, fail_count: int, retry_after: float | None = None) -> float:
    delay = min(interval * (2 ** max(fail_count - 1, 0)), MAX_BACKOFF_SECONDS)
    if retry_after:
        delay = max(delay, min(retry_after, MAX_BACKOFF_SECONDS))
    return delay
