#!/usr/bin/env python3
"""Embed the teaching figures beside their sections and rebuild the visual index.

Run after build_diagrams.py. Existing diagram blocks are replaced, so running
this command again does not duplicate figures or modify the surrounding notes.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re

from build_diagrams import ROOT, TITLES

CAPTIONS = {
    "36_inner_product_gram": r"蓝、绿两条基向量不正交，因此 Gram 矩阵含非零交叉项。坐标 $(0,1)^T$ 代表第二个基向量，普通坐标长度平方为 1，而原向量长度平方为 2；计算几何量时必须使用 $x^*Gx$。",
    "37_gram_schmidt_unitary": r"先保留第一列的单位方向，再从第二列减去该方向上的投影，剩余方向正交。投影系数及残差长度形成上三角矩阵 $R$；满秩与正对角条件一起保证 QR 唯一。",
    "38_projection_adjoint": r"两图投向同一条横轴，但左图沿斜核方向投影，右图沿垂直方向投影。幂等只保证可以分解为像与核；加入自伴条件，核才等于像的正交补，得到 $UU^*$。",
    "39_normal_schur": r"两矩阵都有特征值 1、3。左图严格上三角元 2 额外贡献平方范数 4；右图差额为零。一般矩阵先作酉 Schur 三角化，才能用这个差额判断正规性。",
    "40_hermitian_positive": r"左图是实平面上的三条椭圆等值线，长短轴对应特征值 1、3。右图用正特征值和正顺序主子式验证同一矩阵正定；对复向量的结论由酉谱分解给出。",
    "01_algebra_rules": "先看集合配了几种运算，再看每种运算满足什么规则。群只讨论一种运算；环增加乘法与分配律；域要求非零标量可除。图中的箭头表示增加规则，不表示群、环、域是同一集合里的三层子集。",
    "02_linear_combination": r"左图把 $2u+v$ 画成首尾相接的两段，紫色箭头是结果。右图的第三个方向已能由前两个相加得到，因此三个向量整体相关；不能仅凭两两不平行判断无关。",
    "03_subspace_affine": r"左边的直线含原点且对线性组合封闭；中间的平移直线不含原点；右边的轴的并虽然含原点，但两个轴上向量相加会跑出集合。判断子空间时，这两个条件都要检查。",
    "04_basis_coordinates": r"两图中的紫色箭头都是 $v=(4,2)$。旧基量出系数 $(4,2)$，新基量出 $(3,1)$，因为 $3(1,1)+(1,-1)=(4,2)$。先固定“新基 = 旧基 × P”，坐标转换方向就能推出来。",
    "05_sum_direct_sum": r"两条坐标轴的并只包含轴上的点；它们的和却能生成整个平面。交为零让每个向量的两部分分解唯一，这才是直和的关键，不是要求两条方向垂直。",
    "06_matrix_columns": r"先把输入拆成各基向量的线性组合，再用原系数重组基向量的像。矩阵把这些像的坐标逐列存好，因此“矩阵乘坐标列”就是这次重组。",
    "07_kernel_projection": r"把整个输入平面压到横轴时，同一竖线上的点到达同一个输出。绿色竖线被整体压成零，所以它是核；输出横轴是像。这个二维投影是理解核与像的具体例子。",
    "08_rank_nullity": r"对图中的三维到二维投影，两个独立方向保留在像中，一个方向落进核中，所以 $3=2+1$。秩数的是独立输出方向，零度数的是被映成零的独立输入方向。",
    "09_isomorphism": r"多项式 $a+bt$ 和系数列 $(a,b)^{\mathsf T}$ 是两种对象，但可以保持线性运算地来回互译。每个输入都有唯一输出且不漏输出，因此这张“翻译表”给出同构。",
    "10_composition": r"输入 $(1,2)$ 先经 S 得到 $(1,2,3)$，再经 T 得到 $(4,-1)$。矩阵写作 $AM$，因为右边的 M 先作用；若中间两端采用不同基，还须插入坐标转换。",
    "11_linearity": r"从左上出发，先相加再作用 T，与先分别作用再相加，应得到同一个结果；数乘也必须如此。平方映射虽然把零送到零，却通不过加法这一关。",
    "12_basis_change_map": r"新输入坐标先经 P 翻译成旧坐标，再经 A 作用，最后经 $Q^{-1}$ 翻译成新输出坐标，因此新矩阵为 $Q^{-1}AP$。同步换同一组基时，Q 才等于 P，得到相似变换。",
    "13_control_coordinates": r"这是一个无输入系统的补充例子：右图的两个坐标方向分别衰减，左图通过同一个常数可逆矩阵 P 重组。每一时刻的状态一一对应，坐标改变后看到的曲线和系统矩阵也随之改变。",
    "14_map_space": r"一个 $2\times3$ 矩阵有六个可独立调节的位置。每个矩阵单位基元 $E_{ij}$ 只保留一个位置，对应一个最基本的线性映射；六个基元线性组合就能得到任意这样的映射。",
    "15_polynomial_division": r"先减去 $\lambda(\lambda^2+1)$，再减去 $2(\lambda^2+1)$，最高次项逐次消掉，最后剩下 -1。每次余式次数降低，是多项式除法、辗转相除以及史密斯降次算法共同使用的思路。",
    "16_ideal_lattice": r"图中向上走，生成元的因子要求减少，允许的倍数反而更多。因此理想的和对应最大公因式，交对应最小公倍式；不要把生成元的整除方向直接当作理想的包含方向。",
    "17_polynomial_layers": r"每一层常数矩阵只收集同一幂次的系数。最高层非零说明次数为 2，但这一层并不一定可逆；矩阵多项式相乘时仍要保持系数矩阵的乘法次序。",
    "18_unimodular": r"把一行的多项式倍数加到另一行，可以减回去，逆仍是多项式。把整行乘以 λ 则需要除以 λ 才能撤销，逆中出现分母，所以不能作为幺模初等变换。",
    "19_smith_steps": r"四帧保留每一步合法操作：交换列、消掉左下角、消掉右上角、再首一化。最终不是随便一个对角矩阵，还要求对角元组成整除链。",
    "20_determinantal_divisors": r"上排是单个不变多项式，下排是从第一项累计乘到当前位置的行列式因子。反方向用相邻两个累计结果相除，就取回单项：$d_k=D_k/D_{k-1}$。",
    "21_factor_alignment": r"每种根的指数单独从小到大排，不足的位置在左边补零，再按列相乘。这样每一行的指数都不下降，恢复出的不变多项式自然构成整除链；图示对象是秩为 3 的一般多项式矩阵。",
    "22_eigen_directions": r"蓝色向量变长但仍在横轴方向上，绿色方向的向量保持不变；一般向量则被剪切到另一条方向。特征向量的关键是像仍为它的标量倍数，而非所有向量都能只做缩放。",
    "23_invariant_subspace": r"横轴的一组基的像仍在横轴，因此整条横轴不变；纵轴的基向量的像跑出了纵轴，因此该子空间不变性不成立。只需检验子空间的一组基，不用枚举其中所有向量。",
    "24_companion_cycle": r"在循环基 $(v,Av,A^2v)$ 下，前两次作用只是把向量送到下一个基向量。第三次作用由多项式关系拉回已有三个方向，因此最后一列是关系式移项后的系数。",
    "25_jordan_blocks": r"这是同一个根有三阶、二阶两块的五维例子。总格数给代数重数 5，块数给几何重数 2，最长块给最小多项式指数 3；三个数字各自回答不同问题。",
    "26_real_jordan": r"二阶块与它的共轭块配对，用复链向量的实部、虚部作新基，就得到四阶实块。对角的两个二维块负责共轭根，橙色的单位块负责链之间的接力。",
    "27_jordan_chain": r"N 每作用一次就把链尾向链头推近一步，而换基矩阵的列按链头到链尾排列。这一反向关系解释了为什么若尔当块中的 1 位于超对角线。",
    "28_nullity_staircase": r"第 k 次幂会杀掉每条链前 k 格，所以核维数依次为 2、4、5、5。新增的 2、2、1、0 格就是长度至少为 k 的块数，从而读出块长为 3 和 2。",
    "29_minimal_vs_characteristic": r"同一根出现多个块时，特征多项式要数它们一共占多少维，最小多项式只要求能杀掉最长的一块。图中根 1 的指数分别为 4 和 3，不能混用。",
    "30_two_decompositions": r"四维补充例子把同一组链分两次组。左边按根把三个根 1 的方向放在一起；右边按不变多项式组织循环分量，生成元 $x_2+z_1$ 可以同时带出不同根的方向，因此分量维数无需逐项对应。",
    "31_cyclic_growth": r"从一个向量出发，依次收集 v、Av、A²v；这三列独立，所以张成整个三维空间。A³v 已可由前面三列表示，再反复作用也不会产生新的独立方向。",
    "32_finite_difference": r"左表第一行是在 t=0、1、2、3、4 处的函数值，下一行每项取上一行相邻两项的右减左。二次变一次、一次变常数、常数变零；右侧恰好把这种过程组织成归一化链。",
    "33_course_map": "图中的 01—13 是中文版章节编号。先用空间、基和映射建立坐标语言，再用多项式工具读取矩阵结构，最后把各条链组织成不同的不变分量。",
    "34_problem_routes": "先明确题目给的是空间、映射、坐标矩阵还是多项式矩阵，再选择计算工具。空间题检查维数，标准形题检查因子和总阶数，换基题同时检查矩阵等式与可逆性。",
    "35_characteristic_matrix": r"特征矩阵的史密斯形保留了如何分块的信息。本例只有一个初等因子 $(\lambda-1)^2$，对应一个二阶块；若把两个一阶因子合并，就会误判矩阵结构。",
}

# Section labels are prefixes, so bilingual headings retain their English suffix.
ROUTES = {
    "lecture09/01_内积与Gram矩阵.md": [("二、Gram", ["36_inner_product_gram"])],
    "lecture09/02_正交规范基与酉变换.md": [("二、Gram", ["37_gram_schmidt_unitary"])],
    "lecture10/01_投影与伴随变换.md": [("二、正交补", ["38_projection_adjoint"])],
    "lecture10/02_正规矩阵与Schur及QR分解.md": [("四、Schur", ["39_normal_schur"])],
    "lecture10/03_Hermitian型与正定性.md": [("四、主子式", ["40_hermitian_positive"])],
    "中文精简版/16_内积与Gram矩阵.md": [("二、Gram", ["36_inner_product_gram"])],
    "中文精简版/17_正交规范基与酉变换.md": [("二、Gram", ["37_gram_schmidt_unitary"])],
    "中文精简版/18_投影与伴随变换.md": [("二、正交补", ["38_projection_adjoint"])],
    "中文精简版/19_正规矩阵与Schur及QR分解.md": [("四、Schur", ["39_normal_schur"])],
    "中文精简版/20_Hermitian型与正定性.md": [("四、主子式", ["40_hermitian_positive"])],
    "中文精简版/01_代数基础与线性空间.md": [("一、运算与群", ["01_algebra_rules"]), ("四、线性组合与相关性", ["02_linear_combination"])],
    "中文精简版/02_基与换基及子空间.md": [("二、过渡矩阵", ["04_basis_coordinates"]), ("三、子空间、生成空间与秩", ["03_subspace_affine"]), ("五、直和与补空间", ["05_sum_direct_sum"])],
    "中文精简版/03_线性映射及其矩阵表示.md": [("一、线性映射与基本性质", ["11_linearity"]), ("二、矩阵表示", ["06_matrix_columns"]), ("三、换基", ["12_basis_change_map"]), ("四、核、像与秩零度", ["07_kernel_projection", "08_rank_nullity"]), ("五、同构", ["09_isomorphism"]), ("六、复合映射", ["10_composition"]), ("七、与状态空间模型", ["13_control_coordinates"])],
    "中文精简版/04_代数与多项式及理想.md": [("二、多项式除法", ["15_polynomial_division"]), ("四、理想的和与交", ["16_ideal_lattice"])],
    "中文精简版/05_多项式矩阵与幺模变换.md": [("一、表示、次数与乘法", ["17_polynomial_layers"]), ("四、幺模与多项式逆", ["18_unimodular"])],
    "中文精简版/06_史密斯标准形与不变多项式.md": [("三、化简为什么能够完成", ["19_smith_steps"]), ("四、行列式因子", ["20_determinantal_divisors"])],
    "中文精简版/07_初等因子与特征矩阵.md": [("二、从初等因子", ["21_factor_alignment"]), ("五、特征矩阵", ["35_characteristic_matrix"])],
    "中文精简版/08_特征值与不变子空间.md": [("二、不变子空间", ["23_invariant_subspace"]), ("三、特征值与特征空间", ["22_eigen_directions"])],
    "中文精简版/09_相似不变量与自然标准形.md": [("一、哪些量", ["35_characteristic_matrix"]), ("二、列伴随矩阵", ["24_companion_cycle"])],
    "中文精简版/10_复数与实数若尔当标准形.md": [("二、一个初等因子", ["25_jordan_blocks"]), ("五、实矩阵", ["26_real_jordan"])],
    "中文精简版/11_若尔当链与子空间分解.md": [("二、链关系", ["27_jordan_chain"]), ("四、不求初等因子", ["28_nullity_staircase"])],
    "中文精简版/12_最小多项式与第一分解.md": [("二、矩阵最小多项式", ["29_minimal_vs_characteristic"]), ("三、第一分解", ["30_two_decompositions"])],
    "中文精简版/13_循环子空间与第二分解.md": [("一、循环子空间", ["31_cyclic_growth"]), ("二、第二分解", ["30_two_decompositions"]), ("三、平移算子", ["32_finite_difference"])],
    "lecture01-02/01_抽象代数基础.md": [("1.1.4 环与域", ["01_algebra_rules"])],
    "lecture01-02/02_线性空间.md": [("1.2.1 线性空间", ["03_subspace_affine"]), ("1.2.2 线性组合", ["02_linear_combination"])],
    "lecture01-02/03_基与换基.md": [("1.3.2 过渡矩阵", ["04_basis_coordinates"])],
    "lecture01-02/04_线性子空间.md": [("1.4.1 子空间", ["03_subspace_affine"]), ("1.4.4 直和与补空间", ["05_sum_direct_sum"])],
    "lecture01-02/05_线性映射与矩阵表示.md": [("1.5.2 基本性质", ["07_kernel_projection", "08_rank_nullity"]), ("1.5.3 线性映射的矩阵表示", ["06_matrix_columns"]), ("1.5.4 映射矩阵换基", ["12_basis_change_map"])],
    "lecture01-02/06_自动控制联系_教学补充.md": [("与自动控制的一个连接", ["13_control_coordinates"])],
    "lecture03/01_线性映射复习.md": [("1. 保持线性组合", ["11_linearity"])],
    "lecture03/02_矩阵表示与映射空间.md": [("1. 一列", ["06_matrix_columns"]), ("4. 映射本身", ["14_map_space"])],
    "lecture03/03_换基与矩阵等价.md": [("1. 先固定", ["12_basis_change_map"])],
    "lecture03/04_同构.md": [("2. 同构保留", ["09_isomorphism"])],
    "lecture03/05_核与像及秩零度.md": [("1. 核在输入", ["07_kernel_projection"]), ("3. 秩、零度", ["08_rank_nullity"])],
    "lecture03/06_复合映射.md": [("3. 复合对应", ["10_composition"])],
    "lecture04/01_线性代数与多项式除法.md": [("四、欧氏除法", ["15_polynomial_division"])],
    "lecture04/02_多项式理想与因式分解.md": [("三、和取最大公因式", ["16_ideal_lattice"])],
    "lecture04/03_多项式矩阵与幺模变换.md": [("一、两种等价写法", ["17_polynomial_layers"]), ("四、幺模", ["18_unimodular"])],
    "lecture05/01_Smith标准形与不变多项式.md": [("三、为什么能够", ["19_smith_steps"]), ("四、用行列式因子", ["20_determinantal_divisors"])],
    "lecture05/02_初等因子与特征矩阵.md": [("二、如何恢复", ["21_factor_alignment"]), ("五、特征矩阵", ["35_characteristic_matrix"])],
    "lecture06/01_特征值与不变子空间.md": [("二、不变子空间", ["23_invariant_subspace"]), ("三、特征值、特征向量", ["22_eigen_directions"])],
    "lecture06/02_相似不变量与自然标准形.md": [("二、用特征矩阵", ["35_characteristic_matrix"]), ("三、列伴随矩阵", ["24_companion_cycle"])],
    "lecture07/01_复数与实数Jordan标准形.md": [("三、复 Jordan 块", ["25_jordan_blocks"]), ("四、实 Jordan 形", ["26_real_jordan"])],
    "lecture07/02_Jordan链与子空间分解.md": [("二、链的列顺序", ["27_jordan_chain"]), ("七、教学补充", ["28_nullity_staircase"])],
    "lecture08/01_最小多项式与第一分解.md": [("二、矩阵表示", ["29_minimal_vs_characteristic"]), ("四、第一分解", ["30_two_decompositions"])],
    "lecture08/02_循环子空间与第二分解.md": [("一、一个向量", ["31_cyclic_growth"]), ("三、第二分解", ["30_two_decompositions"]), ("四、平移算子", ["32_finite_difference"])],
}


def block(key, path):
    relative = Path(os.path.relpath(ROOT / "assets/diagrams" / f"{key}.png", path.parent)).as_posix()
    return (f"<!-- diagram:{key}:start -->\n\n"
            f"**图解 · {TITLES[key]}**\n\n"
            f"![{TITLES[key]}]({relative})\n\n"
            f"**读图：** {CAPTIONS[key]}\n\n"
            f"<!-- diagram:{key}:end -->")


def strip_generated(text):
    return re.sub(r"\n*<!-- diagram:[^:]+:start -->.*?<!-- diagram:[^:]+:end -->\n*", "\n\n", text, flags=re.S)


def insert_section(text, prefix, content):
    match = re.search(r"(?m)^## "+re.escape(prefix)+r"[^\n]*\n", text)
    if match is None:
        raise ValueError(f"Section not found: {prefix}")
    start = match.end()
    candidates = list(re.finditer(r"(?m)^## |^(?:---\s*\n+)?\[阅读导航", text[start:]))
    end = start+candidates[0].start() if candidates else len(text)
    return text[:end].rstrip()+"\n\n"+content+"\n\n"+text[end:].lstrip("\n")


def update_notes():
    # Prepare every mutation before saving, so a missing anchor cannot leave half
    # the notes edited.
    writes = {}
    paths = sorted((ROOT / "notes").glob("*/*.md"))
    for path in paths:
        text = strip_generated(path.read_text())
        key = path.relative_to(ROOT / "notes").as_posix()
        if key in ROUTES:
            for section, figures in ROUTES[key]:
                text = insert_section(text, section, "\n\n".join(block(f, path) for f in figures))
        else:
            if key.startswith("lecture09/"):
                figure = "36_inner_product_gram"
            elif key.startswith("lecture10/"):
                figure = "39_normal_schur"
            else:
                figure = "33_course_map" if path.name.startswith("00_") else "34_problem_routes"
            pos = re.search(r"(?m)^## ", text)
            end = pos.start() if pos else len(text)
            text = text[:end].rstrip()+"\n\n"+block(figure,path)+"\n\n"+text[end:].lstrip("\n")
        writes[path] = text.rstrip()+"\n"
    assert set(ROUTES) <= {p.relative_to(ROOT / "notes").as_posix() for p in paths}
    for path, text in writes.items():
        path.write_text(text)
    return paths


def write_index():
    cn = ROOT / "notes/中文精简版"
    chunks = [
        "# 线性代数图解索引\n\n",
        "按章节查图，也可以直接打开正文，在相应小节边读边看。几何图使用二维或三维的具体例子；矩阵色块、指数格和链图保留各自的代数关系。图中颜色区分方向、根或分组，具体含义见每张图的读图说明。\n\n",
        "[中文讲义总目录](中文精简版/00_阅读导航.md) · [仓库首页](../README.md)\n\n",
        "## 按中文版章节查图\n\n| 章节 | 图解主题 |\n| --- | --- |\n",
    ]
    for path in sorted(cn.glob("*.md")):
        if "中文精简版/" + path.name not in ROUTES:
            continue
        topics = [TITLES[f] for _, ids in ROUTES["中文精简版/"+path.name] for f in ids]
        chunks.append(f"| [{path.read_text().splitlines()[0][2:]}](中文精简版/{path.name}) | {'；'.join(topics)} |\n")
    chunks.append(f"\n## 全部图解\n\n以下为 {len(TITLES)} 张图。PNG 直接显示；矢量版可放大查看。\n\n")
    for key in TITLES:
        chunks.append(f"### {key[:2]} {TITLES[key]}\n\n")
        chunks.append(f"![{TITLES[key]}](../assets/diagrams/{key}.png)\n\n")
        chunks.append(f"{CAPTIONS[key]}\n\n[查看矢量版](../assets/diagrams/{key}.svg)\n\n")
    (ROOT/"notes/图解索引.md").write_text("".join(chunks).rstrip()+"\n")


def check():
    paths = sorted((ROOT / "notes").glob("*/*.md"))
    errors = []
    for path in paths:
        text=path.read_text()
        if not re.search(r"!\[[^\]]+\]\(", text):
            errors.append(f"Missing illustration: {path}")
        starts=re.findall(r"<!-- diagram:([^:]+):start -->",text)
        ends=re.findall(r"<!-- diagram:([^:]+):end -->",text)
        if starts != ends or len(starts) != len(set(starts)):
            errors.append(f"Invalid diagram blocks: {path}")
    for path in [ROOT/"README.md", *sorted((ROOT/"notes").rglob("*.md"))]:
        for target in re.findall(r"!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)", path.read_text()):
            target=target.strip("<>").split("#",1)[0]
            if target and "://" not in target and not (path.parent/target).exists():
                errors.append(f"Broken local link: {path} -> {target}")
    for key in TITLES:
        for suffix in [".png",".svg"]:
            path=ROOT/"assets/diagrams"/(key+suffix)
            if not path.is_file():
                errors.append(f"Missing asset: {path}")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Checked {len(paths)} note files, {len(ROUTES)} body chapters, {len(TITLES)} diagram pairs and all local links.")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="Validate without editing")
    args=parser.parse_args()
    if not args.check:
        update_notes()
        write_index()
    check()


if __name__ == "__main__":
    main()
