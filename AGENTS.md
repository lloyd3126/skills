# Repository guidance

## 專案與範圍

這是 `lloyd3126/skills`，用來維護可重用的個人 agent skills。以小而可組合的工作流程為單位；目前有實驗中的 skill，尚無正式 skill。
本檔放在 Git root，提供本專案規則；沿用使用者的全域偏好。只有子目錄確實需要不同規則時才新增巢狀指引。

## 結構與資料來源

- `skills/engineering/`：正式的程式開發 skills。
- `skills/productivity/`：正式的非程式工作流程 skills。
- `skills/in-progress/`：實驗中的 skills，不加入 plugin 清單。
- `skills/misc/`：保留但未推廣的 skills；`skills/deprecated/`：停用的 skills。
- `docs/<bucket>/<name>.md`：正式 skills 的使用說明；`.agents/`：維護指引與 ADR。
- `.claude-plugin/plugin.json`：正式 skills 的完整發佈清單；`.claude-plugin/marketplace.json`：本 repo 的 marketplace 識別。
- `package.json` 是版本的唯一來源；不要個別修改 plugin 版本。

## 新增與修改 skill

- 每個 skill 使用 `skills/<bucket>/<name>/SKILL.md`，名稱採 lowercase kebab-case；frontmatter 必須包含 `name` 與明確的 `description`，名稱與目錄一致。
- 先說清楚適用需求、必要輸入、預期結果與實際限制，再編寫步驟。只加入會改變 agent 決策的內容。
- 可選資源按需求加入 `scripts/`、`references/`、`assets/` 或 `agents/openai.yaml`，避免預建無用途的空目錄。
- 預設可自動探索；只有使用者明確要求手動觸發時，才設定 `policy.allow_implicit_invocation: false`。細節見 [.agents/invocation.md](.agents/invocation.md)。
- 正式 skill 的新增、改名、移動或刪除，必須同步根目錄 README、分類 README、plugin 清單及對應 docs。非正式分類不加入 plugin 清單。
- 只讀取本次工作相關的維護指引。撰寫使用說明時讀 [.agents/writing-docs.md](.agents/writing-docs.md)，評估收錄範圍時讀 [SCOPE.md](SCOPE.md)。
- 改編外部內容須保留授權與來源。不要把本機絕對路徑、帳號憑證或未公開的專案資料寫入可分享的 skill。

## 開發與驗證

- 基本檢查不需要安裝依賴：`npm run check`。
- 列出 skills：`bash scripts/list-skills.sh`。清單包含實驗中的 skills，本機連結工具僅處理正式分類。
- 需要 Changesets 時才執行 `npm ci`；版本更新用 `npm run changeset` 及 `npm run version`，然後執行 `npm run check`。
- 修改 shell script 後執行 `bash -n <path>`，並以暫存輸入驗證實際行為；修改 Node script 後檢查語法與相關成功、失敗路徑。
- 修改 skill 後，以代表性需求檢查觸發範圍、執行結果及資源連結；有實際操作風險時在隔離環境驗證。
- `npm run check` 只驗證版本及 shell 語法，不代表 skill 行為或 plugin 安裝已驗證。回報實際通過與未執行的檢查。
- `scripts/link-skills.sh` 預設只預覽。只有工作包含本機安裝時才使用 `--apply`，且不得覆蓋既有同名項目。

## Code Review Rules

- 檢查 skill 的觸發描述是否過廣、步驟是否超出使用者需求，以及引用資源是否存在。以收窄描述或移除無關步驟修正。
- 檢查正式 skills、README、docs 與 plugin 清單是否一致；實驗或停用 skills 不可被誤發佈。
- 檢查 script 是否可能覆蓋既有 skills，或洩漏憑證。驗證實際行為，不用文字比對代替行為驗證。

## 維護依據

依 [OpenAI 官方 AGENTS.md 文件](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 維持簡短、專案專屬且可執行的規則。更新檔案後，新的 Codex session 才會重新建立自動載入的指引鏈；本檔不修改全域設定。
