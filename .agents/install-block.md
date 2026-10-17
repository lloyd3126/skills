# 本機試用與安裝

目前的實驗項目見 [in-progress 分類目錄](../skills/in-progress/README.md)，本機連結工具不處理此分類。新增並驗證正式 skills 後：

```sh
bash scripts/link-skills.sh
bash scripts/link-skills.sh --apply
```

第一行只預覽，第二行將 `engineering` 與 `productivity` skills 連結到 `~/.agents/skills`。其他分類不會連結。既有同名項目不會被覆蓋；先釐清名稱衝突再處理。

每個連結直接指向此 repo，後續修改會立即影響本機使用的內容。`--apply` 是明確的本機安裝操作，不屬於一般編輯與檢查。

Plugin 設定已預留，待有正式 skill 並在目標 agent 驗證後，再補上實測的安裝命令。
