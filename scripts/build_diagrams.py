#!/usr/bin/env python3
"""Build the teaching diagrams: python3 scripts/build_diagrams.py.

Dependencies: matplotlib, numpy, Pillow. Outputs PNG for Markdown readers and
self-contained SVG for zooming. All coordinates and matrix examples are editable.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path
import re
import textwrap
import unicodedata

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import MathTextParser
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
import numpy as np
from diagram_details import DETAILS
from diagram_english import ENGLISH, LABEL_TERMS
from math_typography import typeset_inline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"
BACKGROUND = "#000000"
SURFACE = "#10151D"
INK = "#F4F7FB"
MUTED = "#B5C1D2"
BLUE = "#73B7FF"
TEAL = "#5EEAD4"
ORANGE = "#FFC66D"
PURPLE = "#C4A1FF"
RED = "#FF8196"
LINE = "#303A49"
# Keep highlighted labels bright on dark tinted cells and cards.
HIGHLIGHT_FILLS = {
    BLUE: "#162C45", TEAL: "#10352F", ORANGE: "#3B2B14",
    PURPLE: "#2E2044", RED: "#3C1E28", MUTED: "#1F2835",
}
plt.rcParams.update({
    "font.family": ["Noto Sans CJK JP", "DejaVu Sans"],
    "font.size": 14, "text.color": INK, "axes.labelcolor": INK,
    "axes.titlecolor": INK, "axes.unicode_minus": False,
    "figure.facecolor": BACKGROUND, "axes.facecolor": BACKGROUND,
    "axes.edgecolor": LINE, "xtick.color": MUTED, "ytick.color": MUTED,
    "svg.fonttype": "path", "savefig.facecolor": BACKGROUND,
    "mathtext.fontset": "cm",
})
BUILDERS = {}
TITLES = {}
_MATH_PARSER = MathTextParser("path")


@lru_cache(maxsize=512)
def math_token_width(token):
    """Estimate formula width in Chinese-character units, not TeX source length."""
    font_size = 13.2
    result = _MATH_PARSER.parse(token, dpi=100, prop=FontProperties(size=font_size))
    return result.width / (font_size * 100 / 72)

def wrap_text(text, width=62):
    """Wrap CJK prose without splitting inline math expressions."""
    lines, line, used = [], "", 0
    for token in re.findall(r"\$[^$]+\$|\n|[A-Za-z0-9_]+|.", text):
        if token == "\n":
            lines.append(line.rstrip()); line, used = "", 0
            continue
        weight = (math_token_width(token) if token.startswith("$") and token.endswith("$")
                  else sum(1 if unicodedata.east_asian_width(c) in "WF" else .52 for c in token))
        if used+weight > width and line and token not in "，。！？；：、）】」』":
            lines.append(line.rstrip()); line, used = "", 0
        line += token
        used += weight
    if line:
        lines.append(line.rstrip())
    return "\n".join(lines)


def diagram(key, title):
    def register(fn):
        BUILDERS[key] = fn
        TITLES[key] = title
        return fn
    return register


def canvas(title, subtitle, height=6.5):
    fig = plt.figure(figsize=(12, height), facecolor=BACKGROUND)
    fig.text(.045, .947, title, fontsize=23, weight="bold", va="top")
    fig.text(.045, .878, wrap_text(subtitle), fontsize=12.5, color=MUTED, va="top")
    ax = fig.add_axes([.035, .105, .93, .70])
    ax.set(xlim=(-.2, 12.2), ylim=(-.1, 6.1))
    ax.axis("off")
    return fig, ax


def note(fig, text):
    fig.text(.045, .035, wrap_text(text), fontsize=12.5, color=MUTED, va="bottom")


def label(ax, x, y, text, size=15, color=INK, ha="center", va="center", **kw):
    return ax.text(x, y, text, fontsize=size, color=color, ha=ha, va=va, **kw)


def box(ax, x, y, w, h, text="", color=BLUE, fill=SURFACE, size=15, lw=1.3):
    if text and fill == color:
        fill = HIGHLIGHT_FILLS.get(color, SURFACE)
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                       facecolor=fill, edgecolor=color, linewidth=lw)
    ax.add_patch(p)
    if text:
        label(ax, x+w/2, y+h/2, text, size=size, color=color)
    return p


def arrow(ax, a, b, color=MUTED, text="", bend=0, size=18, lw=1.8):
    p = FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=size, linewidth=lw,
                        color=color, connectionstyle=f"arc3,rad={bend}")
    ax.add_patch(p)
    if text:
        x, y = (np.array(a)+np.array(b))/2
        label(ax, x, y+.24, text, size=12, color=color)
    return p


def matrix(ax, x, y, rows, cell=.6, highlights=None, size=18):
    """Draw a matrix whose origin is its bottom-left cell."""
    m, n = len(rows), len(rows[0])
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            xx, yy = x+j*cell, y+(m-1-i)*cell
            color = (highlights or {}).get((i, j))
            ax.add_patch(Rectangle((xx, yy), cell, cell,
                         facecolor=HIGHLIGHT_FILLS.get(color, color) if color else SURFACE,
                         edgecolor=BACKGROUND, linewidth=2))
            label(ax, xx+cell/2, yy+cell/2, str(text), size=size,
                  color=color or INK)
    for xx, sign in [(x-.10, -1), (x+n*cell+.10, 1)]:
        ax.plot([xx-sign*.09, xx, xx, xx-sign*.09],
                [y, y, y+m*cell, y+m*cell], color=INK, lw=1.5)
    return n*cell, m*cell


def plot_axis(fig, rect, limits=(-1, 5, -1, 4)):
    ax = fig.add_axes(rect)
    ax.set(xlim=limits[:2], ylim=limits[2:], aspect="equal")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_position("zero")
    ax.spines[["bottom", "left"]].set_color(LINE)
    ax.tick_params(labelsize=10, colors=MUTED, length=0, pad=4)
    ax.grid(color=LINE, alpha=.7, lw=.7)
    ax.set_axisbelow(True)
    return ax


def vector(ax, end, start=(0, 0), color=BLUE, text=None, offset=(.1, .12)):
    arrow(ax, start, end, color, size=18, lw=2.3)
    if text:
        label(ax, end[0]+offset[0], end[1]+offset[1], text, 13, color, ha="left")


@diagram("01_algebra_rules", "群、环、域：规则是逐步加上去的")
def algebra_rules():
    fig, ax = canvas(TITLES["01_algebra_rules"], "群先描述一种运算；环把加法群与乘法放在一起；域允许除以非零标量。")
    box(ax, .3, 3.65, 3.2, 1.45, "群：一种运算\n结合律＋单位元＋逆元", BLUE, size=16)
    box(ax, 4.15, 3.65, 3.2, 1.45, "环：两种运算\n加法交换群＋结合的乘法\n满足左右分配律", TEAL, size=14)
    box(ax, 8.0, 3.65, 3.6, 1.45, "域：可用作标量\n乘法交换＋非零可逆", PURPLE, size=16)
    arrow(ax, (3.55, 4.4), (4.05, 4.4))
    arrow(ax, (7.45, 4.4), (7.9, 4.4))
    label(ax, 1.9, 2.9, r"例如 $(\mathbb{Z},+)$", 17, BLUE)
    label(ax, 5.75, 2.9, r"例如 $\mathbb{Z}$、$\mathbb{F}[\lambda]$", 17, TEAL)
    label(ax, 9.8, 2.9, r"例如 $\mathbb{Q},\mathbb{R},\mathbb{C}$", 17, PURPLE)
    box(ax, .65, .6, 4.8, 1.3, "加法逆元：a + (−a) = 0\n群的运算不一定是乘法", BLUE, size=15)
    box(ax, 6.25, .6, 4.8, 1.3, "乘法逆元：a · a⁻¹ = 1，a ≠ 0\n多项式 λ 的倒数不是多项式", PURPLE, size=15)
    note(fig, "图中箭头表示增加运算或规则，不是把只含一种运算的群直接当作环的子集；环沿用课件允许无乘法单位元的约定。")
    return fig


@diagram("02_linear_combination", "线性组合：先缩放，再首尾相接")
def linear_combination():
    fig, _ = canvas(TITLES["02_linear_combination"], "同一套加法与数乘，既适用于箭头，也适用于多项式和矩阵。")
    a = plot_axis(fig, [.07, .20, .40, .55], (-.5, 4, -.5, 3))
    vector(a, (2, 0), color=BLUE, text=r"$2u$")
    vector(a, (3, 2), (2, 0), TEAL, r"$v$", (-.15, .15))
    vector(a, (3, 2), color=PURPLE, text=r"$2u+v$", offset=(-.1, -.5))
    a.plot([1, 1], [0, 1], alpha=0)
    a.set_title(r"$u=(1,0),\quad v=(1,2)$", fontsize=15, pad=14)
    b = fig.add_axes([.54, .22, .41, .52]); b.set(xlim=(0, 5), ylim=(0, 5)); b.axis("off")
    label(b, 2.5, 4.55, "第三个方向其实已被前两个解释", 16)
    vector(b, (2.1, 1), (.6, 1), BLUE, r"$v_1$", (.12, .12))
    vector(b, (.6, 2.6), (.6, 1), TEAL, r"$v_2$", (-.4, .3))
    vector(b, (2.1, 2.6), (.6, 1), PURPLE, r"$v_3$", (.2, .1))
    b.plot([2.1, 2.1, .6], [1, 2.6, 2.6], "--", color=LINE)
    label(b, 2.5, .25, r"$v_1+v_2-v_3=0$：三者相关", 16, PURPLE)
    note(fig, "读图：三个向量两两不平行，也可能整体相关。基需要的是没有冗余的生成方向。")
    return fig


@diagram("03_subspace_affine", "过原点还不够，还必须对线性组合封闭")
def subspace_affine():
    fig, _ = canvas(TITLES["03_subspace_affine"], "把“是不是子空间”画成三种集合：直线、平移直线、两根坐标轴的并。")
    for i, title in enumerate(["是子空间：x + y = 0", "不是：x + y = 1", "不是：两根坐标轴的并"]):
        a = plot_axis(fig, [.055+i*.32, .22, .27, .53], (-2, 2, -2, 2))
        t=np.linspace(-2,2,100)
        if i<2:
            a.plot(t, -t+i, color=TEAL if i==0 else ORANGE, lw=3)
            a.scatter([0], [0], c=TEAL if i==0 else RED, s=55, zorder=5)
        else:
            a.axhline(0, color=BLUE, lw=3); a.axvline(0, color=TEAL, lw=3)
            a.scatter([1, 0], [0, 1], color=[BLUE,TEAL], s=60, zorder=6)
            a.scatter([1],[1], marker="x", color=RED, s=90, zorder=7)
            a.plot([1,1,0],[0,1,1],"--",color=RED,lw=1.2)
        a.set_title(title, fontsize=13, pad=12)
    note(fig, "左：含零向量且封闭。中：不含零向量。右：含零向量，但 (1,0) + (0,1) = (1,1) 跑出了集合。")
    return fig


@diagram("04_basis_coordinates", "换基：同一支箭头，换一套刻度")
def basis_coordinates():
    fig, _ = canvas(TITLES["04_basis_coordinates"], r"$v=(4,2)$；旧基 $B=(e_1,e_2)$；新基 $C=((1,1),(1,-1))$。")
    for i in range(2):
        a=plot_axis(fig,[.07+i*.49,.20,.40,.55],(-1,5,-2,5))
        if i==0:
            a.plot([4,4,0],[0,2,2],"--",color=BLUE)
            vector(a,(1,0),color=BLUE,text=r"$e_1$",offset=(.05,-.45))
            vector(a,(0,1),color=TEAL,text=r"$e_2$")
        else:
            for k in range(-4,6):
                a.plot([-3,6],[-3+k,6+k],color=LINE,lw=.7)
                a.plot([-3,6],[3+k,-6+k],color=LINE,lw=.7)
            vector(a,(3,3),color=BLUE,text=r"$3c_1$",offset=(-.8,.2))
            vector(a,(4,2),(3,3),TEAL,r"$c_2$",(.05,-.45))
        vector(a,(4,2),color=PURPLE,text=r"$v$",offset=(.1,.1))
        a.set_title(r"$[v]_B=(4,2)^{\mathsf{T}}$" if i==0 else r"$[v]_C=(3,1)^{\mathsf{T}}$",fontsize=17,pad=12)
    note(fig, r"先写 $C=BP$，再写 $[v]_B=P[v]_C$；变的是系数，重组后仍得到同一个向量。")
    return fig


@diagram("05_sum_direct_sum", "并只收集已有向量，和还要收集相加的结果")
def sum_direct_sum():
    fig, ax=canvas(TITLES["05_sum_direct_sum"], r"$U$ 为横轴，$W$ 为纵轴；两条不同直线的交为零，所以本例的和是直和。")
    a=plot_axis(fig,[.06,.21,.39,.54],(-.5,3.5,-.5,3.5))
    a.axhline(0,color=BLUE,lw=4); a.axvline(0,color=TEAL,lw=4)
    vector(a,(2,0),color=BLUE,text=r"$u$",offset=(.1,-.35))
    vector(a,(0,2),color=TEAL,text=r"$w$")
    vector(a,(2,2),color=PURPLE,text=r"$u+w$")
    a.plot([2,2,0],[0,2,2],"--",color=PURPLE)
    a.set_title(r"$U\cup W$ 只有两根轴；$U+W$ 是全平面",fontsize=14,pad=12)
    box(ax,6.0,3.55,5.45,1.2,"交 U ∩ W = {0}\n没有可在两边重复计入的方向",TEAL,size=15)
    box(ax,6.0,1.75,5.45,1.2,"直和 U ⊕ W\n每个向量只有一种 u + w 分法",PURPLE,size=15)
    label(ax,8.7,.7,r"$2=1+1-0$",22,PURPLE)
    note(fig, "直和强调分解唯一；补空间不要求垂直。一般和空间的维数要减去交空间的维数，避免重复计数。")
    return fig


@diagram("06_matrix_columns", "矩阵的每一列，就是一个基方向被送到哪里")
def matrix_columns():
    fig,ax=canvas(TITLES["06_matrix_columns"], r"例：A 的两列为 (1,0)、(1,2)，于是 $Ae_1=(1,0)$，$Ae_2=(1,2)$。")
    a=plot_axis(fig,[.055,.24,.33,.48],(-.4,2,-.4,2.5))
    vector(a,(1,0),color=BLUE,text=r"$e_1$",offset=(.1,-.3))
    vector(a,(0,1),color=TEAL,text=r"$e_2$")
    vector(a,(1,1),color=PURPLE,text=r"$x=e_1+e_2$",offset=(.1,.1))
    a.set_title("输入：按基方向拆开",fontsize=15,pad=15)
    b=plot_axis(fig,[.61,.24,.33,.48],(-.4,3,-.4,2.5))
    vector(b,(1,0),color=BLUE,text=r"$Ae_1$",offset=(.1,-.3))
    vector(b,(1,2),color=TEAL,text=r"$Ae_2$",offset=(-.7,.18))
    vector(b,(2,2),color=PURPLE,text=r"$Ax$",offset=(.1,.1))
    b.plot([1,2],[0,2],"--",color=TEAL)
    b.set_title("输出：用原系数重组各列",fontsize=15,pad=15)
    arrow(ax,(4.7,3.0),(6.9,3.0),text=r"$x\mapsto Ax$")
    note(fig, r"$A(x_1e_1+x_2e_2)=x_1Ae_1+x_2Ae_2$：输入基决定列数，输出坐标决定行数。")
    return fig


@diagram("07_kernel_projection", "核是被压掉的方向，像是实际能到达的地方")
def kernel_projection():
    fig,ax=canvas(TITLES["07_kernel_projection"], r"投影 $T(x,y)=(x,0)$：纵向信息消失，所有输出都落在横轴。")
    a=plot_axis(fig,[.06,.23,.36,.5],(-2,2,-2,2))
    for x in [-1.2,0,1.2]:
        a.plot([x,x],[-1.6,1.6],color=TEAL if x==0 else LINE,lw=3 if x==0 else 1.5)
        a.scatter([x]*3,[-1,0,1],s=30,c=TEAL if x==0 else BLUE,zorder=5)
    a.set_title("输入：同一条竖线上的点",fontsize=15,pad=12)
    b=plot_axis(fig,[.60,.23,.34,.5],(-2,2,-2,2))
    b.axhline(0,color=BLUE,lw=4)
    b.scatter([-1.2,0,1.2],[0,0,0],s=90,c=[BLUE,TEAL,BLUE],zorder=5)
    b.set_title("输出：被压成横轴上的一点",fontsize=15,pad=12)
    arrow(ax,(4.9,3.15),(6.7,3.15),text="投影")
    label(ax,6,.2,r"$\ker T=\{(0,y)\},\quad \mathrm{im}\,T=\{(x,0)\}$",18)
    note(fig, "绿线整体映成原点，故它是核。核在输入空间，像在输出空间；图中两个平面代表映射的两端。")
    return fig


@diagram("08_rank_nullity", "秩零度：输入的自由方向去了哪里")
def rank_nullity():
    fig,ax=canvas(TITLES["08_rank_nullity"], r"示例 $T:\mathbb{R}^3\to\mathbb{R}^2$，$T(x,y,z)=(x,y)$。")
    for x,y,t,c in [(1,3.75,r"$e_1$",BLUE),(2.9,3.75,r"$e_2$",BLUE),
                    (1.95,1.0,r"$e_3$",ORANGE)]:
        box(ax,x,y,1.4,1.0,t,c,size=22)
    label(ax,3.1,5.35,"输入空间：3 个独立方向",18)
    box(ax,7.1,3.55,3.6,1.4,"像中保留 2 个方向\nrank T = 2",BLUE,size=17)
    box(ax,7.1,.75,3.6,1.4,"核中压掉 1 个方向\nnullity T = 1",ORANGE,size=17)
    arrow(ax,(4.45,4.25),(7,4.25),BLUE)
    arrow(ax,(3.5,1.5),(7,1.5),ORANGE)
    label(ax,3.7,2.75,"输入 3 = 核 1 + 像 2",19,PURPLE)
    note(fig, "这里数的是独立方向，不是矩阵里非零元素的个数；右边陪域的维数也不必等于秩。")
    return fig


@diagram("09_isomorphism", "同构：对象长得不同，线性信息仍能完整互译")
def isomorphism():
    fig,ax=canvas(TITLES["09_isomorphism"], r"$\Phi:\mathbb{R}_1[t]\to\mathbb{R}^2$，把 $a+bt$ 译成系数列 $(a,b)^{\mathsf{T}}$。")
    for y,l,r in [(4.7,"1","(1, 0)"),(3.2,"t","(0, 1)"),(1.7,"2 + 3t","(2, 3)")]:
        box(ax,.7,y-.45,3.1,.9,l,TEAL,size=21)
        box(ax,8.2,y-.45,3.1,.9,r,BLUE,size=21)
        arrow(ax,(4,y),(8,y),PURPLE,text="取系数")
    label(ax,6,.45,"逆操作：用同一组基重新组合",17,PURPLE)
    note(fig, "单射保证不把两个输入混成一个，满射保证不漏掉输出；同构还要保持加法与数乘。")
    return fig


@diagram("10_composition", "复合映射：操作从左到右，矩阵乘积右边先作用")
def composition():
    fig,ax=canvas(TITLES["10_composition"], r"$S(x,y)=(x,y,x+y)$；$T(a,b,c)=(a+c,b-c)$。")
    for x,text,c in [(.4,"输入\n(1, 2)",BLUE),(4.6,"中间结果\n(1, 2, 3)",TEAL),(8.8,"最终输出\n(4, −1)",PURPLE)]:
        box(ax,x,3.6,2.8,1.4,text,c,size=18)
    arrow(ax,(3.3,4.3),(4.45,4.3),text="S")
    arrow(ax,(7.5,4.3),(8.65,4.3),text="T")
    label(ax,6,2.65,r"$x\ \longmapsto\ Mx\ \longmapsto\ A(Mx)=(AM)x$",20)
    box(ax,.7,.65,4.65,1.05,"中间坐标采用同一组基\n才能直接写 AM",TEAL,size=16)
    box(ax,6.35,.65,4.95,1.05,"若中间换了基 C′ = CP\n先转换，再写 A′P⁻¹M",ORANGE,size=16)
    note(fig, "可从矩阵大小自查：(2×3)(3×2) 得到 2×2；倒过来得到 3×3，描述的是另一种复合。")
    return fig


@diagram("11_linearity", "线性性检验：两个计算路线必须到达同一点")
def linearity():
    fig,ax=canvas(TITLES["11_linearity"], "只检查 T(0)=0 还不够；加法和数乘都要保持。")
    box(ax,.6,3.7,2.6,1.0,"u、v",BLUE,size=22)
    box(ax,8.65,3.7,2.6,1.0,"u + v",BLUE,size=22)
    box(ax,.6,1.1,2.6,1.0,"T(u)、T(v)",TEAL,size=20)
    box(ax,8.65,1.1,2.6,1.0,"同一个输出？",PURPLE,size=18)
    arrow(ax,(3.35,4.2),(8.5,4.2),text="先相加")
    arrow(ax,(1.9,3.55),(1.9,2.25),TEAL)
    label(ax,.4,2.9,"分别作用 T",12,TEAL,ha="left")
    arrow(ax,(10,3.55),(10,2.25),PURPLE)
    label(ax,10.3,2.9,"作用 T",12,PURPLE,ha="left")
    arrow(ax,(3.35,1.6),(8.5,1.6),text="输出再相加")
    label(ax,6,.3,"反例 T(x)=x²：T(1+1)=4，但 T(1)+T(1)=2",15,RED)
    note(fig, r"把相加换成乘以任意标量 a，还要有 $T(au)=aT(u)$；两条性质合在一起才是保持线性组合。")
    return fig


@diagram("12_basis_change_map", "映射的换基：先翻译输入，再作用，最后翻译输出")
def basis_change_map():
    fig,ax=canvas(TITLES["12_basis_change_map"], r"新输入基 $B'=BP$，新输出基 $C'=CQ$；同一算子同步换基时才有 $Q=P$。")
    for x,y,t,c in [(.5,3.8,"新输入 x′",BLUE),(4.6,3.8,"旧输入 x",BLUE),
                    (8.7,3.8,"旧输出 y",TEAL),(8.7,1.0,"新输出 y′",PURPLE)]:
        box(ax,x,y,2.8,1.0,t,c,size=18)
    arrow(ax,(3.4,4.3),(4.45,4.3),text="P")
    arrow(ax,(7.5,4.3),(8.55,4.3),text="A")
    arrow(ax,(10.1,3.65),(10.1,2.15),PURPLE)
    label(ax,10.6,2.9,r"$Q^{-1}$",20,PURPLE)
    label(ax,4.3,1.5,r"$A'=Q^{-1}AP$",27,PURPLE)
    label(ax,4.3,.55,r"同步换基：$A'=P^{-1}AP$",18)
    note(fig, "等价允许输入和输出各换各的基；相似要求同一空间的输入、输出采用同一次换基。")
    return fig


@diagram("13_control_coordinates", "状态换坐标：同一条轨迹的两种读法")
def control_coordinates():
    fig,_=canvas(TITLES["13_control_coordinates"], r"取 $x=Pz$，P 的两列为 (1,0)、(1,1)，在 z 坐标中 $\dot z=\mathrm{diag}(-1,-2)z$。")
    t=np.linspace(0,3,150)
    zz=np.vstack([2*np.exp(-t),1.5*np.exp(-2*t)])
    xx=np.array([[1,1],[0,1]])@zz
    for i,(p,c,title) in enumerate([(xx,BLUE,"x 坐标：两个分量耦合"),(zz,TEAL,"z 坐标：各方向分别衰减")]):
        a=plot_axis(fig,[.065+i*.49,.22,.40,.54],(-.2,4,-.2,2))
        a.plot(*p,color=c,lw=3)
        a.scatter([p[0,0]],[p[1,0]],c=c,s=65)
        k=43
        arrow(a,p[:,k],p[:,k+15],c,size=20,lw=2.5)
        a.set_title(title,fontsize=14,pad=14)
    note(fig, r"两图中的每一时刻由 x=Pz 一一对应。常数可逆 P 改变矩阵表示，不改变系统；$A_x=P\,\mathrm{diag}(-1,-2)P^{-1}$。")
    return fig


@diagram("14_map_space", "映射也能当作向量：一个矩阵位置就是一个自由参数")
def map_space():
    fig,ax=canvas(TITLES["14_map_space"], r"例：从 $\mathbb{R}^3$ 到 $\mathbb{R}^2$ 的线性映射，用 2×3 矩阵表示；总共有 6 个独立参数。")
    matrix(ax,.75,2.6,[[r"$a_{11}$",r"$a_{12}$",r"$a_{13}$"],
                       [r"$a_{21}$",r"$a_{22}$",r"$a_{23}$"]],cell=.95,
           highlights={(0,1):TEAL},size=21)
    label(ax,2.15,1.75,"任意映射的矩阵",17)
    arrow(ax,(4.1,3.55),(6.1,3.55),text="挑一个位置")
    matrix(ax,6.5,2.6,[[0,1,0],[0,0,0]],cell=.95,highlights={(0,1):TEAL},size=21)
    label(ax,8,1.75,r"$E_{12}$：只把第二个输入方向送到第一个输出方向",13)
    label(ax,6,.55,r"$A=\sum_{i=1}^{2}\;\sum_{j=1}^{3}a_{ij}E_{ij},\qquad \dim\mathcal{L}(\mathbb{R}^3,\mathbb{R}^2)=6$",20)
    note(fig, "映射相加、数乘，对应矩阵逐项相加、数乘；固定输入和输出基以后，这个对应是一一的。")
    return fig


@diagram("15_polynomial_division", "多项式除法：每一步都消掉当前最高次项")
def polynomial_division():
    fig,ax=canvas(TITLES["15_polynomial_division"], "把“被除式 = 除式 × 商 + 余式”看成一块主体加一个收尾。")
    box(ax,.4,4.35,11.2,.9,r"$\lambda^3+2\lambda^2+\lambda+1=(\lambda^2+1)(\lambda+2)-1$",BLUE,size=23)
    stages=[
        (.5,r"$\lambda^3+2\lambda^2+\lambda+1$","当前被除式",BLUE),
        (4.6,r"$2\lambda^2+1$","减去 λ(λ²+1) 后",TEAL),
        (8.7,r"$-1$","再减去 2(λ²+1)",ORANGE),
    ]
    for x,t,cap,c in stages:
        box(ax,x,2.0,2.85,1.05,t,c,size=17)
        label(ax,x+1.42,1.45,cap,13,c)
    arrow(ax,(3.45,2.53),(4.45,2.53))
    arrow(ax,(7.55,2.53),(8.55,2.53))
    label(ax,6,.45,"商为 λ + 2；余式次数 0 < 除式次数 2",18,PURPLE)
    note(fig, "辗转相除重复同一件事：把“被除式、除式”换成“除式、余式”，直到余式为零。")
    return fig


@diagram("16_ideal_lattice", "理想的包含方向，与生成元的整除方向相反")
def ideal_lattice():
    fig,ax=canvas(TITLES["16_ideal_lattice"], r"在实系数域中取 $x=\lambda-1$，$y=\lambda+1$；比较 $p=x^2y$、$q=xy^2$ 的全部多项式倍数。")
    box(ax,.8,4.55,4.4,.85,r"$\langle xy\rangle=\langle p\rangle+\langle q\rangle$",TEAL,size=17)
    box(ax,.35,2.65,2.65,.85,r"$\langle x^2y\rangle$",BLUE,size=21)
    box(ax,3.25,2.65,2.65,.85,r"$\langle xy^2\rangle$",PURPLE,size=21)
    box(ax,.8,.75,4.4,.85,r"$\langle x^2y^2\rangle=\langle p\rangle\cap\langle q\rangle$",ORANGE,size=17)
    for a,b in [((1.65,3.55),(2.6,4.45)),((4.55,3.55),(3.4,4.45)),
                ((2.6,1.7),(1.65,2.55)),((3.4,1.7),(4.55,2.55))]:
        arrow(ax,a,b,size=15)
    box(ax,6.7,3.6,4.7,1.1,"向上：限制更少，集合更大\n生成元的指数取较小值",TEAL,size=16)
    box(ax,6.7,1.2,4.7,1.1,"向下：同时满足两边的倍数条件\n生成元的指数取较大值",ORANGE,size=16)
    note(fig, "箭头表示子集指向包含它的集合。和对应最大公因式，交对应最小公倍式；〈p〉包含的是所有多项式倍数。")
    return fig


@diagram("17_polynomial_layers", "多项式矩阵：按幂次拆成几层常数矩阵")
def polynomial_layers():
    fig,ax=canvas(TITLES["17_polynomial_layers"], r"同一个矩阵，既可以逐格读多项式，也可以按 $1,\lambda,\lambda^2$ 收集系数。")
    matrix(ax,.35,3.5,[[r"$1+\lambda$",r"$\lambda^2$"],[0,2]],.9,size=20)
    label(ax,3.1,4.35,"=",26)
    for x,rows,t,c in [(4.0,[[1,0],[0,2]],r"$A_0$",BLUE),
                       (6.7,[[1,0],[0,0]],r"$\lambda A_1$",TEAL),
                       (9.4,[[0,1],[0,0]],r"$\lambda^2A_2$",PURPLE)]:
        matrix(ax,x,3.65,rows,.72,size=19)
        label(ax,x+.72,2.95,t,20,c)
    label(ax,6.05,4.35,"+",24); label(ax,8.75,4.35,"+",24)
    box(ax,.8,.75,4.7,1.15,"最高幂次是 2，所以次数为 2\n最高次系数非零，但可以奇异",PURPLE,size=15)
    box(ax,6.2,.75,4.95,1.15,"乘法按卷积收集幂次\n矩阵系数的先后顺序不能交换",TEAL,size=15)
    note(fig, r"多项式矩阵的秩按子式是否恒零判断。例如 diag(λ,1) 的多项式秩为 2，但代入 λ=0 后数值秩为 1。")
    return fig


@diagram("18_unimodular", "幺模变换：做完以后，仍能用多项式完整撤销")
def unimodular():
    fig,ax=canvas(TITLES["18_unimodular"], "多项式环中不能随便除以 λ；能作为单位的只有非零常数。")
    label(ax,3,5.25,"允许：把一行的 λ 倍加到另一行",16,TEAL)
    matrix(ax,1.25,3.2,[[1,r"$\lambda$"],[0,1]],.75,highlights={(0,1):TEAL},size=21)
    label(ax,4.2,3.95,r"$\det U=1$",19,TEAL)
    matrix(ax,1.25,.9,[[1,r"$-\lambda$"],[0,1]],.75,highlights={(0,1):TEAL},size=21)
    label(ax,4.2,1.65,r"$U^{-1}$ 仍是多项式",15,TEAL)
    label(ax,9,5.25,"不允许：把整行乘 λ 当作可逆操作",16,ORANGE)
    matrix(ax,7.1,3.2,[[r"$\lambda$",0],[0,1]],.75,highlights={(0,0):ORANGE},size=21)
    label(ax,10.25,3.95,r"$\det H=\lambda$",19,ORANGE)
    matrix(ax,7.1,.9,[[r"$\frac{1}{\lambda}$",0],[0,1]],.75,highlights={(0,0):ORANGE},size=19)
    label(ax,10.3,1.65,"逆中出现分母",15,ORANGE)
    note(fig, "左边可以把同一个倍数减回去；右边要除以 λ，已经离开多项式矩阵。幺模的判据是行列式为非零常数。")
    return fig


@diagram("19_smith_steps", "史密斯化简：把可逆行列操作画成四帧")
def smith_steps():
    fig,ax=canvas(TITLES["19_smith_steps"], r"同一个例子看全过程；最终对角元为首一，并满足整除链 $1\mid\lambda^2$。")
    frames=[(.7,3.65,[[r"$\lambda$",1],[0,r"$\lambda$"]],"① 起点"),
            (7.3,3.65,[[1,r"$\lambda$"],[r"$\lambda$",0]],"② 交换两列"),
            (.7,.55,[[1,r"$\lambda$"],[0,r"$-\lambda^2$"]],"③ 第二行减去\nλ 倍第一行"),
            (7.3,.55,[[1,0],[0,r"$\lambda^2$"]],"④ 清空右上角\n再首一化")]
    for x,y,rows,cap in frames:
        matrix(ax,x,y,rows,.78,highlights={(0,0):TEAL,(1,1):PURPLE},size=21)
        label(ax,x+2.65,y+.75,cap,13,ha="left")
    arrow(ax,(5.5,4.4),(7.0,4.4))
    arrow(ax,(8.05,3.4),(1.5,2.4),bend=-.15)
    arrow(ax,(5.5,1.3),(7.0,1.3))
    note(fig, "第④帧的具体操作：c₂ ← c₂ − λc₁，然后 r₂ ← −r₂。每一步均可逆，不曾把整行除以非恒定多项式。")
    return fig


@diagram("20_determinantal_divisors", "行列式因子是累计乘积，不变多项式是相邻之商")
def determinantal_divisors():
    fig,ax=canvas(TITLES["20_determinantal_divisors"], r"例：$d_1=1,\ d_2=\lambda,\ d_3=\lambda(\lambda+1)$；从整除链向累计乘积逐层读取。")
    for i,(d,D,c) in enumerate([(r"$d_1=1$",r"$D_1=1$",BLUE),
                               (r"$d_2=\lambda$",r"$D_2=\lambda$",TEAL),
                               (r"$d_3=\lambda(\lambda+1)$",r"$D_3=\lambda^2(\lambda+1)$",PURPLE)]):
        x=.35+i*4.05
        box(ax,x,4.1,3.55,.9,d,c,size=19)
        box(ax,x,1.4,3.55,1.0,D,c,size=19)
        arrow(ax,(x+1.77,3.95),(x+1.77,2.6),c)
        label(ax,x+1.77,3.25,"累计乘到这一项",12,c)
    label(ax,6,.35,r"$D_0=1,\qquad d_k=\frac{D_k}{D_{k-1}}$",22)
    note(fig, "Dₖ 是全部 k 阶子式的首一最大公因式；一个非零子式不一定就是 Dₖ，但一个非零常数子式能直接给出 Dₖ=1。")
    return fig


@diagram("21_factor_alignment", "恢复不变多项式：各根排指数，左补零，再按列相乘")
def factor_alignment():
    fig,ax=canvas(TITLES["21_factor_alignment"], r"实系数多项式矩阵，秩 r=3；初等因子为 $(\lambda-1),(\lambda-1)^3,(\lambda+2)^2$。")
    label(ax,1.6,4.7,r"$\lambda-1$ 的指数",17,BLUE)
    label(ax,1.6,3.55,r"$\lambda+2$ 的指数",17,TEAL)
    for i,values in enumerate([[0,1,3],[0,0,2]]):
        for j,value in enumerate(values):
            c=BLUE if i==0 else TEAL
            box(ax,3.3+j*2.7,4.2-i*1.15,2.1,.9,str(value),c,
                fill=BACKGROUND if value==0 else SURFACE,size=24)
    for j,text in enumerate([r"$1$",r"$\lambda-1$",r"$(\lambda-1)^3(\lambda+2)^2$"]):
        x=4.35+j*2.7
        arrow(ax,(x,2.8),(x,2.1),PURPLE)
        label(ax,x,1.55,text,17 if j<2 else 14,PURPLE)
    label(ax,6,.45,r"$d_1\mid d_2\mid d_3$：每一种因子的指数都不下降",19)
    note(fig, "空缺补在左边，才能保证整除链。初等因子是按根拆开的信息，不变多项式是把各根在相同位置重新组合。")
    return fig


@diagram("22_eigen_directions", "特征向量：变换后仍沿着原来的直线")
def eigen_directions():
    fig,_=canvas(TITLES["22_eigen_directions"], r"示例 $A(x,y)=(2x+y,y)$；蓝色方向放大 2 倍，绿色方向保持不变，一般向量会转向。")
    a=plot_axis(fig,[.065,.19,.42,.58],(-2.2,4,-1,3))
    t=np.linspace(-2,4,50)
    a.plot(t,t*0,color=BLUE,alpha=.35,lw=2)
    a.plot(t,-t,color=TEAL,alpha=.35,lw=2)
    vector(a,(1,0),color=BLUE,text=r"$u$",offset=(-.05,-.4))
    vector(a,(2,0),color=BLUE,text=r"$Au=2u$",offset=(.08,.18))
    vector(a,(-1,1),color=TEAL,text=r"$Av=v$",offset=(-.8,.3))
    a.set_title("特征方向：只倍乘，不离开直线",fontsize=14,pad=12)
    b=plot_axis(fig,[.565,.19,.39,.58],(-.5,4,-1,3))
    vector(b,(1,1),color=ORANGE,text=r"$w$")
    vector(b,(3,1),color=RED,text=r"$Aw$")
    b.set_title("一般方向：w 与 Aw 不平行",fontsize=14,pad=12)
    note(fig, "特征值也可以为负或零：负值可能反向，零值会压成零向量。不能把“保持方向”误解为必须同向。")
    return fig


@diagram("23_invariant_subspace", "不变子空间：里面的向量变换后仍留在里面")
def invariant_subspace():
    fig,_=canvas(TITLES["23_invariant_subspace"], r"仍用 $A(x,y)=(2x+y,y)$；检查子空间的一组基的像，就能判断不变性。")
    for i in range(2):
        a=plot_axis(fig,[.06+i*.49,.22,.40,.54],(-.5,3,-.5,2.5))
        if i==0:
            a.axhline(0,color=BLUE,lw=4,alpha=.5)
            vector(a,(1,0),color=BLUE,text=r"$e_1$",offset=(-.2,-.45))
            vector(a,(2,0),color=TEAL,text=r"$Ae_1=2e_1$")
            a.set_title("横轴不变：像仍在横轴上",fontsize=14,pad=14)
        else:
            a.axvline(0,color=ORANGE,lw=4,alpha=.5)
            vector(a,(0,1),color=ORANGE,text=r"$e_2$",offset=(-.2,.25))
            vector(a,(1,1),color=RED,text=r"$Ae_2=(1,1)$",offset=(.15,.1))
            a.set_title("纵轴不变性不成立：像跑了出去",fontsize=14,pad=14)
    note(fig, "不变是 T(W)⊆W，不要求等号。更高维的不变空间允许内部方向相互混合，不必是一个特征空间。")
    return fig


@diagram("24_companion_cycle", "伴随矩阵：前几列负责接力，最后一列负责回收")
def companion_cycle():
    fig,ax=canvas(TITLES["24_companion_cycle"], r"若 $\psi(\lambda)=\lambda^3+2\lambda^2-\lambda+4$，则 $A^3v=-4v+Av-2A^2v$。")
    for x,t,c in [(.4,r"$v$",BLUE),(2.35,r"$Av$",TEAL),(4.3,r"$A^2v$",PURPLE)]:
        box(ax,x,3.9,1.45,.95,t,c,size=22)
    arrow(ax,(1.95,4.38),(2.2,4.38))
    arrow(ax,(3.9,4.38),(4.15,4.38))
    box(ax,.6,1.1,5.2,1.45,"再次作用 A，不增加新方向\nA³v = −4v + Av − 2A²v",ORANGE,size=17)
    arrow(ax,(5,3.75),(3.4,2.7),ORANGE)
    colors={(1,0):TEAL,(2,1):TEAL,(0,2):ORANGE,(1,2):ORANGE,(2,2):ORANGE}
    matrix(ax,8.0,2.0,[[0,0,-4],[1,0,1],[0,1,-2]],.92,colors,size=23)
    label(ax,9.4,5.15,"基 (v, Av, A²v) 下的矩阵",15)
    label(ax,9.4,1.1,"绿色：前两次接力\n橙色：线性关系的负系数",14)
    note(fig, "这个图假设 v、Av、A²v 独立。最后一列不是多项式系数直接照抄，而是由 ψ(A)v=0 移项得到。")
    return fig


@diagram("25_jordan_blocks", "若尔当色块：块的大小与块的个数是两件事")
def jordan_blocks():
    fig,ax=canvas(TITLES["25_jordan_blocks"], r"示例 $J=\mathrm{diag}(J_3(2),J_2(2))$；同一个根 2 有两块，不能合并成一块。")
    rows=[[2,1,0,0,0],[0,2,1,0,0],[0,0,2,0,0],[0,0,0,2,1],[0,0,0,0,2]]
    colors={(i,j):(BLUE if i<3 else TEAL) for i in range(5) for j in range(5)
            if (i<3 and j<3) or (i>=3 and j>=3)}
    colors.update({(0,1):ORANGE,(1,2):ORANGE,(3,4):ORANGE})
    matrix(ax,.7,1.15,rows,.78,colors,size=22)
    box(ax,6.25,3.85,4.9,1,"代数重数：3 + 2 = 5\n数的是该根占据的总维数",BLUE,size=16)
    box(ax,6.25,2.1,4.9,1,"几何重数：2\n数的是块数，也就是链头数",TEAL,size=16)
    box(ax,6.25,.35,4.9,1,"最大块长：3\n决定最小多项式中的最高指数",PURPLE,size=16)
    note(fig, "橙色的 1 把同一条链接起来；不同色块之间没有连接。所有块都为一阶，才可在复数域对角化。")
    return fig


@diagram("26_real_jordan", "一对共轭复块，配成一个维数翻倍的实块")
def real_jordan():
    fig,ax=canvas(TITLES["26_real_jordan"], r"$J_2(-1+i)$ 与 $J_2(-1-i)$ 都是二阶；配对后得到四阶实块。")
    matrix(ax,.5,3.5,[[r"$-1+i$",1],[0,r"$-1+i$"]],.83,size=17)
    matrix(ax,.5,.7,[[r"$-1-i$",1],[0,r"$-1-i$"]],.83,size=17)
    label(ax,3.5,4.35,"二阶复块",14,BLUE)
    label(ax,3.5,1.55,"共轭二阶复块",14,TEAL)
    arrow(ax,(4.6,3.0),(6.4,3.0),text="取实部、虚部")
    colors={(i,j):BLUE for i in range(2) for j in range(2)}
    colors.update({(i,j):TEAL for i in range(2,4) for j in range(2,4)})
    colors.update({(0,2):ORANGE,(1,3):ORANGE,(0,3):ORANGE,(1,2):ORANGE})
    matrix(ax,7.1,1.4,[[-1,1,1,0],[-1,-1,0,1],[0,0,-1,1],[0,0,-1,-1]],.83,colors,size=23)
    label(ax,8.75,.6,r"对角放 $R(-1,1)$，右上块放 $I_2$",15)
    note(fig, "实基按 (u₁,v₁,u₂,v₂) 排列，使用 R(a,b)=[[a,b],[-b,a]]；更换基的顺序会相应改变矩阵的外观。")
    return fig


@diagram("27_jordan_chain", "若尔当链：作用方向与基向量排列方向相反")
def jordan_chain():
    fig,ax=canvas(TITLES["27_jordan_chain"], r"例 $A=J_3(2)$，记 $N=A-2I$；N 每作用一次，就向链头退一步。")
    xs=[.25,3.2,6.15,9.1]
    for x,t,c in zip(xs,["0",r"$x_1=e_1$",r"$x_2=e_2$",r"$x_3=e_3$"],[MUTED,BLUE,TEAL,PURPLE]):
        box(ax,x,4.5,2.4,.9,t,c,size=20)
    for i in range(1,4):
        arrow(ax,(xs[i]-.1,4.95),(xs[i-1]+2.5,4.95),text="N")
    label(ax,6,4.05,"链头在左，链尾在右；列顺序 P = (x₁, x₂, x₃)",17)
    box(ax,.7,1.05,5.3,1.45,"Nx₁ = 0，Nx₂ = x₁，Nx₃ = x₂\n所以 Ax₂ = 2x₂ + x₁",BLUE,size=17)
    matrix(ax,8.0,.9,[[2,1,0],[0,2,1],[0,0,2]],.77,
           {(0,1):ORANGE,(1,2):ORANGE},size=22)
    label(ax,9.2,3.55,"前一向量出现在上一行",14,ORANGE)
    note(fig, "因此超对角线为 1。验证 AP=PJ 之后，还必须检查 P 的列独立；重复链头会让 P 不可逆。")
    return fig


@diagram("28_nullity_staircase", "核维数的台阶，能反推出每一条链有多长")
def nullity_staircase():
    fig,ax=canvas(TITLES["28_nullity_staircase"], r"同一特征值处有两条链，长度分别为 3、2；设 $h_k=\dim\ker(A-\rho I)^k$。")
    for row,m in enumerate([3,2]):
        label(ax,.75,4.65-row*1.15,f"链 {row+1}",14,ha="left")
        for j in range(m):
            box(ax,1.8+j*1.0,4.15-row*1.15,.83,.85,str(j+1),[BLUE,TEAL,ORANGE][j],size=20)
    label(ax,3.15,2.3,"Nᵏ 能杀掉每条链的前 k 格",14)
    label(ax,3.15,.95,"新增的格数：2、2、1、0\n就是长度至少 k 的块数",16,PURPLE)
    a=fig.add_axes([.60,.25,.33,.47])
    a.plot(range(5),[0,2,4,5,5],"o-",lw=3,color=PURPLE,markersize=8)
    a.set(xlim=(-.2,4.25),ylim=(-.2,5.8),xticks=range(5),yticks=range(6),xlabel="幂次 k",ylabel="核维数 hₖ")
    a.spines[["top","right"]].set_visible(False)
    a.grid(color=LINE,lw=.7)
    for k,h in enumerate([0,2,4,5,5]):
        a.annotate(str(h),(k,h),xytext=(0,11),textcoords="offset points",ha="center",color=PURPLE,fontsize=12)
    note(fig, "h₁ 给块数，最终稳定值给该根的代数重数；相邻增量为 2、2、1、0，所以恰好有一个三阶块、一个二阶块。")
    return fig


@diagram("29_minimal_vs_characteristic", "特征多项式把块长相加，最小多项式只取最大值")
def minimal_vs_characteristic():
    fig,ax=canvas(TITLES["29_minimal_vs_characteristic"], r"示例 $A=\mathrm{diag}(J_3(1),[1],J_2(2))$：同根处的多个块必须同时处理。")
    for y,m,t,c in [(4.7,3,"根 1 的第一块",BLUE),(3.5,1,"根 1 的第二块",BLUE),(2.3,2,"根 2 的一块",TEAL)]:
        label(ax,.15,y,t,12,ha="left")
        for j in range(m):
            box(ax,2.0+j*.65,y-.33,.55,.65,"",c,fill=c)
        label(ax,4.35,y,f"长度 {m}",13)
    box(ax,6.1,3.7,5.45,1.35,"特征多项式：总共占多少维\n" r"$\chi_A=(\lambda-1)^4(\lambda-2)^2$",BLUE,size=18)
    box(ax,6.1,1.35,5.45,1.35,"最小多项式：每个根最长的链\n" r"$m_A=(\lambda-1)^3(\lambda-2)^2$",PURPLE,size=18)
    label(ax,6,.35,"同根指数：特征多项式取和；最小多项式取最大值",17)
    note(fig, "分块矩阵的最小多项式取各块最小多项式的最小公倍式；只有各块对应多项式互素时，才可直接相乘。")
    return fig


@diagram("30_two_decompositions", "第一分解按根分组，第二分解按不变多项式分组")
def two_decompositions():
    fig,ax=canvas(TITLES["30_two_decompositions"], r"同一组链：根 1 有 $(x_1,x_2)$ 和 $(y_1)$；根 2 有 $(z_1)$。")
    label(ax,3,5.5,"第一分解：相同特征值放一起",17,BLUE)
    label(ax,9,5.5,"第二分解：组成循环空间",17,PURPLE)
    box(ax,.3,2.95,5.25,1.6,"",BLUE)
    for x,t in [(1,r"$x_1$"),(2.5,r"$x_2$"),(4,r"$y_1$")]:
        box(ax,x,3.35,1.1,.8,t,BLUE,fill=BLUE,size=20)
    box(ax,.3,.8,5.25,1.3,"",TEAL)
    box(ax,2.5,1.05,1.1,.8,r"$z_1$",TEAL,fill=TEAL,size=20)
    label(ax,3,2.55,r"$G_1$：3 维",14,BLUE)
    label(ax,3,.3,r"$G_2$：1 维",14,TEAL)
    box(ax,6.4,3.35,5.25,1.2,"",PURPLE)
    box(ax,8.5,3.55,1.1,.8,r"$y_1$",BLUE,fill=BLUE,size=20)
    box(ax,6.4,.8,5.25,1.55,"",PURPLE)
    for x,t,c in [(7.1,r"$x_1$",BLUE),(8.6,r"$x_2$",BLUE),(10.1,r"$z_1$",TEAL)]:
        box(ax,x,1.2,1.1,.8,t,c,fill=c,size=20)
    label(ax,9,2.9,r"$\psi_1=\lambda-1$：1 维",14,PURPLE)
    label(ax,9,.3,r"$\psi_2=(\lambda-1)^2(\lambda-2)$：3 维",14,PURPLE)
    note(fig, "右边的生成元可取 β₁=y₁、β₂=x₂+z₁；因为两根的局部最小多项式互素，β₂ 能生成蓝、绿两部分。")
    return fig


@diagram("31_cyclic_growth", "循环空间：让同一个向量反复经过 A")
def cyclic_growth():
    fig,ax=canvas(TITLES["31_cyclic_growth"], r"例 $A=\mathrm{diag}(J_2(1),[2])$，取 $v=(0,1,1)^{\mathsf{T}}$。")
    colors=[BLUE,TEAL,PURPLE]
    for i,(name,coords) in enumerate([(r"$v$","(0, 1, 1)"),(r"$Av$","(1, 1, 2)"),(r"$A^2v$","(2, 1, 4)")]):
        x=.55+i*4
        box(ax,x,3.7,2.9,1.3,name+"\n"+coords,colors[i],size=18)
        label(ax,x+1.45,3.05,f"累计独立方向：{i+1}",15,colors[i])
    arrow(ax,(3.55,4.35),(4.4,4.35),text="A")
    arrow(ax,(7.55,4.35),(8.4,4.35),text="A")
    box(ax,.75,.8,5.0,1.25,"P = (v, Av, A²v)，det P = −1\n三个方向独立，已生成整个空间",PURPLE,size=16)
    box(ax,6.3,.8,5.0,1.25,"A³v = 4A²v − 5Av + 2v\n再作用 A 也不增加新方向",ORANGE,size=16)
    note(fig, "循环空间的维数等于向量处最小多项式的次数；若改取特征向量 e₁，反复作用只沿一条直线，维数为 1。")
    return fig


@diagram("32_finite_difference", "有限差分：平移一次再相减，多项式就降一阶")
def finite_difference():
    fig,ax=canvas(TITLES["32_finite_difference"], r"示例步长 a=1；$\Delta f(t)=f(t+1)-f(t)$，取 $f_2(t)=\frac{t(t-1)}{2}$。")
    data=[[0,0,1,3,6],[0,1,2,3],[1,1,1],[0,0]]
    for i,values in enumerate(data):
        y=4.75-i*1.1
        label(ax,.3,y,["f₂","Δf₂","Δ²f₂","Δ³f₂"][i],15,ha="left")
        for j,value in enumerate(values):
            x=1.65+j*.95+i*.475
            box(ax,x,y-.32,.65,.65,str(value),[BLUE,TEAL,PURPLE,MUTED][i],size=19)
        label(ax,6.65,y,["二次","一次","常数","零"][i],12,MUTED)
    for y,t,c in [(4.4,r"$f_2=\frac{t(t-1)}{2}$",BLUE),(2.8,r"$f_1=t$",TEAL),(1.2,r"$f_0=1$",PURPLE)]:
        box(ax,7.3,y-.45,3.8,.9,t,c,size=21)
    arrow(ax,(9.2,3.8),(9.2,3.4),TEAL,text="")
    arrow(ax,(9.2,2.2),(9.2,1.8),PURPLE,text="")
    label(ax,11.4,3.6,"Δ",16,TEAL); label(ax,11.4,2.0,"Δ",16,PURPLE)
    note(fig, "左表每项等于上一行相邻两项“右减左”；右边的牛顿多项式恰满足 Δf₂=f₁、Δf₁=f₀、Δf₀=0，组成归一化若尔当链。")
    return fig


@diagram("33_course_map", "整套讲义的地图：先建立坐标，再看清算子的结构")
def course_map():
    fig,ax=canvas(TITLES["33_course_map"], "编号对应中文版正文；沿箭头从基础走向标准形与空间分解。")
    cards=[(.2,3.8,"01 运算与空间",BLUE),(3.25,3.8,"02 基与子空间",BLUE),
           (6.3,3.8,"03 线性映射",TEAL),(9.35,3.8,"04—05 多项式",TEAL),
           (9.35,1.0,"06—07 史密斯形\n初等因子",PURPLE),
           (6.3,1.0,"08—09 特征值\n自然标准形",PURPLE),
           (3.25,1.0,"10—11 若尔当块\n若尔当链",ORANGE),
           (.2,1.0,"12—13 最小多项式\n两种分解",ORANGE)]
    for x,y,t,c in cards:
        box(ax,x,y,2.45,1.2,t,c,size=15)
    for a,b in [((2.75,4.4),(3.1,4.4)),((5.8,4.4),(6.15,4.4)),
                ((8.85,4.4),(9.2,4.4)),((10.55,3.6),(10.55,2.4)),
                ((9.2,1.6),(8.85,1.6)),((6.15,1.6),(5.8,1.6)),((3.1,1.6),(2.75,1.6))]:
        arrow(ax,a,b)
    note(fig, "主线始终是同一个问题：选哪些向量作基，才能让线性作用更容易理解和计算？")
    return fig


@diagram("34_problem_routes", "做题先认对象，再选工具，最后验证")
def problem_routes():
    fig,ax=canvas(TITLES["34_problem_routes"], "四类问题用四种读法，避免把坐标列、抽象向量和多项式矩阵混在一起。")
    for x,y,title,text,c in [
        (.4,3.55,"① 求空间","解齐次方程、选独立方向\n检查维数与子空间条件",BLUE),
        (6.4,3.55,"② 求矩阵表示","逐列计算基向量的像\n检查输入、输出基与大小",TEAL),
        (.4,.6,"③ 求标准形","先构造 λI−A，再读因子\n检查块长、块数和总阶数",PURPLE),
        (6.4,.6,"④ 求换基与分解","按链或循环基组织列\n检查 AP=PN 与 P 可逆",ORANGE),
    ]:
        box(ax,x,y,5.1,1.8,"",c)
        label(ax,x+.25,y+1.37,title,19,c,ha="left")
        label(ax,x+.25,y+.6,text,16,ha="left")
    note(fig, "若只求一个向量的最小多项式，不能直接照抄全空间结果；若求整个矩阵相似，不能只比较特征多项式。")
    return fig


@diagram("35_characteristic_matrix", "研究常数矩阵的结构，先把它变成特征矩阵")
def characteristic_matrix():
    fig,ax=canvas(TITLES["35_characteristic_matrix"], r"同一个例子从 A 出发；史密斯形属于 $\lambda I-A$，不是常数矩阵 A 本身。")
    for x,rows,title,cell in [
        (.4,[[1,1],[0,1]],"常数矩阵 A",.8),
        (4.4,[[r"$\lambda-1$",-1],[0,r"$\lambda-1$"]],"特征矩阵 λI − A",.9),
        (9,[[1,0],[0,r"$(\lambda-1)^2$"]],"史密斯形",.95),
    ]:
        matrix(ax,x,3.2,rows,cell,size=17)
        label(ax,x+cell,5.35,title,15)
    arrow(ax,(2.25,4.05),(4.1,4.05),text="构造")
    arrow(ax,(6.5,4.05),(8.7,4.05),text="幺模等价")
    box(ax,.8,.7,4.9,1.15,"两个不变多项式：1、(λ−1)²\n只有一个初等因子 (λ−1)²",BLUE,size=16)
    box(ax,6.3,.7,4.9,1.15,"因此是一个二阶若尔当块\n不是两个一阶块",PURPLE,size=16)
    note(fig, "λI−A 在有理函数域上满秩；代入特征值 λ=1 后数值矩阵奇异，这两种“秩”不能混为一谈。")
    return fig


def detail_panel_height(key, dpi):
    """Size both cards to the taller set of bilingual statements."""
    measurement = plt.figure(figsize=(12, 5), dpi=dpi)
    ax = measurement.add_axes([0, 0, 1, 1])
    ax.axis("off")
    cards = []
    for (_, statements), (_, en_statements) in zip(DETAILS[key], ENGLISH[key][3]):
        if len(statements) != len(en_statements):
            raise ValueError(f"{key}: Chinese and English statement counts differ")
        rows = []
        for statement, en_statement in zip(statements, en_statements):
            zh = ax.text(0, 1, typeset_inline("· " + wrap_text(statement, 25).replace("\n", "\n  ")),
                         color=INK, fontsize=13.2, va="top", linespacing=1.35)
            en = ax.text(0, 1, textwrap.fill(en_statement, 57, break_long_words=False),
                         fontfamily="DejaVu Sans", fontsize=10.5, va="top", linespacing=1.24)
            rows.append((zh, en))
        cards.append(rows)
    measurement.canvas.draw()
    renderer = measurement.canvas.get_renderer()
    card_heights = []
    for rows in cards:
        content = sum((zh.get_window_extent(renderer).height + en.get_window_extent(renderer).height) / dpi
                      + (.055 if en.get_text() else 0) for zh, en in rows)
        card_heights.append(content + .13 * max(0, len(rows) - 1))
    plt.close(measurement)
    # Account for panel border, heading, bottom inset and a small rendering margin.
    return max(3.15, .51 + .87 + .20 + max(card_heights) + .06)


def add_details(fig, key):
    """Add paired English text and expand the canvas without shrinking the artwork."""
    width, old_height = fig.get_size_inches()
    extra_height = detail_panel_height(key, fig.dpi)
    note_extra = .60
    header_extra = 1.22
    height = old_height + extra_height + note_extra + header_extra
    en_title, en_subtitle, en_note, en_panels = ENGLISH[key]
    fig.set_size_inches(width, height, forward=True)
    fig._main_axes = list(fig.axes)
    for ax in fig._main_axes:
        bounds = ax.get_position(original=True)
        ax.set_position([bounds.x0, (bounds.y0 * old_height + extra_height + note_extra) / height,
                         bounds.width, bounds.height * old_height / height])
    original_texts = list(fig.texts)
    if len(original_texts) != 3:
        raise ValueError(f"{key}: expected title, subtitle and note")
    for index, text in enumerate(original_texts):
        x, y = text.get_position()
        header_shift = (header_extra if index == 0 else .65 if index == 1 else 0)
        text.set_position((x, (y * old_height + extra_height + note_extra + header_shift) / height))

    def english_text(text, x, y, size=10.5, **kwargs):
        item = fig.text(x, y / height, text, fontfamily="DejaVu Sans",
                        fontsize=size, color=kwargs.pop("color", MUTED), **kwargs)
        item._english_translation = True
        return item

    english_text(en_title, .045, old_height * .947 + extra_height + note_extra + header_extra - .36,
                 size=12, color=BLUE, va="top")
    english_text(textwrap.fill(en_subtitle, 115, break_long_words=False), .045,
                 old_height * .878 + extra_height + note_extra + .65 - .37,
                 size=10.8, va="top", linespacing=1.15)
    label_terms = fig.text(.045, (old_height * .878 + extra_height + note_extra + .65 - .59) / height,
                           "图中术语 / Key labels: " + LABEL_TERMS[key],
                           fontfamily=["Noto Sans CJK JP", "DejaVu Sans"], fontsize=10.1,
                           color=TEAL, va="top")
    label_terms._english_translation = True
    english_text(textwrap.fill(en_note, 125, break_long_words=False), .045,
                 extra_height + .70, size=10.2, va="top", linespacing=1.15)

    panel = fig.add_axes([0, 0, 1, extra_height / height])
    panel.set(xlim=(0, width), ylim=(0, extra_height))
    panel.axis("off")
    panel.plot([.48, width - .48], [extra_height - .18, extra_height - .18], color=LINE, lw=1)
    fig._detail_regions = []
    fig._detail_layout = []
    for index, ((heading, statements), (en_heading, en_statements)) in enumerate(zip(DETAILS[key], en_panels)):
        if len(statements) != len(en_statements):
            raise ValueError(f"{key}: Chinese and English statement counts differ")
        x = .48 + index * 5.62
        y, card_width, card_height = .18, 5.42, extra_height - .51
        panel.add_patch(FancyBboxPatch(
            (x, y), card_width, card_height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=SURFACE, edgecolor=LINE, linewidth=1,
        ))
        heading_text = panel.text(x + .22, y + card_height - .18, heading,
                                  color=BLUE if index == 0 else TEAL,
                                  fontsize=14, weight="bold", va="top")
        heading_en = panel.text(x + .22, y + card_height - .46, en_heading,
                                color=BLUE if index == 0 else TEAL,
                                fontfamily="DejaVu Sans", fontsize=10.2, va="top")
        heading_en._english_translation = True
        body_rows = []
        for statement, en_statement in zip(statements, en_statements):
            zh = panel.text(x + .22, y + card_height - .87,
                            "· " + wrap_text(statement, 25).replace("\n", "\n  "),
                            color=INK, fontsize=13.2, va="top", linespacing=1.35)
            en = panel.text(x + .37, y + card_height - .87,
                            textwrap.fill(en_statement, 57, break_long_words=False),
                            color=MUTED, fontfamily="DejaVu Sans", fontsize=10.5,
                            va="top", linespacing=1.24)
            en._english_translation = True
            body_rows.append((zh, en))
        fig._detail_layout.append((panel, body_rows, y + .20, y + card_height - .87))
        fig._detail_regions.extend((t, panel, (x, y, x + card_width, y + card_height))
                                   for t in (heading_text, heading_en, *(t for row in body_rows for t in row)))
    fig._header_extra = header_extra


def balance_layout(fig, key):
    """Center the main visual and space each card's items by their drawn height."""
    renderer = fig.canvas.get_renderer()
    # Measure actual bright artwork, rather than the extent of invisible axes.
    # The title/subtitle and the explanatory note are outside this vertical band.
    rgba = np.asarray(fig.canvas.buffer_rgba())
    dpi = fig.dpi
    header_extra = fig._header_extra
    upper, lower = round((1.08 + header_extra) * dpi), round((5.86 + header_extra) * dpi)
    ink = np.max(rgba[upper:lower, :, :3], axis=2) > 100
    rows = np.flatnonzero(np.count_nonzero(ink, axis=1) > 2)
    if rows.size:
        first, last = rows[0] + upper, rows[-1] + upper
        target = ((1.13 + 5.84) / 2 + header_extra) * dpi
        shift = target - (first + last) / 2
        shift = np.clip(shift, (1.08 + header_extra) * dpi - first,
                        (5.86 + header_extra) * dpi - last)
        figure_shift = -shift / fig.bbox.height
        for ax in fig._main_axes:
            bounds = ax.get_position(original=True)
            ax.set_position([bounds.x0, bounds.y0 + figure_shift, bounds.width, bounds.height])

    # Place individual statements between consistent top/bottom insets, taking
    # fractions, matrices and wrapped lines into account when measuring height.
    for ax, rows, bottom, top in fig._detail_layout:
        row_heights = [(zh.get_window_extent(renderer).height / dpi,
                        en.get_window_extent(renderer).height / dpi if en.get_text() else 0)
                       for zh, en in rows]
        inset = .055
        heights = [zh_height + (en_height + inset if en_height else 0)
                   for zh_height, en_height in row_heights]
        available = top - bottom
        spare = available - sum(heights)
        if spare < -0.005:
            raise ValueError(f"{key}: supplementary statements exceed available height")
        gap = min(.17, max(0, spare) / max(1, len(rows) - 1))
        cursor = top - max(0, spare - gap * max(0, len(rows) - 1)) / 2
        for (zh, en), (zh_height, _), height in zip(rows, row_heights, heights):
            zh.set_y(cursor)
            en.set_y(cursor - zh_height - inset)
            cursor -= height + gap


def save_figure(key):
    fig = BUILDERS[key]()
    add_details(fig, key)
    # Keep Chinese in the CJK font while setting every inline formula in mathtext.
    for item in fig.findobj(matplotlib.text.Text):
        if item.get_text() and not getattr(item, "_english_translation", False):
            item.set_text(typeset_inline(item.get_text()))
    fig.canvas.draw()
    balance_layout(fig, key)
    fig.canvas.draw()
    # Every visible label must fit inside the exported canvas.
    bounds = fig.bbox
    for text in fig.findobj(matplotlib.text.Text):
        if not text.get_visible() or not text.get_text() or text.axes is not None and not text.axes.get_visible():
            continue
        extent = text.get_window_extent(fig.canvas.get_renderer())
        if extent.x0 < -2 or extent.y0 < -2 or extent.x1 > bounds.x1+2 or extent.y1 > bounds.y1+2:
            raise ValueError(f"{key}: label outside canvas: {text.get_text()!r}")
    for text, ax, (x0, y0, x1, y1) in fig._detail_regions:
        extent = text.get_window_extent(fig.canvas.get_renderer())
        (left, bottom), (right, top) = ax.transData.transform([(x0, y0), (x1, y1)])
        if extent.x0 < left or extent.y0 < bottom or extent.x1 > right or extent.y1 > top:
            raise ValueError(f"{key}: detail text outside its panel: {text.get_text()!r}")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{key}.png", dpi=150)
    svg_path = OUT / f"{key}.svg"
    fig.savefig(svg_path, metadata={"Date": None})
    # Matplotlib's path serialization leaves trailing spaces on every SVG
    # coordinate line; remove them so repository whitespace checks stay useful.
    svg_path.write_text(re.sub(r"[ \t]+$", "", svg_path.read_text(), flags=re.MULTILINE))
    plt.close(fig)


from inner_product_diagrams import register as register_inner_product_diagrams
register_inner_product_diagrams(globals())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figures", nargs="*", help="Optional figure IDs; default: all")
    args = parser.parse_args()
    if any(set(items) != set(BUILDERS) for items in (DETAILS, ENGLISH, LABEL_TERMS)):
        parser.error("Chinese and English content must cover exactly the registered diagrams")
    for key in args.figures or BUILDERS:
        if key not in BUILDERS:
            parser.error(f"Unknown figure ID: {key}")
        save_figure(key)
        print(f"Built {key}", flush=True)


if __name__ == "__main__":
    main()
