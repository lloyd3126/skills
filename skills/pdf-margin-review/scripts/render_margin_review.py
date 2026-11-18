#!/usr/bin/env python3
"""Render fixed margin cards and highlights onto a copy of a text PDF."""

import argparse
from datetime import datetime
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
import unicodedata
from zoneinfo import ZoneInfo

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


FONT = "LXGWWenKaiTC"
FONT_PATH = Path(__file__).resolve().parent.parent / "assets" / "LXGWWenKaiTC-Regular.ttf"
SIZE = 9.4
LEADING = 12.5
SECTION_STEP = 17.4
PANEL_WIDTH = 240
PANEL_MARGIN = 12
TOP_PADDING = 18
SIDE_PADDING = 18
BOTTOM_PADDING = 14
CARD_GAP = 10
RED = HexColor("#C00000")
DARK = HexColor("#344254")
ID_PATTERN = re.compile(r"([0-9]{14})-([1-9][0-9]*)")


def read_reviews(path, page_count, source_hash):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("annotations"), list):
        raise ValueError("JSON 需要包含 annotations 陣列")
    if "source_sha256" in data and data["source_sha256"] != source_hash:
        raise ValueError("標注清單對應的原始 PDF 與本次輸入不同")
    annotations = data["annotations"]
    if not annotations:
        raise ValueError("至少需要一筆標注")
    ids = set()
    for index, item in enumerate(annotations, 1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 筆標注必須是物件")
        unknown = item.keys() - {"page", "quote", "comment", "occurrence", "id"}
        if unknown:
            raise ValueError(f"第 {index} 筆有未知欄位：{', '.join(sorted(unknown))}")
        page = item.get("page")
        if type(page) is not int or not 1 <= page <= page_count:
            raise ValueError(f"第 {index} 筆頁碼超出範圍")
        for field in ("quote", "comment"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"第 {index} 筆缺少 {field}")
        occurrence = item.get("occurrence", 1)
        if type(occurrence) is not int or occurrence < 1:
            raise ValueError(f"第 {index} 筆 occurrence 必須是正整數")
        if "id" in item:
            value = item["id"]
            match = ID_PATTERN.fullmatch(value) if isinstance(value, str) else None
            if not match or value in ids:
                raise ValueError(f"第 {index} 筆編號格式錯誤或重複")
            datetime.strptime(match[1], "%Y%m%d%H%M%S")
            ids.add(value)
    return annotations, ids


def compact(text):
    return "".join(character for character in unicodedata.normalize("NFKC", text)
                   if not character.isspace())


def locate_quote(page, item):
    needle = compact(item["quote"])
    stream = []
    positions = []
    for line_number, line in enumerate(page.dedupe_chars().extract_text_lines()):
        for char in line["chars"]:
            for letter in compact(char["text"]):
                stream.append(letter)
                positions.append((line_number, char))

    matches = list(re.finditer(r"(?=" + re.escape(needle) + r")", "".join(stream)))
    location = f"第 {item['page']} 頁「{item['quote']}」"
    if not matches:
        raise ValueError(f"{location}找不到可定位的原文")
    if len(matches) > 1 and "occurrence" not in item:
        offsets = [round(positions[match.start()][1]["top"], 1) for match in matches]
        raise ValueError(f"{location}出現 {len(matches)} 次。距頁頂位置依序為 {offsets} pt，請指定 occurrence")
    occurrence = item.get("occurrence", 1)
    if occurrence > len(matches):
        raise ValueError(f"{location}只有 {len(matches)} 個符合位置")

    start = matches[occurrence - 1].start()
    lines = {}
    for line_number, char in positions[start:start + len(needle)]:
        lines.setdefault(line_number, []).append(char)

    bounds = []
    for chars in lines.values():
        # Avoid painting a long empty band when matched glyphs sit in separate cells.
        ordered = sorted(chars, key=lambda char: char["x0"])
        groups = [[ordered[0]]]
        for char in ordered[1:]:
            previous = groups[-1][-1]
            if char["x0"] - previous["x1"] > max(char["size"], previous["size"]):
                groups.append([])
            groups[-1].append(char)
        for group in groups:
            bounds.append((
                min(char["x0"] for char in group),
                min(char["top"] for char in group),
                max(char["x1"] for char in group),
                max(char["bottom"] for char in group),
            ))
    return bounds


def wrap(text, width):
    lines = []
    for paragraph in text.splitlines():
        row = ""
        for char in paragraph:
            if row and pdfmetrics.stringWidth(row + char, FONT, SIZE) > width:
                if char in "，。！？；：、）」』】》" and len(row) > 1:
                    lines.append(row[:-1].rstrip())
                    row = row[-1]
                else:
                    lines.append(row.rstrip())
                    row = ""
            row += char if row or not char.isspace() else ""
        lines.append(row.rstrip())
    return lines


def make_card(item, bounds, panel_width):
    line_width = panel_width - 2 * (PANEL_MARGIN + SIDE_PADDING)
    groups = [
        (RED, ["編號："] + wrap(item["id"], line_width)),
        (RED, ["原文："] + wrap(item["quote"], line_width)),
        (DARK, ["說明："] + wrap(item["comment"], line_width)),
    ]
    offset = TOP_PADDING + SIZE * 0.88
    rows = []
    for color, lines in groups:
        for line in lines:
            rows.append((offset, color, line))
            offset += LEADING
        offset += SECTION_STEP - LEADING
    height = rows[-1][0] + SIZE * 0.12 + BOTTOM_PADDING
    anchor = (bounds[0][1] + bounds[0][3]) / 2
    return anchor, rows, height


def paginate_cards(entries, page_height, page_number):
    available = page_height - 2 * PANEL_MARGIN
    pages = [[]]
    used = 0
    for item, bounds in entries:
        card = make_card(item, bounds, PANEL_WIDTH)
        height = card[2]
        if height > available:
            raise ValueError(f"第 {page_number} 頁的標注 {item['id']} 單張卡片超過頁面高度，請縮短原文或說明")
        gap = CARD_GAP if pages[-1] else 0
        if used + gap + height > available:
            pages.append([])
            used = 0
            gap = 0
        pages[-1].append(card)
        used += gap + height
    return pages


def position_cards(cards, page_height):
    positions = []
    minimum = PANEL_MARGIN
    for anchor, _, height in cards:
        top = max(minimum, anchor - height / 2)
        positions.append(top)
        minimum = top + height + CARD_GAP

    limit = page_height - PANEL_MARGIN
    for index in range(len(cards) - 1, -1, -1):
        positions[index] = min(positions[index], limit - cards[index][2])
        limit = positions[index] - CARD_GAP
    return list(zip(positions, cards))


def panel_overlay(width, height, panel_width, entries, positioned):
    stream = BytesIO()
    canvas = Canvas(stream, pagesize=(width + panel_width, height), pageCompression=1)
    canvas.saveState()
    canvas.setFillColor(HexColor("#FFD54F"))
    canvas.setFillAlpha(0.35)
    for _, bounds in entries:
        for x0, top, x1, bottom in bounds:
            canvas.rect(x0, height - bottom, x1 - x0, bottom - top, fill=1, stroke=0)
    canvas.restoreState()
    canvas.setFillColor(HexColor("#F1F3F5"))
    canvas.rect(width, 0, panel_width, height, fill=1, stroke=0)

    for top, (_, rows, card_height) in positioned:
        card_x = width + PANEL_MARGIN
        canvas.setFillColor(white)
        canvas.setStrokeColor(HexColor("#D1D5DB"))
        canvas.setLineWidth(0.8)
        canvas.roundRect(card_x, height - top - card_height,
                         panel_width - 2 * PANEL_MARGIN, card_height, 4, fill=1)
        canvas.setFont(FONT, SIZE)
        for offset, color, line in rows:
            canvas.setFillColor(color)
            canvas.drawString(card_x + SIDE_PADDING, height - top - offset, line)

    canvas.showPage()
    canvas.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


def publish(writer, output, manifest, manifest_data):
    staged = []
    published = []
    try:
        for target, write in (
            (output, writer.write),
            (manifest, lambda stream: stream.write(manifest_data)),
        ):
            with NamedTemporaryFile(dir=target.parent, prefix=".margin-review-", delete=False) as stream:
                staged.append((Path(stream.name), target))
                write(stream)
        for temp, target in staged:
            target.hardlink_to(temp)
            published.append(target)
    except Exception:
        for target in published:
            target.unlink()
        raise
    finally:
        for temp, _ in staged:
            temp.unlink(missing_ok=True)


def render(args):
    source, notes, output = (path.resolve() for path in (args.source, args.annotations, args.output))
    manifest = (args.resolved_manifest or output.with_suffix(".annotations.json")).resolve()
    if len({source, notes, output, manifest}) != 4:
        raise ValueError("來源、標注清單及兩個輸出必須使用不同路徑")
    for target in (output, manifest):
        if target.exists():
            raise ValueError(f"輸出已存在：{target}")

    data = source.read_bytes()
    source_hash = sha256(data).hexdigest()
    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        raise ValueError("請提供已解密且可選取文字的 PDF")
    page_sizes = []
    for number, page in enumerate(reader.pages, 1):
        media = tuple(page.mediabox)
        if page.rotation or page.user_unit != 1 or media[:2] != (0, 0) or tuple(page.cropbox) != media:
            raise ValueError(f"第 {number} 頁含頁面旋轉、自訂裁切或座標設定，請先正規化後再標注")
        page_sizes.append((float(page.mediabox.width), float(page.mediabox.height)))

    annotations, ids = read_reviews(notes, len(page_sizes), source_hash)
    entries = [[] for _ in page_sizes]
    with pdfplumber.open(BytesIO(data)) as document:
        for item in annotations:
            page_index = item["page"] - 1
            entries[page_index].append((item, locate_quote(document.pages[page_index], item)))
    for page_entries in entries:
        page_entries.sort(key=lambda entry: (entry[1][0][1], entry[1][0][0]))

    stamp = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d%H%M%S")
    sequence = 1
    for page_entries in entries:
        for item, _ in page_entries:
            if "id" in item:
                continue
            while f"{stamp}-{sequence}" in ids:
                sequence += 1
            item["id"] = f"{stamp}-{sequence}"
            ids.add(item["id"])
            sequence += 1

    font = TTFont(FONT, FONT_PATH)
    missing = sorted({char for item in annotations for field in ("quote", "comment")
                      for char in item[field] if not char.isspace() and ord(char) not in font.face.charWidths})
    if missing:
        raise ValueError("字型缺少這些字元：" + " ".join(missing))
    pdfmetrics.registerFont(font)

    writer = PdfWriter(clone_from=reader)
    output_index = 0
    for page_number, ((width, height), page_entries) in enumerate(zip(page_sizes, entries), 1):
        original_cards, *continuations = paginate_cards(page_entries, height, page_number)
        total_width = width + PANEL_WIDTH
        page = writer.pages[output_index]
        page.mediabox.upper_right = (total_width, height)
        page.cropbox.upper_right = (total_width, height)
        positioned = position_cards(original_cards, height)
        page.merge_page(panel_overlay(width, height, PANEL_WIDTH, page_entries, positioned))
        output_index += 1

        for cards in continuations:
            positioned = []
            top = PANEL_MARGIN
            for card in cards:
                positioned.append((top, card))
                top += card[2] + CARD_GAP
            writer.insert_blank_page(width=total_width, height=height, index=output_index)
            writer.pages[output_index].merge_page(panel_overlay(width, height, PANEL_WIDTH, [], positioned))
            output_index += 1

    manifest_data = (json.dumps({"source_sha256": source_hash, "annotations": annotations},
                                ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    publish(writer, output, manifest, manifest_data)
    print(output)
    print(manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--resolved-manifest", type=Path)
    try:
        render(parser.parse_args())
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
