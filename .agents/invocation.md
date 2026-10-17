# 觸發方式

`SKILL.md` frontmatter 必須包含 `name` 與 `description`。description 應讓 agent 能判斷何時使用，必要時指出容易混淆的排除範圍。

預設允許自動探索。使用者明確要求只能手動觸發時，在該 skill 的 `agents/openai.yaml` 設定：

```yaml
policy:
  allow_implicit_invocation: false
```

這是 Codex 的設定；其他 agent 的觸發欄位要另依其官方文件確認。不要把參考專案的手動觸發偏好自動套用到新 skills。
