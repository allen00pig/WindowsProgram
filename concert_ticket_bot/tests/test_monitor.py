import asyncio
import sys
from pathlib import Path

import pytest
from aiohttp import web

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import monitor  # noqa: E402
from monitor import (  # noqa: E402
    DEFAULT_KEYWORDS, DEFAULT_SOLDOUT_KEYWORDS, FetchError, Fetcher,
    analyze, backoff_seconds, decide_alerts, extract_text, normalize_url,
)

SOLD_OUT = "<html><body><script>var x='立即購買'</script><div class='t'>全區 已售完</div></body></html>"
RELEASED = "<html><body><div class='t'>A區 <button>立即購買</button></div></body></html>"


def state(html, selector=None):
    return analyze(extract_text(html, selector), DEFAULT_KEYWORDS, DEFAULT_SOLDOUT_KEYWORDS)


def test_script_text_ignored():
    assert "立即購買" not in extract_text(SOLD_OUT)
    assert state(SOLD_OUT).found_soldout == ["已售完", "售完"]


def test_first_check_is_baseline_only():
    assert decide_alerts(None, state(RELEASED), True) == []


def test_release_detected():
    reasons = decide_alerts(state(SOLD_OUT), state(RELEASED), False)
    assert any("立即購買" in r for r in reasons)
    assert any("消失" in r for r in reasons)


def test_no_alert_when_unchanged():
    assert decide_alerts(state(SOLD_OUT), state(SOLD_OUT), True) == []


def test_change_mode():
    a = state("<p>場次 1</p>")
    b = state("<p>場次 2</p>")
    assert decide_alerts(a, b, False) == []
    assert decide_alerts(a, b, True) == ["頁面內容有變動"]


def test_selector_and_case_insensitive():
    html = "<div class='x'>SOLD OUT</div><div class='y'>Buy now</div>"
    assert extract_text(html, ".x") == "SOLD OUT"
    assert extract_text(html, ".missing") == ""
    assert state(html, ".y").found_keywords == ["Buy Now"]


def test_normalize_url():
    assert normalize_url(" https://a.com/x ") == "https://a.com/x"
    with pytest.raises(ValueError):
        normalize_url("javascript:alert(1)")


def test_backoff():
    assert backoff_seconds(60, 1) == 60
    assert backoff_seconds(60, 3) == 240
    assert backoff_seconds(600, 10) == monitor.MAX_BACKOFF_SECONDS
    assert backoff_seconds(60, 1, retry_after=300) == 300


@pytest.fixture
def server(monkeypatch):
    monkeypatch.setattr(monitor, "PER_HOST_GAP_SECONDS", 0)
    page = {"html": SOLD_OUT}

    async def robots(_):
        return web.Response(text="User-agent: *\nDisallow: /private\n")

    async def event(_):
        return web.Response(text=page["html"], content_type="text/html", charset="utf-8")

    async def busy(_):
        return web.Response(status=429, headers={"Retry-After": "120"})

    app = web.Application()
    app.router.add_get("/robots.txt", robots)
    app.router.add_get("/event", event)
    app.router.add_get("/private", event)
    app.router.add_get("/busy", busy)
    return app, page


def test_fetch_flow(server):
    app, page = server

    async def run():
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]
        base = f"http://127.0.0.1:{port}"
        f = Fetcher()
        try:
            s1 = state(await f.fetch(base + "/event"))
            page["html"] = RELEASED
            s2 = state(await f.fetch(base + "/event"))
            assert decide_alerts(s1, s2, False)

            with pytest.raises(FetchError) as e:
                await f.fetch(base + "/private")
            assert e.value.permanent

            with pytest.raises(FetchError) as e:
                await f.fetch(base + "/busy")
            assert e.value.retry_after == 120
        finally:
            await f.close()
            await runner.cleanup()

    asyncio.run(run())
