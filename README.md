# Lloyd's Skills

收錄從實際工作整理出的可重用 Agent Skills，讓 Codex、Claude Code 等工具依循同一套工作流程。

## 分類

### 工作流程

- [plan-sdgs-exhibition](skills/plan-sdgs-exhibition/SKILL.md) 協助分階段規劃 SDGs 數位展覽，從策展主張做到可試作的原型企劃。詳見[使用說明](docs/plan-sdgs-exhibition.md)。

### 文件處理

- [pdf-margin-review](skills/pdf-margin-review/SKILL.md) 在 PDF 副本標亮原句，並把短評排成右側卡片。詳見[使用說明](docs/pdf-margin-review.md)。

## 用 skills.sh 安裝

在要使用 skill 的專案目錄執行，並依提示選擇 Agent。

```sh
npx skills add lloyd3126/skills --skill plan-sdgs-exhibition
npx skills add lloyd3126/skills --skill pdf-margin-review
```

加上 `--list` 可查看儲存庫可安裝的 skills，加上 `-g` 可跨專案使用。詳見 [skills.sh CLI 文件](https://skills.sh/docs/cli)。

維護方式見[專案指引](AGENTS.md)，授權與改編來源見 [NOTICE.md](NOTICE.md)。
