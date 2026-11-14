# 图解维护说明

正文直接引用 `assets/diagrams/` 中的 PNG；同名 SVG 将文字转为轮廓，放大或在其他设备查看时不依赖本地字体。图片的几何数据、矩阵元素与布局位于 `build_diagrams.py`，章节锚点和读图说明位于 `add_diagrams_to_notes.py`。

全部 40 张图统一使用纯黑背景、亮色文字与公式，蓝、绿、橙、紫、红区分方向和分组；矩阵重点格使用深色填充配亮色数字。配色集中定义在生成脚本顶部，重新生成会直接覆盖同名 PNG 和 SVG，保持讲义中的图片链接有效。

每张图下方有两个补充面板，围绕图中示例给出计算步骤、判别条件或核对方法。面板文字由 `diagram_details.py` 维护，生成时会校验每个面板的文字是否越界。

生成时根据实际图形边界居中主体，按中英文和公式的实际高度自适应面板，并限制各条目间距，避免文字拥挤或留白过大。

公式由 `math_typography.py` 统一排为 Computer Modern 数学字体；已有的 `$...$` 数学表达式保留原样，中文仍使用 CJK 字体。

标题、图解说明和补充面板按中文、英文顺序配对，图中主要术语在顶部列出对照。英文内容及术语表维护在 `diagram_english.py`；公式在两种语言中共用。

## 重新生成

依赖 Python 3、`matplotlib`、`numpy`、`Pillow`，以及用于生成中文标签的 Noto Sans CJK 字体。仓库根目录下运行：

```bash
python3 scripts/build_diagrams.py
python3 scripts/add_diagrams_to_notes.py
```

只重画指定图片时，可将文件名去掉扩展名后传给生成脚本，例如：

```bash
python3 scripts/build_diagrams.py 27_jordan_chain 28_nullity_staircase
```

生成脚本检查文字是否越出画布。嵌入脚本使用图解注释区块定位已有内容，重复运行会替换对应区块；先校验全部章节锚点，再保存章节，保留周围正文。

## 检查引用

```bash
python3 scripts/add_diagrams_to_notes.py --check
```

该命令检查全部笔记是否配图、图解区块是否重复、PNG 和 SVG 是否齐全，以及 README 和笔记中的本地链接是否有效。修改数值例子时，还需要核对矩阵运算、曲线或块长与图注一致，并重新查看图片的文字和箭头布局。

第四章的 36—40 号图由 `inner_product_diagrams.py` 注册到统一生成器，沿用同一配色、数学排版和自动布局检查。新图涵盖 Gram、Gram–Schmidt、投影、Schur 差额与正定性。

## 中文精简版打印 PDF

`build_print_pdf.py` 从中文精简版的全部内容生成 A4 正文、练习答案、合订本三份 PDF，输出至 `output/pdf/`。练习分册包含 `notes/练习阅读说明.md`，可独立阅读。正文按阅读顺序连续编号为 18 章；原 Markdown 文件名保持不变。

正文使用宋体风格的 Noto Serif CJK，标题使用 Noto Sans CJK，公式由 KaTeX 排为矢量文字。图解从已有 SVG 生成独立的白底打印配色，保留矢量线条和公式，不覆盖原来的黑底图片。合并后重新添加连续页码、章节书签，目录页码随实际分页生成。

需要 Python 包 `markdown-it-py`、`pypdf`、`reportlab`，Node.js 包 `katex`、`playwright`，以及 Chrome、Poppler 和上述 CJK 字体。例如：

```bash
python3 -m pip install markdown-it-py pypdf reportlab
npm install --prefix tmp/pdfs/runtime katex@0.16.22 playwright
python3 scripts/build_print_pdf.py
```

可通过 `--node`、`--node-modules`、`--katex-dir`、`--pdf-python` 指定已有运行时。`--katex-dir` 指向含 `katex.js`、`katex.min.css` 和 `fonts/` 的 `dist` 目录；`CHROME_BIN` 可指定 Chrome 路径。中间 HTML、逐章 PDF、打印用 SVG 和分页记录存放在已忽略的 `tmp/pdfs/chinese-print/`。发布前需渲染最终 PDF，检查公式、图解、目录页码与页边裁切。
