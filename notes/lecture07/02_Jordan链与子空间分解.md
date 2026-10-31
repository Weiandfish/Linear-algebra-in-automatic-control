# Jordan 链与子空间分解 / Jordan Chains and Subspace Decomposition

[阅读导航 / Guide](00_阅读导航.md) · [上一章 / Previous](01_复数与实数Jordan标准形.md) · [练习速查 / Exercises](03_练习与公式速查.md)

> 对应课件第 12-21 页：定义 3.10-3.12、定理 3.13-3.18。 / Slides 12-21: Definitions 3.10-3.12 and Theorems 3.13-3.18.

## 一、广义特征向量与链关系 / Generalized eigenvectors and chain relations

**中文：** 固定特征值 $\rho$，记 $N_\rho=A-\rho I$。非零向量 $x$ 的确切广义特征向量阶数为 $k$，是指 $N_\rho^kx=0$ 而 $N_\rho^{k-1}x\ne0$。一阶就是普通特征向量。

**English:** Fix an eigenvalue $\rho$ and write $N_\rho=A-\rho I$. A nonzero vector has exact generalized-eigenvector order $k$ when $N_\rho^kx=0$ but $N_\rho^{k-1}x\ne0$. Order one gives ordinary eigenvectors.

$$
N_\rho x_1=0,\quad x_1\ne0,\qquad
N_\rho x_{r+1}=x_r\quad(1\le r<m).
$$

**中文：** 上式是长度为 $m$ 的链关系，$x_1$ 是链头，$x_m$ 是链尾；每个 $x_r$ 恰为 $r$ 阶。课件还要求 $x_m\notin\operatorname{im}N_\rho$，使链不能再延长。只满足递推式的截短链未必满足这个额外要求。

**English:** These are the relations of a length-$m$ chain, with head $x_1$ and terminal vector $x_m$; each $x_r$ has exact order $r$. The lecture additionally requires $x_m\notin\operatorname{im}N_\rho$, so the chain cannot be extended. A truncated sequence can satisfy the recurrence without meeting that extra condition.

**中文：** 单链向量线性无关：若关系中最高非零系数对应 $x_r$，作用 $N_\rho^{r-1}$ 只剩该系数乘 $x_1$，矛盾。这是定理 3.14 的证明要点。

**English:** A chain is independent: in a dependence, take the largest index $r$ with a nonzero coefficient and apply $N_\rho^{r-1}$. Only that coefficient times $x_1$ remains, a contradiction. This proves the key claim of Theorem 3.14.

## 二、链的列顺序决定 Jordan 块的方向 / Column order determines block orientation

**中文：** 把向量按链头到链尾排成 $X_\rho=(x_1,\ldots,x_m)$。链关系等价于

**English:** Arrange the columns from head to terminal vector as $X_\rho=(x_1,\ldots,x_m)$. The chain relations become

$$
AX_\rho=X_\rho J_m(\rho).
$$

**中文：** 第 $r$ 列满足 $Ax_r=\rho x_r+x_{r-1}$，约定 $x_0=0$，因此 $1$ 出现在上次对角线。倒序放列会改变矩阵形式，不能仍照写同一个 $J_m$。

**English:** Column $r$ satisfies $Ax_r=\rho x_r+x_{r-1}$, with $x_0=0$, placing ones on the superdiagonal. Reversing the column order changes the resulting matrix.

**中文：** 同一特征值下，多条链合在一起线性无关，当且仅当链头线性无关；不同特征值的链来自互不相交的广义特征空间。选齐正确长度的链后，若总列数为 $n$，得到

**English:** Chains for the same eigenvalue are jointly independent exactly when their heads are independent. Chains for distinct eigenvalues lie in independent generalized eigenspaces. With the required lengths and a total of $n$ columns, one obtains

$$
X=(X_1,\ldots,X_r),\qquad AX=XJ,\qquad \det X\ne0,
\qquad X^{-1}AX=J.
$$

**中文：** 验证时要同时检查 $AX=XJ$ 和 $X$ 可逆；只有前一个等式并不能保证相似。

**English:** Verify both $AX=XJ$ and invertibility of $X$. The intertwining equation alone does not establish similarity.

## 三、如何实际寻找链 / How to find chains

1. **中文：** 先由初等因子确定各根的块数与块长，从长链开始。

   **English:** Determine block counts and lengths from elementary divisors, starting with longer chains.

2. **中文：** 对目标长度 $m$，选 $v\in\ker N_\rho^m\setminus\ker N_\rho^{m-1}$ 作链尾，依次计算 $x_r=N_\rho^{m-r}v$。按课件的不可延长定义，还须令 $v\notin\operatorname{im}N_\rho$。

   **English:** For a length-$m$ chain, choose a terminal vector $v\in\ker N_\rho^m\setminus\ker N_\rho^{m-1}$ and set $x_r=N_\rho^{m-r}v$. The lecture's nonextendible-chain definition also requires $v\notin\operatorname{im}N_\rho$.

3. **中文：** 补选其余链，使链头独立；不能只看每条链各自独立。最后检查列数、秩与 $AX=XJ$。

   **English:** Choose remaining chains with independent heads. Independence within each chain alone is insufficient. Finally check the column count, rank and intertwining equation.

**教学补充例题：不是每个特征向量都能延长 / Teaching supplement: not every eigenvector extends.**

$$
A=\operatorname{diag}(J_2(\rho),[\rho]).
$$

**中文：** $e_1,e_3$ 都是特征向量；$e_1$ 可用 $e_2$ 延长，因为 $(A-\rho I)e_2=e_1$。但 $e_3$ 不在像空间中，不能作为长度二的链头。选择链长时必须考虑像空间条件。

**English:** Both $e_1$ and $e_3$ are eigenvectors. The vector $e_1$ extends through $e_2$, since $(A-\rho I)e_2=e_1$. The vector $e_3$ is outside the image and cannot head a length-two chain. Extension depends on the image condition.

## 四、作业例题与教学补充：四阶矩阵的完整 Jordan 基 / Homework example and supplement: a complete four-dimensional Jordan basis

$$
A=\begin{bmatrix}2&0&2&1\\6&1&4&4\\10&0&0&4\\7&0&-7&2\end{bmatrix}.
$$

**中文：** 特征多项式为 $(\lambda-1)^3(\lambda-2)$。两个特征空间均一维：

**English:** The characteristic polynomial is $(\lambda-1)^3(\lambda-2)$. Both eigenspaces are one-dimensional:

$$
E_1(A)=\operatorname{span}\{(0,1,0,0)^T\},\qquad
E_2(A)=\operatorname{span}\{(1,2,1,-2)^T\}.
$$

**中文：** 作业第 1 题只要求普通特征向量。若原基为 $(\alpha_1,\alpha_2,\alpha_3,\alpha_4)$，则算子的特征向量分别为非零倍数的 $\alpha_2$ 与 $\alpha_1+2\alpha_2+\alpha_3-2\alpha_4$。坐标列与抽象向量不能混写。

**English:** Problem 1 asks only for ordinary eigenvectors. In the given abstract basis, the operator eigenvectors are nonzero multiples of $\alpha_2$ and $\alpha_1+2\alpha_2+\alpha_3-2\alpha_4$. Distinguish these vectors from their coordinate columns.

**中文：** 以下补出完整 Jordan 基供学习。对特征值 $1$，可取

**English:** As a teaching supplement, a complete Jordan basis can be constructed. At eigenvalue one, take

$$
x_1=\begin{bmatrix}0\\6\\0\\0\end{bmatrix},\quad
x_2=\begin{bmatrix}-9\\-26\\-6\\21\end{bmatrix},\quad
x_3=\begin{bmatrix}5\\0\\0\\-14\end{bmatrix},\qquad
x_4=\begin{bmatrix}1\\2\\1\\-2\end{bmatrix}.
$$

$$
(A-I)x_1=0,\quad(A-I)x_2=x_1,\quad(A-I)x_3=x_2,\quad Ax_4=2x_4.
$$

**中文：** $X=(x_1,x_2,x_3,x_4)$ 的行列式为 $-18$，所以可逆，且 $AX=X\operatorname{diag}(J_3(1),[2])$。这解释了为什么只有两个无关的普通特征向量，却仍能组成四维 Jordan 基。

**English:** The matrix $X=(x_1,x_2,x_3,x_4)$ has determinant $-18$ and satisfies $AX=X\operatorname{diag}(J_3(1),[2])$. Although only two independent ordinary eigenvectors exist, generalized vectors complete a four-dimensional basis.

## 五、Jordan 子空间是广义特征空间 / Jordan subspaces are generalized eigenspaces

**中文：** 课件定义的 Jordan 子空间为

**English:** The lecture's Jordan subspace is

$$
G_\rho=\{x:\exists k\ge1,\ (A-\rho I)^kx=0\}
=\ker(A-\rho I)^n.
$$

**中文：** 最后一式用于有限维 $n$ 阶矩阵。$G_\rho$ 由该根所有 Jordan 链的向量生成，维数等于该根的代数重数；普通特征空间 $E_\rho=\ker(A-\rho I)$ 一般只是其中一部分。

**English:** The final equality is for an $n$-by-$n$ matrix. All chains at $\rho$ span $G_\rho$, whose dimension is the algebraic multiplicity. The ordinary eigenspace $E_\rho$ is generally a proper part of it.

$$
G_\rho=\bigoplus_{\text{该根各链 / chains at }\rho}\operatorname{span}\{x_1,\ldots,x_m\},
\qquad\mathbb C^n=\bigoplus_\rho G_\rho.
$$

**中文：** 每个链空间都不变，因为 $Ax_r=\rho x_r+x_{r-1}$。不同链的具体选法可以改变，但整个 $G_\rho$ 由核的定义确定。上一例中，$G_1=\operatorname{span}\{x_1,x_2,x_3\}$，$G_2=\operatorname{span}\{x_4\}$。

**English:** Each chain span is invariant because $Ax_r=\rho x_r+x_{r-1}$. Individual chains are not uniquely chosen, but $G_\rho$ is fixed by its kernel definition. In the example, $G_1$ is spanned by the first three columns and $G_2$ by the fourth.

**中文：** 对抽象空间中的算子，把每个坐标列 $x$ 还原为 $\sum_i\alpha_i x_i$。坐标空间的链和直和分解便得到课件第 20—21 页的抽象空间分解。

**English:** For an abstract operator, convert each coordinate column $x$ into $\sum_i\alpha_i x_i$. Coordinate chains and direct sums then give the abstract decomposition described on slides 20-21.

## 六、教学补充：从复链构造实基 / Teaching supplement: real bases from complex chains

**中文：** 设 $A$ 为实矩阵，$z_r=u_r+iv_r$ 是特征值 $a+bi$（$b>0$）的一条链，令 $u_0=v_0=0$。分离实部与虚部可得

**English:** Let $A$ be real and let $z_r=u_r+iv_r$ form a chain at $a+bi$, $b>0$. Set $u_0=v_0=0$. Separating real and imaginary parts gives

$$
Au_r=au_r-bv_r+u_{r-1},\qquad
Av_r=bu_r+av_r+v_{r-1}.
$$

**中文：** 按 $(u_1,v_1,u_2,v_2,\ldots,u_m,v_m)$ 排列实基，矩阵正好是上一章的 $\mathcal R_m(a,b)$。这也说明为什么实形式需要 $I_2$ 连接相邻二阶块。

**English:** Ordering the real basis as $(u_1,v_1,u_2,v_2,\ldots,u_m,v_m)$ produces $\mathcal R_m(a,b)$ from Chapter 01. This explains the $I_2$ links between consecutive two-by-two blocks.

## 七、教学补充：从核维数读块长 / Teaching supplement: block lengths from nullities

**中文：** 若尚未求出初等因子，可以逐次求核。记 $h_0=0$、$h_k=\dim\ker(A-\rho I)^k$。一个长度 $m$ 的块贡献 $\min(k,m)$，所以

**English:** Kernel computations provide another way to determine block sizes. Write $h_0=0$ and $h_k=\dim\ker(A-\rho I)^k$. A size-$m$ block contributes $\min(k,m)$, hence

$$
\begin{aligned}
\#\{\text{块长 / size}\ge k\}&=h_k-h_{k-1},\\
\#\{\text{块长 / size}=k\}&=2h_k-h_{k-1}-h_{k+1}.
\end{aligned}
$$

**教学补充例题 / Teaching supplement：** 若 $h_1,h_2,h_3,h_4=2,4,5,5$，增量为 $2,2,1,0$，所以有两个块，大小分别为 $3,2$。 / Nullities $2,4,5,5$ give increments $2,2,1,0$, hence two blocks of sizes three and two.

[阅读导航 / Guide](00_阅读导航.md) · [上一章 / Previous](01_复数与实数Jordan标准形.md) · [练习速查 / Exercises](03_练习与公式速查.md)
