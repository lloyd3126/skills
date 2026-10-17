# Lloyd's Skills

將實際使用的工作流程整理成小而可組合、可版本控制的 agent skills。

目前是專案骨架，尚無正式或實驗中的 skills，也尚未發佈或驗證 plugin 安裝。

## 專案結構

```text
.agents/                  維護指引與架構決策
.changeset/               版本變更記錄
.claude-plugin/           Plugin 與 marketplace 設定
.github/                  Issue 範本與檢查流程
.out-of-scope/            已確認不收錄的提案
skills/
  engineering/            正式開發 skills
  productivity/           正式工作流程 skills
  in-progress/            實驗中的 skills
  misc/                   未推廣的 skills
  deprecated/             停用的 skills
docs/
  engineering/            正式開發 skills 使用說明
  productivity/           正式工作流程 skills 使用說明
  agents/                 Agent 整合說明
scripts/                  列表、本機連結與版本工具
AGENTS.md                 專案維護規則
CLAUDE.md                 指向 AGENTS.md 的相容入口
```

## 開始維護

閱讀 [AGENTS.md](AGENTS.md) 與 [收錄範圍](SCOPE.md)。先從一個常用工作流程開始，在 `skills/in-progress/<name>/SKILL.md` 定義觸發需求、輸入、步驟及驗證結果；實際使用驗證後再移入正式分類。

```sh
npm run check
bash scripts/list-skills.sh
```

以上命令不需要安裝依賴。需要管理版本時執行 `npm ci`、`npm run changeset`，並以 `npm run version` 同步 package 與 plugin 版本。

## 正式 skills

### Engineering

尚無正式 skills。見 [分類目錄](skills/engineering/README.md)。

### Productivity

尚無正式 skills。見 [分類目錄](skills/productivity/README.md)。

## 本機連結

`bash scripts/link-skills.sh` 預覽正式 skills 的連結，`--apply` 才會寫入 `~/.agents/skills`；遇到同名項目時停止。這與參考專案的覆蓋式連結行為不同。完整說明見 [.agents/install-block.md](.agents/install-block.md)。

## 來源

目錄分類與發佈骨架參考 [mattpocock/skills](https://github.com/mattpocock/skills)，快照 commit：`49dd158d1076134a641b33efb035946536778336`。保留原作者 MIT 授權，來源與改編範圍見 [NOTICE.md](NOTICE.md)。本專案的 skill 內容待建立。
