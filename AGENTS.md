# 專案維護指引

## 收錄範圍

本 repo 收錄有重複需求、輸入清楚且結果可驗證的個人工作流程。一次性指令留在當次任務，專案專屬慣例寫在各專案的 `AGENTS.md`。共用 skill 應可在其他環境使用，避免依賴作者電腦的固定路徑、憑證或私密資訊。

新 skill 放在 `skills/<name>/`。試用中的 skill 可留在開發分支。確認適用時機及可觀察成果後，再收錄到 README。

## 維護 Skills

- 每個 skill 使用 `skills/<name>/SKILL.md` 作為入口。目錄名稱用小寫 kebab-case，與 frontmatter 的 `name` 一致。`description` 要說清楚適用時機，必要時指出容易誤觸發的需求。
- 在 `SKILL.md` 說明必要輸入、執行步驟、可觀察成果及重要限制。腳本、參考資料與素材放在 skill 目錄內，並保留改編來源及授權。
- 較完整的使用說明放在 `docs/<name>.md`，包含用途、輸入、自然語言範例與限制。依實際驗證結果更新說明。
- 新增、改名、移動或刪除正式 skill 時，同步更新 README 分類索引、安裝指令和使用說明。

## 觸發方式

預設允許 agent 自動選用。只有使用者明確要求改成手動觸發時，才在該 skill 的 `agents/openai.yaml` 設定下列 Codex 選項。其他 agent 的設定請查閱各自的官方文件。

```yaml
policy:
  allow_implicit_invocation: false
```

## 安裝與驗證

正式安裝使用 [README](README.md) 中各 skill 的 `npx skills add` 指令。

- 從 repo 根目錄執行 `npx skills add . --list`，核對 CLI 找到的 skills 與 README 的安裝指令。
- 修改 skill 後，用代表性需求確認觸發範圍、成果與資源連結。修改腳本後，在暫存環境驗證實際行為，並檢查是否可能覆蓋既有安裝或洩漏憑證。
