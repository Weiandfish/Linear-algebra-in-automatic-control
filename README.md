# 控制中的线性代数

Linear Algebra in Automatic Control — 课程讲义、中英文学习笔记与作业解答。

当前整理范围为第 1–8 份讲义和 Homework 1–8，内容包括线性空间、基与换基、子空间、线性映射、多项式、理想、Smith 标准形、不变多项式、初等因子、特征值、不变子空间、自然标准形、复数与实数 Jordan 标准形、最小多项式、循环子空间及两种分解，以及相关控制背景。第 8 份讲义文件的封面写作 Lecture 9，笔记已注明编号差异。

## 从这里开始

- [纯中文精简讲义](notes/中文精简版/00_阅读导航.md)：覆盖前四讲，合为五个正文大章；第四讲仅分两章，保留例题，另有前三讲的 20 道自测题。
- [Lecture 1–2 阅读导航](notes/lecture01-02/00_阅读导航.md)：讲义页码对照、学习目标和章节目录。
- [Lecture 3 阅读导航](notes/lecture03/00_阅读导航.md)：第三讲分章中英文教学笔记、讲义对照和作业关联。
- [Lecture 4 阅读导航](notes/lecture04/00_阅读导航.md)：三个双语正文大章、8 道练习、公式速查与课件勘误。
- [Lecture 5 阅读导航](notes/lecture05/00_阅读导航.md)：两个双语正文大章、8 道练习，涵盖 Smith 标准形、初等因子和特征矩阵。
- [Lecture 6 阅读导航](notes/lecture06/00_阅读导航.md)：两个双语正文大章、8 道练习，涵盖特征值、不变子空间、相似与自然标准形。
- [Lecture 7 阅读导航](notes/lecture07/00_阅读导航.md)：两个双语正文大章、8 道练习，涵盖复数与实数 Jordan 形、链、换基矩阵与子空间分解。
- [Lecture 8 文件阅读导航](notes/lecture08/00_阅读导航.md)：两个双语正文大章、8 道练习，涵盖最小多项式、第一分解、循环子空间、第二分解与平移算子。
- [综合练习与答案](notes/lecture01-02/07_综合练习与答案.md)：12 道练习及解答。
- [术语与公式速查](notes/lecture01-02/08_术语与公式速查.md)：中英术语、核心公式和易错点。
- [Homework 1 中文版](homework/homework01/Homework1_题目与解答.pdf) / [英文版](homework/homework01/Homework1_英文题目与解答.pdf)：题目与简明解答。
- [Homework 2 中文版](homework/homework02/Homework2_题目与解答.pdf) / [英文版](homework/homework02/Homework2_英文题目与解答.pdf)：五道题与简明解答。
- [Homework 3 中文版](homework/homework03/Homework3_题目与解答.pdf) / [英文版](homework/homework03/Homework3_英文题目与解答.pdf)：三道题与简明解答。
- [Homework 4 中文版](homework/homework04/Homework4_题目与解答.pdf) / [英文版](homework/homework04/Homework4_英文题目与解答.pdf)：四道 Smith 标准形与不变多项式题。
- [Homework 5 中文版](homework/homework05/Homework5_题目与解答.pdf) / [英文版](homework/homework05/Homework5_英文题目与解答.pdf)：分块初等因子、微分与平移算子的四道题。
- [Homework 6 中文版](homework/homework06/Homework6_题目与解答.pdf) / [英文版](homework/homework06/Homework6_英文题目与解答.pdf)：特征向量、自然标准形及复、实 Jordan 标准形的三道题。
- [Homework 7 中文版](homework/homework07/Homework7_题目与解答.pdf) / [英文版](homework/homework07/Homework7_英文题目与解答.pdf)：最小多项式的取得、平移算子、标准形及广义特征空间的四道题。
- [Homework 8 中文版](homework/homework08/Homework8_题目与解答.pdf) / [英文版](homework/homework08/Homework8_英文题目与解答.pdf)：最小多项式、平移算子的广义特征向量、换基矩阵与循环生成元的五道题。

## 目录结构

```text
.
├── notes/
│   ├── lecture01-02/       # 前两讲按章节组织的中英文 Markdown 笔记
│   ├── lecture03/          # 第三讲：导航、六章正文、练习与术语公式
│   ├── lecture04/          # 第四讲：三个正文大章、导航和练习速查
│   ├── lecture05/          # 第五讲：两个正文大章、导航和练习速查
│   ├── lecture06/          # 第六讲：两个正文大章、导航和练习速查
│   ├── lecture07/          # 第七讲：两个正文大章、导航和练习速查
│   ├── lecture08/          # 第八份讲义（封面 Lecture 9）：两个正文大章、导航和练习速查
│   └── 中文精简版/         # 五个正文大章、导航和前三讲练习答案，共七个 Markdown 文件
├── homework/
│   ├── homework01/         # 原始题目、中英文 LaTeX 源码、PDF 和编译脚本
│   ├── homework02/         # 第二次作业，含双击编译入口
│   ├── homework03/         # 第三次作业，含双击编译入口
│   ├── homework04/         # 第四次作业，含双击编译入口
│   ├── homework05/         # 第五次作业，含双击编译入口
│   ├── homework06/         # 第六次作业，含双击编译入口
│   ├── homework07/         # 第七次作业，含双击编译入口
│   └── homework08/         # 第八次作业，含双击编译入口
└── materials/
    ├── lectures/           # 第 1—8 份原始课件
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

## Lecture 3 笔记目录

第三讲共 27 页。笔记按正文实际内容组织；第 2 页仅预告了多项式章节，因此未将该预告扩写为讲义正文。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture03/00_阅读导航.md) | 页码对照、阅读顺序、讲义笔误提示、Homework 2 关联 |
| [01 线性映射复习](notes/lecture03/01_线性映射复习.md) | 线性性、恒等与零映射、相关性与反例 |
| [02 矩阵表示与映射空间](notes/lecture03/02_矩阵表示与映射空间.md) | 列的构造、坐标关系、唯一性、映射的加法与数乘 |
| [03 换基与矩阵等价](notes/lecture03/03_换基与矩阵等价.md) | 独立换基、等价关系、行列变换、相似 |
| [04 同构](notes/lecture03/04_同构.md) | 单射、满射、维数、初值映射例子 |
| [05 核与像及秩零度](notes/lecture03/05_核与像及秩零度.md) | 求核与像、坐标还原、维数公式及证明 |
| [06 复合映射](notes/lecture03/06_复合映射.md) | 复合顺序、矩阵乘积、中间基衔接 |
| [07 练习与答案](notes/lecture03/07_练习与答案.md) | 8 道双语自测题及答案 |
| [08 术语与公式速查](notes/lecture03/08_术语与公式速查.md) | 中英术语、核心公式、维数检查 |

## Lecture 4 笔记目录

第四讲共 40 页，正文包含第 2.1—2.6 节。双语笔记合并为三个大章，保留计算例题，并区分原课件内容与教学补充。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture04/00_阅读导航.md) | 页码对照、系数域与符号、作业关联、课件勘误 |
| [01 线性代数与多项式除法](notes/lecture04/01_线性代数与多项式除法.md) | 代数结构、代数同构、代入、欧氏除法、辗转相除 |
| [02 多项式理想与因式分解](notes/lecture04/02_多项式理想与因式分解.md) | 主理想、和与交、最大公因式、贝祖等式、分解与重数 |
| [03 多项式矩阵与幺模变换](notes/lecture04/03_多项式矩阵与幺模变换.md) | 次数、左右除法、秩、幺模、初等变换、等价 |
| [04 练习与公式速查](notes/lecture04/04_练习与公式速查.md) | 8 道双语练习及答案、术语与公式 |

## Lecture 5 笔记目录

第五讲共 21 页，正文包含第 2.6—2.7 节；第 2.8 节只在提纲中预告。笔记合并为两个双语正文大章，区分行列式因子、不变多项式和初等因子，并保留例题的关键计算。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture05/00_阅读导航.md) | 页码对照、符号、完整条件、作业对应与例题来源 |
| [01 Smith 标准形与不变多项式](notes/lecture05/01_Smith标准形与不变多项式.md) | 幺模、初等变换、降次算法、行列式因子、唯一性与计算 |
| [02 初等因子与特征矩阵](notes/lecture05/02_初等因子与特征矩阵.md) | 初等因子重数、恢复不变多项式、等价、分块与特征矩阵 |
| [03 练习与公式速查](notes/lecture05/03_练习与公式速查.md) | 8 道双语练习及答案、公式、秩与单位因子检查 |

## Lecture 6 笔记目录

第六讲共 24 页，进入第三章第 3.1—3.2 节。笔记分为两个正文大章，保留矩阵幂的讲义推导，增加微分、平移和伴随块的计算例题，并明确抽象特征向量与坐标列的区别。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture06/00_阅读导航.md) | 页码对照、空间维数、变量约定、课件勘误与作业对应 |
| [01 特征值与不变子空间](notes/lecture06/01_特征值与不变子空间.md) | 换基、不变子空间、特征空间、代数与几何重数、微分与平移 |
| [02 相似不变量与自然标准形](notes/lecture06/02_相似不变量与自然标准形.md) | 特征矩阵的相似判据、列伴随矩阵、自然标准形、换基与作业例题 |
| [03 练习与公式速查](notes/lecture06/03_练习与公式速查.md) | 8 道双语练习及答案、公式与必要条件 |

## Lecture 7 笔记目录

第七讲共 21 页，复习自然标准形并展开第 3.3 节 Jordan 标准形。笔记分为两个正文大章，保留推导关系，补充完整 Jordan 基与作业标准形的计算例题，明确广义特征空间与普通特征空间的区别。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture07/00_阅读导航.md) | 页码对照、块与链的约定、实数条件、例题来源、作业对应 |
| [01 复数与实数 Jordan 标准形](notes/lecture07/01_复数与实数Jordan标准形.md) | 互素拆块、复 Jordan 块、共轭实块、三阶及十一阶作业例题 |
| [02 Jordan 链与子空间分解](notes/lecture07/02_Jordan链与子空间分解.md) | 广义特征向量、链头独立、换基验证、Jordan 子空间、实基与核维数 |
| [03 练习与公式速查](notes/lecture07/03_练习与公式速查.md) | 8 道双语练习及答案、公式、维数与链条件检查 |

## Lecture 8 文件笔记目录

本次讲义共 23 页，文件名为第 8 讲，封面标作 Lecture 9，内容为第 3.4—3.5 节；第 22、23 页重复。笔记合为两个正文大章，区分局部与整体最小多项式，保留证明思路，并补齐可直接验证的循环基与平移算子例题。

| 文件 | 主要内容 |
| --- | --- |
| [00 阅读导航](notes/lecture08/00_阅读导航.md) | 页码对照、编号差异、符号与必要条件、勘误、作业对应 |
| [01 最小多项式与第一分解](notes/lecture08/01_最小多项式与第一分解.md) | 零化理想、整除关系、最大不变多项式、分块最小公倍式、互素分解与取得定理 |
| [02 循环子空间与第二分解](notes/lecture08/02_循环子空间与第二分解.md) | 循环基与伴随块、第二分解、Newton 多项式基、平移算子、换基方向 |
| [03 练习与公式速查](notes/lecture08/03_练习与公式速查.md) | 8 道双语练习及答案、核心公式与条件 |

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

## Homework 2

作业日期为 2026 年 10 月 10 日。两版均保留五道题与全部子题，中文版本翻译题目并用中文作答，英文版本保留英文题目并用英文作答。首页已加入 YuanHao Tang / 3120265621。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework02/Homework2_题目与解答.pdf) | [源码](homework/homework02/Homework2_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework02/Homework2_英文题目与解答.pdf) | [源码](homework/homework02/Homework2_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework02/Homework2_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework02/编译PDF.cmd)，即可用 XeLaTeX 更新两份 PDF。编译结果或错误会留在窗口中，按任意键关闭。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework02\build.ps1
```

## Homework 3

作业日期为 2026 年 10 月 15 日，包含节点基下的反射变换与两道多项式理想题。中文版本翻译题目并用中文作答；英文版本保留英文题目并用英文作答。两版均保留全部三题及子题，首页加入 YuanHao Tang / 3120265621。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework03/Homework3_题目与解答.pdf) | [源码](homework/homework03/Homework3_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework03/Homework3_英文题目与解答.pdf) | [源码](homework/homework03/Homework3_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework03/Homework3_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework03/编译PDF.cmd)，即可重新生成两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework03\build.ps1
```

## Homework 4

作业日期为 2026 年 10 月 16 日，包含四道 Smith 标准形与不变多项式题。中文版本翻译题目并用中文作答；英文版本保留原题并用英文作答。两版均保留全部矩阵与必要解答，首页加入 YuanHao Tang / 3120265621。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework04/Homework4_题目与解答.pdf) | [源码](homework/homework04/Homework4_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework04/Homework4_英文题目与解答.pdf) | [源码](homework/homework04/Homework4_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework04/Homework4_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework04/编译PDF.cmd)，即可更新两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework04\build.ps1
```

## Homework 5

作业日期为 2026 年 10 月 21 日，包含分块多项式矩阵、求导线性、平移算子的特征值，以及有限维微分算子的初等因子。两版保留四道题与全部子题，中文版本翻译题目并作答，英文版本保留原题并用英文作答，首页加入 YuanHao Tang / 3120265621。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework05/Homework5_题目与解答.pdf) | [源码](homework/homework05/Homework5_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework05/Homework5_英文题目与解答.pdf) | [源码](homework/homework05/Homework5_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework05/Homework5_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework05/编译PDF.cmd)，即可更新两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework05\build.ps1
```

## Homework 6

作业日期为 2026 年 10 月 23 日，包含矩阵及抽象算子的特征向量，以及 Smith、自然、复 Jordan 和实 Jordan 标准形。两版保留三道题与全部子题，中文版本翻译题目并作答，英文版本保留原题并用英文作答，首页加入 YuanHao Tang / 3120265621。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework06/Homework6_题目与解答.pdf) | [源码](homework/homework06/Homework6_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework06/Homework6_英文题目与解答.pdf) | [源码](homework/homework06/Homework6_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework06/Homework6_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework06/编译PDF.cmd)，即可更新两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework06\build.ps1
```

## Homework 7

作业日期为 2026 年 10 月 28 日，包含最小多项式可由单向量取得的证明、平移算子的 Smith/Jordan 形及换基矩阵、两组初等因子对应的标准形和广义特征空间。两版保留四道题及全部子题，中文版本翻译题目并作答，英文版本保留原题并用英文作答，首页加入 YuanHao Tang / 3120265621。两组标准形分别对应 10 维与 11 维空间。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework07/Homework7_题目与解答.pdf) | [源码](homework/homework07/Homework7_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework07/Homework7_英文题目与解答.pdf) | [源码](homework/homework07/Homework7_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework07/Homework7_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework07/编译PDF.cmd)，即可更新两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework07\build.ps1
```

## Homework 8

作业日期为 2026 年 10 月 30 日，包含四道最小多项式计算题及一道平移算子综合题。两版保留五道题及全部子题，中文版本翻译题目并作答，英文版本保留原题并用英文作答，首页加入 YuanHao Tang / 3120265621。平移算子的解答给出全部非零广义特征向量、Newton 基的系数换基矩阵及一个循环生成元。

| 资料 | PDF | LaTeX 源码 |
| --- | --- | --- |
| 中文题目与解答 | [查看](homework/homework08/Homework8_题目与解答.pdf) | [源码](homework/homework08/Homework8_题目与解答.tex) |
| 英文题目与解答 | [查看](homework/homework08/Homework8_英文题目与解答.pdf) | [源码](homework/homework08/Homework8_英文题目与解答.tex) |
| 原始题目 | [查看](homework/homework08/Homework8_原始题目.pdf) | — |

保存源码后，双击 [编译PDF.cmd](homework/homework08/编译PDF.cmd)，即可更新两份 PDF。也可从仓库根目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\homework\homework08\build.ps1
```

## 原始资料

- [Lecture 1](<materials/lectures/Lecture 1-linear algebra.pdf>)：46 页。
- [Lecture 2](<materials/lectures/Lecture 2-linear algebra.pdf>)：29 页。
- [Lecture 3](<materials/lectures/Lecture 3-linear algebra.pdf>)：27 页。
- [Lecture 4](<materials/lectures/Lecture 4-linear algebra.pdf>)：40 页。
- [Lecture 5](<materials/lectures/Lecture 5-linear algebra.pdf>)：21 页。
- [Lecture 6](<materials/lectures/Lecture 6-linear algebra.pdf>)：24 页。
- [Lecture 7](<materials/lectures/Lecture 7-linear algebra.pdf>)：21 页。
- [Lecture 8 文件（封面 Lecture 9）](<materials/lectures/Lecture 8-linear algebra.pdf>)：23 页。
- [黄琳《系统与控制理论中的线性代数》](materials/reference/系统与控制理论中的线性代数_黄琳.pdf)。

笔记中的“教学补充”标识用于区分补充例题、证明和控制背景与原讲义内容。

## 本地文件

`tmp/` 中的 PDF 渲染图、提取文本等缓存，以及 `.local-backup/` 中的原压缩包和重复原题保留在本地，由 `.gitignore` 排除。作业成品 PDF 随源码一起提交，方便直接阅读。
