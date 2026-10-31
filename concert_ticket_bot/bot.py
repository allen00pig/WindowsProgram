"""演唱會釋票通知機器人（只通知、不搶票）。

使用方式：
    1. pip install -r requirements.txt
    2. 複製 .env.example 為 .env，填入 DISCORD_TOKEN
    3. python bot.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import tasks

from monitor import (
    DEFAULT_KEYWORDS,
    DEFAULT_SOLDOUT_KEYWORDS,
    MIN_INTERVAL_SECONDS,
    FetchError,
    Fetcher,
    PageState,
    analyze,
    backoff_seconds,
    decide_alerts,
    extract_text,
    normalize_url,
)
from storage import MAX_WATCHES_PER_GUILD, Store, Watch

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

log = logging.getLogger("ticket-bot")
DATA_FILE = os.getenv("DATA_FILE", "data/watches.json")
MAX_CONCURRENT_CHECKS = 5
FAIL_NOTICE_AT = 5
DISCLAIMER = "本機器人只發送通知，不會代為登入或購票，請自行前往官方頁面購買。"


def split_words(raw: str | None, default: list[str]) -> list[str]:
    if raw is None or not raw.strip():
        return list(default)
    return [w.strip() for w in raw.replace("，", ",").split(",") if w.strip()]


def fmt_time(ts: float) -> str:
    return f"<t:{int(ts)}:R>" if ts else "尚未檢查"


class TicketBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.store = Store.load(DATA_FILE)
        self.fetcher = Fetcher()
        self.sem = asyncio.Semaphore(MAX_CONCURRENT_CHECKS)
        self.running: set[str] = set()

    async def setup_hook(self) -> None:
        self.tree.add_command(watch_group)
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
        self.scheduler.start()

    async def close(self) -> None:
        await self.fetcher.close()
        await super().close()

    async def on_ready(self) -> None:
        log.info("已登入：%s，目前監控 %d 個頁面", self.user, len(self.store.watches))

    # ---------- 檢查流程 ----------

    async def check_page(self, w: Watch) -> PageState:
        html = await self.fetcher.fetch(w.url)
        text = extract_text(html, w.selector)
        if w.selector and not text:
            raise FetchError(f"找不到 CSS 選擇器「{w.selector}」對應的內容")
        return analyze(text, w.keywords, w.soldout_keywords)

    async def run_watch(self, w: Watch) -> None:
        async with self.sem:
            now = time.time()
            try:
                state = await self.check_page(w)
            except FetchError as e:
                w.fail_count += 1
                w.last_error = str(e)
                w.last_checked = now
                w.next_check = now + backoff_seconds(w.interval, w.fail_count, e.retry_after)
                log.warning("[%s] 檢查失敗（第 %d 次）：%s", w.id, w.fail_count, e)
                if e.permanent:
                    w.paused = True
                    await self.notify_problem(w, f"已自動暫停：{e}")
                elif w.fail_count == FAIL_NOTICE_AT:
                    await self.notify_problem(w, f"連續 {w.fail_count} 次檢查失敗：{e}（會持續放慢頻率重試）")
            else:
                prev = PageState.from_dict(w.last_state)
                reasons = decide_alerts(prev, state, w.notify_on_change)
                w.last_state = state.to_dict()
                w.last_checked = now
                w.next_check = now + w.interval
                w.fail_count = 0
                w.last_error = None
                if reasons:
                    w.alert_count += 1
                    await self.send_alert(w, state, reasons)
            finally:
                self.running.discard(w.id)
                if w.id in self.store.watches:
                    await self.store.save()

    @tasks.loop(seconds=15)
    async def scheduler(self) -> None:
        now = time.time()
        for w in list(self.store.watches.values()):
            if w.paused or w.id in self.running or w.next_check > now:
                continue
            self.running.add(w.id)
            asyncio.create_task(self.run_watch(w))

    @scheduler.before_loop
    async def _wait_ready(self) -> None:
        await self.wait_until_ready()

    # ---------- 通知 ----------

    async def _channel(self, channel_id: int):
        ch = self.get_channel(channel_id)
        if ch is None:
            try:
                ch = await self.fetch_channel(channel_id)
            except discord.HTTPException:
                return None
        return ch

    async def send_alert(self, w: Watch, state: PageState, reasons: list[str], test: bool = False) -> None:
        title = ("🧪 測試通知：" if test else "🎫 可能有票券釋出：") + w.name
        embed = discord.Embed(title=title, url=w.url, color=0x2ECC71,
                              timestamp=datetime.now(timezone.utc))
        embed.add_field(name="偵測原因", value="\n".join(f"• {r}" for r in reasons)[:1024], inline=False)
        if state.snippet:
            embed.add_field(name="頁面片段", value=state.snippet[:1024], inline=False)
        embed.set_footer(text=f"監控 ID：{w.id}｜{DISCLAIMER}")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="前往官方頁面", url=w.url, style=discord.ButtonStyle.link))

        content = f"<@&{w.mention_role_id}>" if w.mention_role_id else None
        allowed = discord.AllowedMentions(roles=True, users=False, everyone=False)
        ch = await self._channel(w.channel_id)
        if ch is not None:
            try:
                await ch.send(content=content, embed=embed, view=view, allowed_mentions=allowed)
            except discord.HTTPException as e:
                log.error("[%s] 無法在頻道發送通知：%s", w.id, e)
        if w.dm_creator:
            try:
                user = self.get_user(w.creator_id) or await self.fetch_user(w.creator_id)
                await user.send(embed=embed, view=view)
            except discord.HTTPException as e:
                log.warning("[%s] 無法私訊建立者：%s", w.id, e)

    async def notify_problem(self, w: Watch, message: str) -> None:
        ch = await self._channel(w.channel_id)
        if ch is not None:
            try:
                await ch.send(f"⚠️ 監控「{w.name}」（`{w.id}`）：{message}")
            except discord.HTTPException:
                pass


bot = TicketBot()
watch_group = app_commands.Group(name="watch", description="演唱會釋票監控（只通知，不代購）",
                                 guild_only=True)


def can_manage(inter: discord.Interaction, w: Watch) -> bool:
    perms = getattr(inter.user, "guild_permissions", None)
    return w.creator_id == inter.user.id or bool(perms and perms.manage_guild)


def get_watch(inter: discord.Interaction, watch_id: str) -> Watch | None:
    w = bot.store.watches.get(watch_id.strip())
    return w if w and w.guild_id == inter.guild_id else None


async def watch_id_autocomplete(inter: discord.Interaction, current: str):
    items = bot.store.for_guild(inter.guild_id)
    return [
        app_commands.Choice(name=f"{w.id}｜{w.name}"[:100], value=w.id)
        for w in items
        if current.lower() in (w.id + w.name).lower()
    ][:25]


def describe(w: Watch) -> str:
    state = PageState.from_dict(w.last_state)
    status = "⏸️ 暫停中" if w.paused else "▶️ 監控中"
    lines = [
        f"{status}｜每 {w.interval // 60} 分鐘｜通知頻道 <#{w.channel_id}>",
        f"網址：{w.url}",
        f"釋票關鍵字：{'、'.join(w.keywords) or '（無）'}",
        f"售完關鍵字：{'、'.join(w.soldout_keywords) or '（無）'}",
    ]
    if w.selector:
        lines.append(f"CSS 範圍：`{w.selector}`")
    if state:
        lines.append(f"目前偵測到：釋票字樣 {'、'.join(state.found_keywords) or '無'}；"
                     f"售完字樣 {'、'.join(state.found_soldout) or '無'}")
    lines.append(f"上次檢查：{fmt_time(w.last_checked)}｜已通知 {w.alert_count} 次")
    if w.last_error:
        lines.append(f"最近錯誤：{w.last_error}")
    return "\n".join(lines)


@watch_group.command(name="add", description="新增一個要監控的售票頁面")
@app_commands.describe(
    name="顯示名稱，例如：五月天 台北場",
    url="售票頁面網址（公開頁面，不需登入）",
    interval_minutes="多久檢查一次（分鐘，最少 1）",
    keywords="出現就通知的字，逗號分隔（留空用預設：立即購買、釋票…）",
    soldout_keywords="消失就通知的字，逗號分隔（留空用預設：已售完、Sold Out…）",
    selector="（進階）只看頁面某區塊的 CSS 選擇器，例如 .ticket-list",
    notify_on_change="頁面任何文字變動也通知（容易誤報，建議搭配 selector）",
    mention_role="通知時要 @ 的身分組",
    channel="通知要發到哪個頻道（預設目前頻道）",
    dm_me="同時私訊通知我",
)
async def watch_add(
    inter: discord.Interaction,
    name: app_commands.Range[str, 1, 80],
    url: str,
    interval_minutes: app_commands.Range[int, 1, 1440] = 3,
    keywords: str | None = None,
    soldout_keywords: str | None = None,
    selector: str | None = None,
    notify_on_change: bool = False,
    mention_role: discord.Role | None = None,
    channel: discord.TextChannel | None = None,
    dm_me: bool = False,
):
    if len(bot.store.for_guild(inter.guild_id)) >= MAX_WATCHES_PER_GUILD:
        await inter.response.send_message(f"每個伺服器最多 {MAX_WATCHES_PER_GUILD} 個監控，請先刪除不需要的。",
                                          ephemeral=True)
        return
    try:
        url = normalize_url(url)
    except ValueError as e:
        await inter.response.send_message(str(e), ephemeral=True)
        return

    await inter.response.defer(thinking=True)
    w = Watch(
        id=bot.store.new_id(),
        guild_id=inter.guild_id,
        channel_id=(channel or inter.channel).id,
        creator_id=inter.user.id,
        name=name,
        url=url,
        interval=max(interval_minutes * 60, MIN_INTERVAL_SECONDS),
        keywords=split_words(keywords, DEFAULT_KEYWORDS),
        soldout_keywords=split_words(soldout_keywords, DEFAULT_SOLDOUT_KEYWORDS),
        selector=(selector or "").strip() or None,
        notify_on_change=notify_on_change,
        mention_role_id=mention_role.id if mention_role else None,
        dm_creator=dm_me,
    )

    # 先檢查一次：確認網站允許、建立比對基準
    try:
        state = await bot.check_page(w)
    except FetchError as e:
        await inter.followup.send(f"❌ 無法新增：{e}")
        return
    now = time.time()
    w.last_state, w.last_checked, w.next_check = state.to_dict(), now, now + w.interval
    bot.store.watches[w.id] = w
    await bot.store.save()

    embed = discord.Embed(title=f"✅ 已開始監控：{w.name}", description=describe(w), color=0x3498DB)
    embed.set_footer(text=f"監控 ID：{w.id}｜{DISCLAIMER}")
    await inter.followup.send(embed=embed)


@watch_group.command(name="list", description="列出這個伺服器的所有監控")
async def watch_list(inter: discord.Interaction):
    items = bot.store.for_guild(inter.guild_id)
    if not items:
        await inter.response.send_message("目前沒有任何監控，用 `/watch add` 新增一個吧。", ephemeral=True)
        return
    embed = discord.Embed(title=f"🎫 監控清單（{len(items)}）", color=0x3498DB)
    for w in items[:25]:
        embed.add_field(name=f"{w.name}（{w.id}）", value=describe(w)[:1024], inline=False)
    embed.set_footer(text=DISCLAIMER)
    await inter.response.send_message(embed=embed, ephemeral=True)


@watch_group.command(name="remove", description="刪除一個監控")
@app_commands.autocomplete(watch_id=watch_id_autocomplete)
async def watch_remove(inter: discord.Interaction, watch_id: str):
    w = get_watch(inter, watch_id)
    if not w:
        await inter.response.send_message("找不到這個監控 ID。", ephemeral=True)
        return
    if not can_manage(inter, w):
        await inter.response.send_message("只有建立者或有「管理伺服器」權限的人可以刪除。", ephemeral=True)
        return
    del bot.store.watches[w.id]
    await bot.store.save()
    await inter.response.send_message(f"🗑️ 已刪除監控「{w.name}」。")


async def _set_paused(inter: discord.Interaction, watch_id: str, paused: bool):
    w = get_watch(inter, watch_id)
    if not w:
        await inter.response.send_message("找不到這個監控 ID。", ephemeral=True)
        return
    if not can_manage(inter, w):
        await inter.response.send_message("只有建立者或有「管理伺服器」權限的人可以變更。", ephemeral=True)
        return
    w.paused = paused
    if not paused:
        w.fail_count, w.last_error, w.next_check = 0, None, time.time()
    await bot.store.save()
    await inter.response.send_message(f"{'⏸️ 已暫停' if paused else '▶️ 已恢復'}監控「{w.name}」。")


@watch_group.command(name="pause", description="暫停一個監控")
@app_commands.autocomplete(watch_id=watch_id_autocomplete)
async def watch_pause(inter: discord.Interaction, watch_id: str):
    await _set_paused(inter, watch_id, True)


@watch_group.command(name="resume", description="恢復一個監控")
@app_commands.autocomplete(watch_id=watch_id_autocomplete)
async def watch_resume(inter: discord.Interaction, watch_id: str):
    await _set_paused(inter, watch_id, False)


@watch_group.command(name="status", description="查看單一監控的目前狀態")
@app_commands.autocomplete(watch_id=watch_id_autocomplete)
async def watch_status(inter: discord.Interaction, watch_id: str):
    w = get_watch(inter, watch_id)
    if not w:
        await inter.response.send_message("找不到這個監控 ID。", ephemeral=True)
        return
    embed = discord.Embed(title=f"{w.name}（{w.id}）", url=w.url, description=describe(w), color=0x3498DB)
    if not w.paused:
        embed.add_field(name="下次檢查", value=fmt_time(w.next_check))
    await inter.response.send_message(embed=embed, ephemeral=True)


@watch_group.command(name="test", description="發一則測試通知，確認頻道、身分組、私訊設定正確")
@app_commands.autocomplete(watch_id=watch_id_autocomplete)
async def watch_test(inter: discord.Interaction, watch_id: str):
    w = get_watch(inter, watch_id)
    if not w:
        await inter.response.send_message("找不到這個監控 ID。", ephemeral=True)
        return
    state = PageState.from_dict(w.last_state) or PageState()
    await bot.send_alert(w, state, ["這是測試通知，頁面沒有實際變動"], test=True)
    await inter.response.send_message("已送出測試通知。", ephemeral=True)


@bot.tree.error
async def on_app_command_error(inter: discord.Interaction, error: app_commands.AppCommandError):
    log.exception("指令錯誤", exc_info=error)
    msg = "執行指令時發生錯誤，請稍後再試。"
    if inter.response.is_done():
        await inter.followup.send(msg, ephemeral=True)
    else:
        await inter.response.send_message(msg, ephemeral=True)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("請先在 .env 設定 DISCORD_TOKEN（可參考 .env.example）")
    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
