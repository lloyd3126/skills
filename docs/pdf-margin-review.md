# PDF 頁邊短評

[pdf-margin-review](../skills/pdf-margin-review/SKILL.md) 保留原始 PDF，另存一份副本，在原句上加黃色標記，並在右側卡片顯示編號、原文和說明。

## 在 Codex 使用

在專案目錄用 [README 的指令](../README.md#用-skillssh-安裝)安裝後，附上 PDF 並指定審閱範圍。也可以直接提供要標記的原句與說明。

> 用 `$pdf-margin-review` 幫我檢查這份 PDF 的教學目標與評量方式，並加上頁邊短評。

## 直接執行

Python 環境需要 `pdfplumber`、`pypdf`、`reportlab`。將短評寫成 JSON，格式見 [SKILL.md](../skills/pdf-margin-review/SKILL.md)。

```sh
python3 skills/pdf-margin-review/scripts/render_margin_review.py original.pdf annotations.json review.pdf
```

完成後會產生 `review.pdf` 和 `review.annotations.json`。重排時，把同一份原始 PDF 和輸出的 JSON 交給腳本，並指定新的輸出檔名。

支援可選取文字、未加密、未旋轉且未裁切的 PDF。掃描件需先建立可靠的文字層。同一頁有多處相同原句時，用 `occurrence` 指定要標記的位置。
