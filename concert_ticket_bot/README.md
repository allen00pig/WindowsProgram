# 🎫 演唱會釋票通知機器人（只通知、不搶票）

定期檢查你指定的**公開**售票頁面，一偵測到釋票跡象就在 Discord 發通知，
附上官方頁面連結，**由你自己手動購票**。

## 這個機器人「不會」做的事

- ❌ 不登入任何售票帳號、不保存帳密
- ❌ 不送出表單、不選位、不加入購物車、不下單、不破解驗證碼
- ❌ 不繞過網站的防機器人機制

它只做一件事：像一般瀏覽器一樣讀取公開頁面的文字，比對有沒有變化。

## 為了合規內建的限制

| 項目 | 說明 |
|------|------|
| 最短檢查間隔 | 每個監控最少 **1 分鐘** 檢查一次（預設 3 分鐘） |
| 同網站限速 | 對同一網站的兩次請求至少間隔 10 秒 |
| robots.txt | 每次檢查前會遵守網站的 robots.txt，網站不允許就自動停止 |
| 被限流時 | 收到 HTTP 429 會依照 `Retry-After` 等待，連續失敗會逐步放慢（最長 1 小時） |
| 身分標示 | User-Agent 清楚標示為「只通知、不購票」的機器人 |
| 數量上限 | 每個伺服器最多 20 個監控 |

> 提醒：台灣《文化創意產業發展法》第 10-1 條禁止以不正方式（含自動化程式）**購票**。
> 本機器人只發送通知、不參與購票流程。但各售票平台的服務條款不同，
> 有些明文禁止任何自動化存取，使用前請自行確認，並以官方規定為準（此說明非法律意見）。

## 偵測方式

每次檢查會取出頁面的可見文字（忽略 script/style），然後：

1. **出現釋票關鍵字** → 通知（預設：立即購買、立即訂購、釋票、加開、可購買、Buy Now、Buy Tickets）
2. **售完字樣消失** → 通知（預設：已售完、售完、完售、Sold Out、暫無票券、選購一空）
3. （選用）**任何文字變動** → 通知

第一次檢查只會記錄目前狀態當作比對基準，不會通知；之後只在「狀態改變」時通知一次，不會洗版。

## 安裝與啟動

需要 Python 3.10 以上。

```bash
cd concert_ticket_bot
pip install -r requirements.txt
cp .env.example .env      # Windows 用：copy .env.example .env
# 編輯 .env，填入 DISCORD_TOKEN
python bot.py
```

### 建立 Discord 機器人

1. 到 <https://discord.com/developers/applications> → **New Application**
2. 左側 **Bot** → **Reset Token**，把 Token 貼到 `.env` 的 `DISCORD_TOKEN`（不要公開！）
3. 左側 **OAuth2 → URL Generator**：
   - Scopes 勾 `bot`、`applications.commands`
   - Bot Permissions 勾 `Send Messages`、`Embed Links`、`View Channels`（要 @ 身分組再勾 `Mention Everyone`）
4. 用產生的網址把機器人邀請進你的伺服器

> 斜線指令全域同步可能要等一段時間才出現。測試時可在 `.env` 設定 `GUILD_ID=你的伺服器ID`，會立即生效。

## 指令

| 指令 | 說明 |
|------|------|
| `/watch add` | 新增監控（名稱、網址、間隔、關鍵字、通知頻道、@身分組、私訊…） |
| `/watch list` | 列出所有監控與目前狀態 |
| `/watch status` | 查看單一監控詳情與下次檢查時間 |
| `/watch test` | 發一則測試通知，確認通知設定正確 |
| `/watch pause` / `/watch resume` | 暫停 / 恢復 |
| `/watch remove` | 刪除監控（限建立者或有「管理伺服器」權限者） |

範例：

```
/watch add name:五月天 台北場 url:https://example.com/event/123 interval_minutes:2 mention_role:@搶票團
```

### 進階：只看頁面某一區

頁面上常有不相關的「售完」字樣（例如其他場次）。可以用 `selector` 指定 CSS 選擇器只看票區：
在瀏覽器對票區按右鍵 →「檢查」，找到外層元素的 class，例如 `.ticket-list`，填入 `selector:.ticket-list`。

## 已知限制

- 有些售票網站的票區是用 JavaScript 動態載入，直接讀 HTML 看不到票況；這種頁面可能偵測不到。
- 有些網站會擋所有自動程式（回 403），機器人會回報錯誤並放慢重試，不會嘗試繞過。
- 監控資料存在 `data/watches.json`，機器人重開後會接續監控。

## 測試

```bash
pip install pytest
python -m pytest tests
```
