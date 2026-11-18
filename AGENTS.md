# 專案維護指引

本 repo 收錄可重用的個人 agent skills，適用範圍見 [SCOPE.md](SCOPE.md)。

## 維護 Skills

- 每個 skill 放在 `skills/<name>/SKILL.md`。目錄名稱用小寫 kebab-case，並與 frontmatter 的 `name` 一致。`description` 要說清楚何時適用。
- 說明必要輸入、執行步驟、可觀察成果與重要限制。依需求在 skill 目錄加上腳本、參考資料或素材。保留改編來源與授權，避免在可分享內容中寫入本機絕對路徑、憑證或私密資料。
- 觸發方式見[設定指引](.agents/invocation.md)。較完整的使用說明依[撰寫指引](.agents/writing-docs.md)放在 `docs/<name>.md`。
- 新增、改名、移動或刪除已收錄的 skill 時，同步更新 README 的分類索引、相關使用說明與 `.claude-plugin/plugin.json`。

## 驗證與發布

- 執行 `npm run check` 驗證版本同步與 shell 語法，執行 `bash scripts/list-skills.sh` 核對收錄路徑。
- 修改 skill 後，用代表性需求檢查觸發範圍、成果與資源連結。修改腳本後，在暫存環境驗證實際行為。
- 本機連結工具預設只預覽。只有當次包含本機安裝時才用 `--apply`，操作方式見[安裝指引](.agents/install-block.md)。
- `package.json` 是版本來源。需要更新版本時執行 `npm ci`、`npm run changeset`、`npm run version`，再跑 `npm run check`。

## Code Review Rules

- 檢查 skill 是否會在無關需求誤觸發，並核對 README、使用說明與 plugin 路徑是否一致。
- 檢查腳本是否可能覆蓋既有安裝或洩漏憑證。
