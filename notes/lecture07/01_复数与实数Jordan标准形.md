# 复数与实数 Jordan 标准形 / Complex and Real Jordan Forms

[阅读导航 / Guide](00_阅读导航.md) · [下一章 / Next](02_Jordan链与子空间分解.md)

> 对应课件第 2-11 页：定理 3.9、引理 3.1、定理 3.10-3.11、定义 3.9。 / Slides 2-11: Theorem 3.9, Lemma 3.1, Theorems 3.10-3.11 and Definition 3.9.

## 一、从自然标准形开始 / Start with natural normal form

**中文：** 对 $n$ 阶常数矩阵 $A$，先对特征矩阵 $\lambda I-A$ 求 Smith 形。去掉单位项后，设非常数不变多项式为 $\psi_1\mid\cdots\mid\psi_\ell$；自然标准形为它们的列伴随块组成的块对角矩阵。

**English:** Start with the Smith form of $\lambda I-A$. Remove unit entries and write the nonconstant invariant polynomials as $\psi_1\mid\cdots\mid\psi_\ell$. Their column companion blocks form the natural normal form.

$$
\begin{gathered}
S_{\lambda I-A}=\operatorname{diag}(I_{n-\ell},\psi_1,\ldots,\psi_\ell),\\
A\sim\operatorname{diag}(C(\psi_1),\ldots,C(\psi_\ell)),\qquad
\sum_i\deg\psi_i=n.
\end{gathered}
$$

**中文：** 对首一 $p=\lambda^m+c_{m-1}\lambda^{m-1}+\cdots+c_0$，$C(p)$ 的次对角线为 $1$，最后一列为 $-(c_0,\ldots,c_{m-1})^T$，其余为零。Jordan 形继续把一个伴随块按互素因子拆成更小的块。

**English:** For monic $p=\lambda^m+c_{m-1}\lambda^{m-1}+\cdots+c_0$, $C(p)$ has subdiagonal ones, final column $-(c_0,\ldots,c_{m-1})^T$ and zeros elsewhere. Jordan form further splits a companion block according to coprime factors.

## 二、互素分解为什么允许拆块 / Why coprime factors split blocks

**中文：** 课件引理 3.1：若 $\varphi_1,\ldots,\varphi_s$ 两两互素，则

**English:** Lemma 3.1 states that, for pairwise coprime $\varphi_1,\ldots,\varphi_s$,

$$
\operatorname{diag}(\varphi_1,\ldots,\varphi_s)
\cong\operatorname{diag}\left(I_{s-1},\prod_{i=1}^s\varphi_i\right).
$$

**中文：** $\cong$ 在这里是多项式矩阵的幺模等价，不是常数矩阵相似。对两个因子，第一行列式因子为 $\gcd(\varphi_1,\varphi_2)=1$，第二个为乘积，立即得到此式。应用于特征矩阵，再用“特征矩阵等价当且仅当原矩阵相似”，便可拆分伴随块。

**English:** Here $\cong$ denotes unimodular equivalence of polynomial matrices. For two factors, the determinantal divisors are their gcd one and their product, which proves the identity. Apply this to characteristic matrices and then use the similarity criterion to split companion blocks.

**教学补充例题 / Teaching supplement：**

$$
C\bigl((\lambda-1)^2(\lambda+2)\bigr)
\sim\operatorname{diag}\bigl(J_2(1),[-2]\bigr).
$$

**中文：** 两个互素因子分别对应一个二阶块与一个一阶块，总大小仍为 $3$。同一根的不同初等因子不能相互合并；互素分解和合并重数是不同操作。

**English:** The two coprime factors give blocks of orders two and one, totaling three. Distinct elementary divisors for the same root must not be merged; coprime splitting does not combine their exponents.

## 三、复 Jordan 块：一个初等因子对应一个块 / One elementary divisor, one block

**中文：** 定义 $m$ 阶 Jordan 块为

**English:** The Jordan block of order $m$ is

$$
J_m(\rho)=\begin{bmatrix}
\rho&1&0&\cdots&0\\
0&\rho&1&\ddots&\vdots\\
\vdots&\ddots&\ddots&\ddots&0\\
0&\cdots&0&\rho&1\\
0&\cdots&\cdots&0&\rho
\end{bmatrix},\qquad J_1(\rho)=[\rho].
$$

**中文：** $\lambda I-J_m(\rho)$ 有常数子式 $(-1)^k$（$k<m$），且行列式为 $(\lambda-\rho)^m$，所以它只有一个非常数不变多项式，也只有一个初等因子：$(\lambda-\rho)^m$。

**English:** The characteristic matrix has constant minors $(-1)^k$ for $k<m$ and determinant $(\lambda-\rho)^m$. It has a single nonconstant invariant polynomial and a single elementary divisor, $(\lambda-\rho)^m$.

**中文：** 在复数域上，把所有初等因子逐个换成对应 Jordan 块，即得到完整复 Jordan 形。相同根的两个因子仍对应两个块。块的排列可变；块的根和大小由初等因子唯一确定。

**English:** Over the complex field, replace each elementary divisor by its Jordan block. Two factors at the same root still give two blocks. Block order is arbitrary, while eigenvalues and block sizes are fixed by the elementary divisors.

$$
\begin{aligned}
\text{代数重数 / algebraic multiplicity of }\rho
&=\text{该根各块大小之和 / sum of its block sizes},\\
\text{几何重数 / geometric multiplicity of }\rho
&=\text{该根的块数 / number of its blocks}.
\end{aligned}
$$

**中文：** 所有块均为一阶，当且仅当矩阵可在复数域对角化。代数重数本身不决定块长，还需要初等因子或核空间信息。

**English:** The matrix is diagonalizable over the complex field exactly when all blocks have order one. Algebraic multiplicity alone does not determine block lengths; elementary divisors or kernel information are needed.

## 四、实 Jordan 形：把共轭块配成实块 / Pairing conjugate blocks over the reals

**中文：** 对实矩阵，非实特征值 $a+bi$、$a-bi$（$b>0$）的 Jordan 块必须按相同大小配对。定义

**English:** For a real matrix, blocks at $a+bi$ and $a-bi$, with $b>0$, pair with matching sizes. Define

$$
R(a,b)=\begin{bmatrix}a&b\\-b&a\end{bmatrix},\qquad
\mathcal R_m(a,b)=\begin{bmatrix}
R(a,b)&I_2&0&\cdots&0\\
0&R(a,b)&I_2&\ddots&\vdots\\
\vdots&\ddots&\ddots&\ddots&0\\
0&\cdots&0&R(a,b)&I_2\\
0&\cdots&\cdots&0&R(a,b)
\end{bmatrix}.
$$

**中文：** 一对 $m$ 阶复块变为一个 $2m$ 阶实块。实特征值的普通 Jordan 块不变。注意实块的上次块对角线是 $I_2$，不是标量 $1$。

**English:** Two complex blocks of order $m$ become one real block of order $2m$. Blocks at real eigenvalues are unchanged. The real block's superdiagonal consists of $I_2$, not scalar ones.

**教学补充例题 / Teaching supplement：** 对 $a=-1,b=1,m=2$，有 / For these values,

$$
\mathcal R_2(-1,1)=\begin{bmatrix}
-1&1&1&0\\-1&-1&0&1\\0&0&-1&1\\0&0&-1&-1
\end{bmatrix}.
$$

**中文：** 它对应的复初等因子是 $(\lambda+1-i)^2$ 与 $(\lambda+1+i)^2$，对应的实不可约因子幂为 $((\lambda+1)^2+1)^2$。

**English:** Its complex elementary divisors are $(\lambda+1-i)^2$ and $(\lambda+1+i)^2$. Over the reals the corresponding irreducible power is $((\lambda+1)^2+1)^2$.

## 五、作业例题：三阶矩阵的全部标准形 / Homework example: all forms of a three-by-three matrix

$$
A=\begin{bmatrix}4&6&0\\-3&-5&0\\-3&-6&1\end{bmatrix}.
$$

**中文：** 对 $\lambda I-A$，计算得 $D_1=1$、$D_2=\lambda-1$、$D_3=(\lambda-1)^2(\lambda+2)$。这里 $D_2$ 可由 $\operatorname{rank}(A-I)=1$ 与一个子式 $-6(\lambda-1)$ 核对。

**English:** For $\lambda I-A$, the determinantal divisors are $1$, $\lambda-1$ and $(\lambda-1)^2(\lambda+2)$. Check the second using rank one at $\lambda=1$ and a witnessing minor $-6(\lambda-1)$.

$$
(d_1,d_2,d_3)=\bigl(1,\lambda-1,(\lambda-1)(\lambda+2)\bigr),\qquad
N=\begin{bmatrix}1&0&0\\0&0&2\\0&1&-1\end{bmatrix}.
$$

**中文：** 初等因子是 $\lambda-1$、$\lambda-1$、$\lambda+2$，所以所有 Jordan 块都是一阶，$J_{\rm complex}=J_{\rm real}=\operatorname{diag}(1,1,-2)$。特征值 $1$ 虽为二重根，但几何重数也是 $2$，因此可对角化。

**English:** The elementary divisors are $\lambda-1$, $\lambda-1$ and $\lambda+2$, so every Jordan block has order one. Both real and complex forms are $\operatorname{diag}(1,1,-2)$. The repeated eigenvalue one has geometric multiplicity two, so the matrix is diagonalizable.

## 六、作业例题：从初等因子恢复十一阶标准形 / Homework example: reconstructing eleven-dimensional forms

**中文：** 第 3 题给出根 $-1$ 的指数 $1,2,2$，根 $-1-j$、$-1+j$ 各有指数 $1,2$。按升序在左侧补零：

**English:** Problem 3 gives exponents $1,2,2$ at $-1$ and $1,2$ at each of $-1-j$ and $-1+j$. Sort and pad on the left:

| 根 / Root | 第 1 项 / First | 第 2 项 / Second | 第 3 项 / Third |
| --- | --- | --- | --- |
| $-1$ | 1 | 2 | 2 |
| $-1-j$ | 0 | 1 | 2 |
| $-1+j$ | 0 | 1 | 2 |

**中文：** 令 $x=\lambda+1$、$q=x^2+1$，同位置相乘得到

**English:** With $x=\lambda+1$ and $q=x^2+1$, multiply corresponding positions to obtain

$$
\psi_1=x,\qquad\psi_2=x^2q,\qquad\psi_3=x^2q^2.
$$

**中文：** 次数为 $1,4,6$，总和 $11$。特征矩阵满秩，因此有 $11$ 个非零不变多项式，其中 $8$ 个为 $1$。所以

**English:** Their degrees are one, four and six, totaling eleven. The characteristic matrix has eleven nonzero invariant polynomials, eight of which are one. Hence

$$
S=\operatorname{diag}(I_8,\psi_1,\psi_2,\psi_3),\qquad
N=\operatorname{diag}(-1,C(\psi_2),C(\psi_3)).
$$

**中文：** 复形中，$-1$ 的块长为 $1,2,2$，两个非实根各为 $1,2$。定义 $K_\pm=\operatorname{diag}(-1\pm j,J_2(-1\pm j))$，则

**English:** At $-1$, the complex block lengths are one, two and two; at each nonreal root they are one and two. Defining $K_\pm=\operatorname{diag}(-1\pm j,J_2(-1\pm j))$ gives

$$
J_{\rm complex}=\operatorname{diag}(-1,J_2(-1),J_2(-1),K_-,K_+).
$$

**中文：** 在实形中，两个非实根的一阶块配成 $R(-1,1)$，二阶块配成 $\mathcal R_2(-1,1)$：

**English:** For the real form, pair the order-one blocks into $R(-1,1)$ and the order-two blocks into $\mathcal R_2(-1,1)$:

$$
J_{\rm real}=\operatorname{diag}(-1,J_2(-1),J_2(-1),R(-1,1),\mathcal R_2(-1,1)).
$$

**中文：** 大小检查为 $1+2+2+2+4=11$。这一步能发现漏掉重复初等因子、误配共轭块和遗漏 Smith 单位项等错误。

**English:** Check the size: $1+2+2+2+4=11$. This catches omitted repeated factors, incorrectly paired conjugate blocks and missing Smith unit entries.

[阅读导航 / Guide](00_阅读导航.md) · [下一章 / Next](02_Jordan链与子空间分解.md)
