# 本機試用與安裝

正式 skills 見 [productivity 分類目錄](../skills/productivity/README.md)。維護者可以在 repo 根目錄使用以下工具：

```sh
bash scripts/link-skills.sh
bash scripts/link-skills.sh --apply
```

第一行只預覽，第二行將 `engineering` 與 `productivity` skills 連結到 `~/.agents/skills`。其他分類不會連結。既有同名項目不會被覆蓋；先釐清名稱衝突再處理。

每個連結直接指向此 repo，後續修改會立即影響本機使用的內容。`--apply` 是明確的本機安裝操作，不屬於一般編輯與檢查。

專案級安裝 `plan-sdgs-exhibition` 的提示見[使用說明](../docs/productivity/plan-sdgs-exhibition.md)。這與上方的個人目錄連結工具是不同的安裝範圍。

Plugin 清單包含正式 skills；plugin 安裝尚未在目標 agent 驗證，驗證後再補上實測命令。
