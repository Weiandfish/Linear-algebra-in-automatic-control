# 控制中的线性代数

Linear Algebra in Automatic Control — 课程讲义、中英文学习笔记与作业解答。

当前整理范围为 Lecture 1–2 和 Homework 1，内容包括抽象代数基础、线性空间、基与换基、线性子空间、线性映射及其矩阵表示，以及它们与状态空间模型的联系。

## 从这里开始

- [Lecture 1–2 阅读导航](notes/lecture01-02/00_阅读导航.md)：讲义页码对照、学习目标和章节目录。
- [综合练习与答案](notes/lecture01-02/07_综合练习与答案.md)：12 道练习及解答。
- [术语与公式速查](notes/lecture01-02/08_术语与公式速查.md)：中英术语、核心公式和易错点。
- [Homework 1 中文版](homework/homework01/Homework1_题目与解答.pdf) / [英文版](homework/homework01/Homework1_英文题目与解答.pdf)：题目与简明解答。

## 目录结构

```text
.
├── notes/
│   └── lecture01-02/       # 按章节组织的中英文 Markdown 笔记
├── homework/
│   └── homework01/         # 原始题目、中英文 LaTeX 源码、PDF 和编译脚本
└── materials/
    ├── lectures/           # Lecture 1、Lecture 2 原始课件
    └── reference/          # 参考教材
```

## 笔记目录

| 文件 | 主要内容 |
| --- | --- |
| [01 抽象代数基础](notes/lecture01-02/01_抽象代数基础.md) | 二元运算、群、环与域 |
| [02 线性空间](notes/lecture01-02/02_线性空间.md) | 空间公理、线性组合、线性相关性 |
| [03 基与换基](notes/lecture01-02/03_基与换基.md) | 基、维数、坐标、过渡矩阵 |
| [04 线性子空间](notes/lecture01-02/04_线性子空间.md) | 生成空间、秩、交与和、直和与补空间 |
| [05 线性映射与矩阵表示](notes/lecture01-02/05_线性映射与矩阵表示.md) | 核与像、矩阵表示、秩–零度、映射换基 |
| [06 自动控制联系](notes/lecture01-02/06_自动控制联系_教学补充.md) | 状态方程中的换基 |
| [07 综合练习与答案](notes/lecture01-02/07_综合练习与答案.md) | 综合练习与解答 |
| [08 术语与公式速查](notes/lecture01-02/08_术语与公式速查.md) | 中英术语、公式和做题方法 |

## Homework 1

作业日期为 2026 年 9 月 30 日。中英文两版均包含四道作业题与四个教材例题，并保留必要的解答步骤。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework01/Homework1_题目与解答.pdf) | [源码](homework/homework01/Homework1_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework01/Homework1_英文题目与解答.pdf) | [源码](homework/homework01/Homework1_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework01/Homework1_原始题目.pdf) | — |

直接阅读现成 PDF 即可。若要修改后重新编译，请在安装了 XeLaTeX 的环境中，从仓库根目录运行 PowerShell：

```powershell
& .\homework\homework01\build.ps1
```

脚本会编译目录下的两份 `Homework1_*.tex`，更新同名 PDF，并清理临时编译文件。源码依赖 `ctex`、Fandol 字体及 `geometry`、`amsmath`、`amssymb`、`enumitem`、`needspace`、`hyperref` 等宏包。

## 原始资料

- [Lecture 1](<materials/lectures/Lecture 1-linear algebra.pdf>)：46 页。
- [Lecture 2](<materials/lectures/Lecture 2-linear algebra.pdf>)：29 页。
- [黄琳《系统与控制理论中的线性代数》](materials/reference/系统与控制理论中的线性代数_黄琳.pdf)。

笔记中的“教学补充”标识用于区分补充例题、证明和控制背景与原讲义内容。

## 本地文件

`tmp/` 中的 PDF 渲染图、提取文本等缓存，以及 `.local-backup/` 中的原压缩包和重复原题保留在本地，由 `.gitignore` 排除。作业成品 PDF 随源码一起提交，方便直接阅读。
