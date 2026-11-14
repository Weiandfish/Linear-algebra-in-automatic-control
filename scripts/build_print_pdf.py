#!/usr/bin/env python3
"""Build the Chinese notes as an A4 print book and two independently paged volumes.

Python: markdown-it-py, pypdf, reportlab. Node: katex, playwright.
Chrome must be installed. No changes are made to the Markdown or screen diagrams.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tmp/pdfs/chinese-print"
OUT = ROOT / "output/pdf"
NAMES = {
    "book": "线性代数_中文精简版_合订本.pdf",
    "notes": "线性代数_中文精简版_正文.pdf",
    "practice": "线性代数_中文精简版_练习与答案.pdf",
}
MATH = re.compile(r"\$\$([\s\S]*?)\$\$|(?<!\\)\$([^$\n]+)(?<!\\)\$")
NUMBERS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八"]


def print_svg(source: Path, target: Path) -> None:
    # Recolour the editable vector source; preserve paths, labels and geometry.
    palette = {
        "#000000": "#ffffff", "#10151d": "#f7f7f7",
        "#f4f7fb": "#111111", "#b5c1d2": "#444444",
        "#303a49": "#c5c5c5", "#73b7ff": "#24475e",
        "#5eead4": "#24564d", "#ffc66d": "#765015",
        "#c4a1ff": "#57416f", "#ff8196": "#81394b",
        "#162c45": "#e9eef1", "#10352f": "#e9f0ed",
        "#3b2b14": "#f3eee5", "#2e2044": "#eeebf2",
        "#3c1e28": "#f3e9ec", "#1f2835": "#eeeeee",
        "#1f77b4": "#24475e",
    }
    text = re.sub(r"#[0-9a-fA-F]{6}", lambda m: palette.get(m[0].lower(), m[0]), source.read_text())
    tree = ET.fromstring(text)
    ns = {"s": "http://www.w3.org/2000/svg"}
    # Matplotlib omits fill="black" because black is SVG's default. This also
    # happens on subplot backgrounds, not just the outer figure rectangle.
    for group in tree.findall(".//s:g", ns):
        if group.get("id", "").startswith("patch_"):
            for shape in group.findall("s:path", ns):
                style = shape.get("style", "")
                if "fill:" not in style and shape.get("fill") is None:
                    shape.set("style", style + "; fill: #ffffff")
    ET.register_namespace("", ns["s"])
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    target.write_bytes(ET.tostring(tree, encoding="utf-8", xml_declaration=True))


def prepare() -> None:
    from markdown_it import MarkdownIt

    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "diagrams").mkdir(exist_ok=True)
    folder = ROOT / "notes/中文精简版"
    paths = sorted(folder.glob("*.md"))
    chapters = [p for p in paths if 1 <= int(p.name[:2]) <= 13 or 16 <= int(p.name[:2]) <= 20]
    sources = [paths[0], *chapters, ROOT / "notes/练习阅读说明.md", *[p for p in paths if p.name[:2] in ("14", "15")]]
    parser = MarkdownIt("commonmark", {"html": True}).enable("table")
    equations = []
    documents = []
    diagram_paths = set()
    for i, path in enumerate(sources):
        text = path.read_text()
        if path.name.startswith("00_"):
            # The printed table of contents replaces the web file-navigation table.
            text = re.sub(r"## 目录\n[\s\S]*?(?=## 标准形的学习顺序)", "", text)
            text = text.replace("，另附本导航和两份练习答案，共 21 个文件", "，另附两份综合练习与完整答案")
            text = text.replace("新增 16—20 章", "新增内积与正定性部分")
            text = text.replace("需要集中找图时，打开[图解索引](../图解索引.md)。", "")
            renumber = {"十六": "十四", "十七": "十五", "十八": "十六", "十九": "十七", "二十": "十八"}
            text = re.sub(r"第(十六|十七|十八|十九|二十)(?:、(十六|十七|十八|十九|二十))?", lambda m: "第" + renumber[m[1]] + ("、" + renumber[m[2]] if m[2] else ""), text)
            title = "阅读说明与公式速查"
            volume = "notes"
        elif path in chapters:
            number = chapters.index(path) + 1
            title = re.sub(r"^#\s*(?:第[一二三四五六七八九十]+章\s*)?", "", text.splitlines()[0]).strip()
            title = f"第{NUMBERS[number - 1]}章　{title}"
            volume = "notes"
        elif path.name == "练习阅读说明.md":
            title, volume = "练习阅读说明", "practice"
        else:
            title = "综合练习 A　第一至第三讲" if path.name.startswith("14_") else "综合练习 B　第五至第八讲"
            volume = "practice"
        text = re.sub(r"^# .*$", "# " + title, text, count=1, flags=re.M)
        text = "\n".join(line for line in text.splitlines() if not (
            (line.startswith("[") and "](" in line)
            or line.startswith(("原双语版：", "新增双语版："))
            or line.startswith("打印版 PDF：")
        ))
        # Web navigation comments and exercise anchor elements do not belong on paper.
        text = re.sub(r"<!--[\s\S]*?-->", "", text)
        text = re.sub(r'<a\s+id="[^"]+"\s*></a>', "", text)

        def math(match: re.Match[str]) -> str:
            item = {"id": f"MATHEQ{len(equations):05}TOKEN", "tex": match[1] if match[1] is not None else match[2], "display": match[1] is not None, "source": str(path.relative_to(ROOT))}
            equations.append(item)
            return "\n<div class=\"display-equation\">" + item["id"] + "</div>\n" if item["display"] else item["id"]
        text = MATH.sub(math, text)
        if "$" in text:
            raise ValueError(f"Unmatched math delimiter in {path}")
        body = parser.render(text)

        def image(match: re.Match[str]) -> str:
            source = (path.parent / match[1]).resolve().with_suffix(".svg")
            target = WORK / "diagrams" / source.name
            if source not in diagram_paths:
                print_svg(source, target)
                diagram_paths.add(source)
            return 'src="' + target.as_uri() + '"'
        body = re.sub(r'src="([^"]+)"', image, body)
        # Keep each vector illustration together with its title and reading note.
        body = re.sub(r"<p><strong>图解[\s\S]*?</strong></p>\s*<p><img [\s\S]*?</p>\s*<p><strong>读图：[\s\S]*?</p>", lambda m: "<figure>" + m[0] + "</figure>", body)
        # External and repository-file links are plain text in the printed edition.
        body = re.sub(r'<a\b[^>]*>([\s\S]*?)</a>', r"\1", body)
        documents.append({"id": f"chapter-{i:02}", "title": title, "volume": volume, "source": str(path.relative_to(ROOT)), "body": body})
    data = {"documents": documents, "equations": equations, "diagrams": len(diagram_paths)}
    (WORK / "input.json").write_text(json.dumps(data, ensure_ascii=False))
    print(f"Prepared {len(documents)} units, {len(equations)} formulas, {len(diagram_paths)} vector diagrams", flush=True)


def assemble() -> None:
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas

    manifest = json.loads((WORK / "manifest.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    for volume in ("notes", "practice", "book"):
        parts = manifest[volume]
        writer = PdfWriter()
        for part in parts:
            reader = PdfReader(part["pdf"])
            offset = len(writer.pages)
            writer.append(reader, import_outline=False)
            if part.get("title"):
                writer.add_outline_item(part["title"], offset)
        total = len(writer.pages)
        # Use one continuous page sequence, including the cover and contents.
        for number, page in enumerate(writer.pages, 1):
            if number == 1:
                continue
            packet = BytesIO()
            width, height = float(page.mediabox.width), float(page.mediabox.height)
            stamp = canvas.Canvas(packet, pagesize=(width, height))
            stamp.setFillGray(0.32)
            stamp.setFont("Helvetica", 8)
            stamp.drawCentredString(width / 2, 24, f"{number} / {total}")
            stamp.save()
            packet.seek(0)
            page.merge_page(PdfReader(packet).pages[0])
            page.compress_content_streams(level=9)
        writer.compress_identical_objects()
        writer.add_metadata({"/Title": "线性代数 · 中文精简版" + {"book": " · 合订本", "notes": " · 正文", "practice": " · 练习与答案"}[volume], "/Author": "Linear algebra course notes", "/Subject": "A4 打印版 · 18 章正文 · 40 道练习", "/Creator": "scripts/build_print_pdf.py"})
        writer.page_mode = "/UseOutlines"
        target = OUT / NAMES[volume]
        with target.open("wb") as stream:
            writer.write(stream)
        check = PdfReader(target)
        assert len(check.pages) == total
        assert all(abs(float(p.mediabox.width) - 595.28) < 1 and abs(float(p.mediabox.height) - 841.89) < 1 for p in check.pages)
        report[volume] = {"path": str(target), "pages": total, "bytes": target.stat().st_size}
        print(f"Wrote {target.name}: {total} A4 pages, {target.stat().st_size / 1024 / 1024:.1f} MiB", flush=True)
    (WORK / "output-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assemble", action="store_true")
    parser.add_argument("--node", default=shutil.which("node"))
    parser.add_argument("--node-modules", type=Path, default=ROOT / "tmp/pdfs/runtime/node_modules")
    parser.add_argument("--katex-dir", type=Path)
    parser.add_argument("--pdf-python", default=sys.executable)
    args = parser.parse_args()
    if args.assemble:
        assemble()
        return
    if not args.node:
        parser.error("Pass --node with a Node.js executable path")
    prepare()
    katex = args.katex_dir or args.node_modules / "katex/dist"
    subprocess.run([args.node, str(ROOT / "scripts/render_print_pdf.cjs"), str(WORK), str(args.node_modules.resolve()), str(katex.resolve())], check=True)
    subprocess.run([args.pdf_python, str(Path(__file__).resolve()), "--assemble"], check=True)


if __name__ == "__main__":
    main()
