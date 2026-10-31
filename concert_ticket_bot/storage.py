"""監控清單的 JSON 存檔。"""

from __future__ import annotations

import asyncio
import json
import os
import secrets
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path

MAX_WATCHES_PER_GUILD = 20


@dataclass
class Watch:
    id: str
    guild_id: int
    channel_id: int
    creator_id: int
    name: str
    url: str
    interval: int
    keywords: list[str]
    soldout_keywords: list[str]
    selector: str | None = None
    notify_on_change: bool = False
    mention_role_id: int | None = None
    dm_creator: bool = False
    paused: bool = False
    # 執行狀態
    last_state: dict | None = None
    last_checked: float = 0.0
    next_check: float = 0.0
    fail_count: int = 0
    last_error: str | None = None
    alert_count: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "Watch":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class Store:
    path: Path
    watches: dict[str, Watch] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)

    @classmethod
    def load(cls, path: str | os.PathLike) -> "Store":
        p = Path(path)
        store = cls(path=p)
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            store.watches = {w["id"]: Watch.from_dict(w) for w in raw.get("watches", [])}
        return store

    async def save(self) -> None:
        async with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            data = {"watches": [asdict(w) for w in self.watches.values()]}
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(tmp, self.path)

    def for_guild(self, guild_id: int) -> list[Watch]:
        return [w for w in self.watches.values() if w.guild_id == guild_id]

    def new_id(self) -> str:
        while True:
            wid = secrets.token_hex(3)
            if wid not in self.watches:
                return wid
