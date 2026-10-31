# Smith 标准形与不变多项式 / Smith Form and Invariant Polynomials

[阅读导航 / Guide](00_阅读导航.md) · [下一章 / Next](02_初等因子与特征矩阵.md)

> 对应课件第 4-15 页：定义 2.11-2.17、引理 2.1、定理 2.20-2.27。 / Slides 4-15: Definitions 2.11-2.17, Lemma 2.1 and Theorems 2.20-2.27.

## 一、允许哪些变换 / Admissible transformations

**中文：** 多项式矩阵的秩是非零多项式子式的最高阶数，不是在某一点代入后的秩。方阵多项式的逆仍是多项式矩阵时称幺模，等价判据是行列式为非零常数。

**English:** Polynomial-matrix rank is the largest order of a minor that is not identically zero, rather than rank at one substitution. A square polynomial matrix is unimodular when its inverse is also polynomial, equivalently when its determinant is a nonzero constant.

$$
U\text{ 幺模 / unimodular}\iff\det U\in\mathbb F\setminus\{0\}.
$$

**中文：** 合法的初等行变换是交换两行、一行乘非零常数、将一行的多项式倍数加到另一行；列变换同理。加法操作的逆是减去同一个倍数，因此这些变换都可逆。不能用非恒定多项式直接倍乘整行。

**English:** Elementary row operations swap rows, multiply a row by a nonzero constant, or add a polynomial multiple of one row to another; column operations are analogous. A row addition is reversed by subtraction, so all these operations are invertible. Scaling a whole row by a nonconstant polynomial is not admissible.

**教学补充例题 / Teaching supplement：**

$$
U=\begin{bmatrix}1&\lambda\\0&1\end{bmatrix},\qquad
U^{-1}=\begin{bmatrix}1&-\lambda\\0&1\end{bmatrix}.
$$

**中文：** 左乘 $U$ 把第二行的 $\lambda$ 倍加到第一行；右乘 $U$ 把第一列的 $\lambda$ 倍加到第二列。同一初等矩阵的行、列含义要按乘法实际展开，不能直接照抄行号。

**English:** Premultiplication by $U$ adds $\lambda$ times row two to row one. Postmultiplication adds $\lambda$ times column one to column two. Interpret row and column effects through multiplication rather than copying row indices mechanically.

**中文：** 同型矩阵 $A\in\mathbb F[\lambda]^{m\times n}$ 与 $B$ 等价，当且仅当存在 $m$ 阶、$n$ 阶幺模矩阵 $P,Q$，使 $B=PAQ$。这允许独立的左右变换；相似变换 $P^{-1}AP$ 的要求更强。

**English:** Matrices $A\in\mathbb F[\lambda]^{m\times n}$ and $B$ of the same size are equivalent exactly when $B=PAQ$ for unimodular matrices $P,Q$ of orders $m,n$. Left and right transformations are independent; similarity $P^{-1}AP$ imposes a stronger constraint.

## 二、Smith 标准形的含义 / What the Smith form records

**中文：** 若 $A$ 的秩为 $r$，则能通过上述变换得到同型的伪对角矩阵：

**English:** If $A$ has rank $r$, these operations reduce it to a pseudo-diagonal matrix of the same size:

$$
PAQ=S_A=\begin{bmatrix}
\operatorname{diag}(d_1,\ldots,d_r)&0\\0&0
\end{bmatrix},\qquad
d_i\ne0,\quad d_i\text{ 首一 / monic},\quad d_i\mid d_{i+1}.
$$

**中文：** 非零对角元 $d_i$ 叫不变多项式，必须组成整除链。单位多项式 $1$ 也算不变多项式；零行、零列由原矩阵大小和秩确定。零矩阵的标准形就是同型零矩阵，非零不变多项式列表为空。

**English:** The nonzero diagonal entries $d_i$ are invariant polynomials and must form a divisibility chain. The unit polynomial one is included. Original dimensions and rank determine the zero padding. A zero matrix has the same-sized zero Smith form and an empty invariant list.

**中文：** 任意对角矩阵未必已经是 Smith 形。例如 $\operatorname{diag}(\lambda,\lambda-1)$ 不满足整除链，正确 Smith 形是 $\operatorname{diag}(1,\lambda(\lambda-1))$。

**English:** An arbitrary diagonal matrix need not be in Smith form. For example, $\operatorname{diag}(\lambda,\lambda-1)$ fails the divisibility condition; its Smith form is $\operatorname{diag}(1,\lambda(\lambda-1))$.

## 三、为什么能够化成标准形 / Why reduction terminates

**中文：** 课件引理 2.1 的关键是降次：若左上角非零元不能整除某个元素，通过多项式除法和行列操作，可以把某个非零余式移到左上角，使主元次数严格下降。

**English:** Lemma 2.1 provides degree reduction: if the nonzero upper-left entry fails to divide an entry, polynomial division and row/column operations can move a nonzero remainder to the pivot position, strictly lowering its degree.

1. **中文：** 把非零元移到左上角，利用除法处理同一行、同一列；非零余式替换主元并继续。

   **English:** Move a nonzero entry to the upper left and divide entries in its row and column. Replace the pivot by any nonzero remainder and continue.

2. **中文：** 若已清空第一行、第一列，但主元不整除右下块某项，把相应下方行加到第一行，引入该项，再作列除法以降次。

   **English:** After clearing the first row and column, if the pivot fails to divide a lower-right entry, add its row to the first row and use column division to reduce the pivot degree again.

3. **中文：** 主元最终整除余下所有元素，首一化后固定；递归处理右下块。块内变换保留“全是上一主元的倍数”，因此最后得到整除链。

   **English:** Eventually the pivot divides every remaining entry. Normalize it and recurse on the lower-right block. Operations there preserve divisibility by the preceding pivot, producing the required chain.

**教学补充例题：二维降阶 / Teaching supplement: a two-by-two reduction.**

$$
\begin{aligned}
\begin{bmatrix}\lambda&1\\0&\lambda\end{bmatrix}
&\xrightarrow{c_1\leftrightarrow c_2}
\begin{bmatrix}1&\lambda\\\lambda&0\end{bmatrix}
\xrightarrow{r_2\leftarrow r_2-\lambda r_1}
\begin{bmatrix}1&\lambda\\0&-\lambda^2\end{bmatrix}\\
&\xrightarrow{c_2\leftarrow c_2-\lambda c_1}
\begin{bmatrix}1&0\\0&-\lambda^2\end{bmatrix}
\xrightarrow{r_2\leftarrow-r_2}
\operatorname{diag}(1,\lambda^2).
\end{aligned}
$$

**中文：** 每一步都是可逆的多项式初等变换；最后的两个对角元首一且前者整除后者。

**English:** Every step is an invertible polynomial elementary operation. The final entries are monic and satisfy divisibility.

## 四、用行列式因子计算，不必找出左右矩阵 / Compute using determinantal divisors

**中文：** 对 $1\le k\le r$，定义 $D_k$ 为全部非零 $k$ 阶子式的首一最大公因式；把零子式也放进最大公因式计算不改变结果。另设 $D_0=1$、$k>r$ 时 $D_k=0$。

**English:** For $1\le k\le r$, define $D_k$ as the monic gcd of all nonzero $k\times k$ minors. Including zero minors does not change that gcd. Set $D_0=1$ and $D_k=0$ for $k>r$.

$$
\boxed{D_k=d_1d_2\cdots d_k},\qquad
\boxed{d_k=\frac{D_k}{D_{k-1}}}\quad(1\le k\le r).
$$

**中文：** 第一式来自 Smith 形的整除链：每个非零 $k$ 阶子式都被前 $k$ 个对角元的乘积整除，而且该乘积本身就是一个子式。幺模变换后，每个新子式都是原子式的多项式组合，逆变换也成立，故首一最大公因式不变。于是 $D_k$ 唯一确定 $d_k$，证明标准形唯一。

**English:** In Smith form, every nonzero minor of order $k$ is divisible by the product of the first $k$ entries, and that product is itself a minor. Under unimodular operations, new minors are polynomial combinations of old minors, and the inverse gives the reverse relation. Their monic gcd is unchanged. Thus the $D_k$ uniquely determine the $d_k$, proving uniqueness.

**中文：** 只需结果时，通常先找一个简单子式提供“上界”，再证明全部同阶子式都含所需因子。仅找出一个非零子式可以判断秩的下界，不能直接把它当作行列式因子。

**English:** For computation, a simple witnessing minor often bounds the gcd, while a common-factor argument proves divisibility of all minors. One nonzero minor only supplies a lower bound on rank; it is not automatically the determinantal divisor.

**作业例题：第四次作业第 1 题 / Homework example: Problem 1.**

$$
A=\begin{bmatrix}
1-\lambda&\lambda^2&\lambda\\
2\lambda-1&\lambda(1-\lambda)&-2\lambda\\
1+\lambda^2&\lambda^2&-\lambda^2
\end{bmatrix}.
$$

**中文：** $2(1-\lambda)+(2\lambda-1)=1$，故全部元素的最大公因式为 $D_1=1$。第二、三列都含 $\lambda$，任意二阶子式至少选中这两列中的一列，因此均含 $\lambda$。以下子式又恰为 $-\lambda$：

**English:** The identity $2(1-\lambda)+(2\lambda-1)=1$ gives $D_1=1$. Both columns two and three contain $\lambda$, and every two-column selection contains at least one of them, so every second-order minor contains $\lambda$. The following minor is exactly $-\lambda$:

$$
\begin{vmatrix}1-\lambda&\lambda\\2\lambda-1&-2\lambda\end{vmatrix}=-\lambda.
$$

**中文：** 因此 $D_2=\lambda$；行列式为 $-\lambda^2(\lambda+1)$，首一化得 $D_3=\lambda^2(\lambda+1)$。依次相除：

**English:** Therefore $D_2=\lambda$. The determinant is $-\lambda^2(\lambda+1)$, so its monic normalization is $D_3=\lambda^2(\lambda+1)$. Consecutive quotients give

$$
(d_1,d_2,d_3)=(1,\lambda,\lambda(\lambda+1)),\qquad
S_A=\operatorname{diag}(1,\lambda,\lambda(\lambda+1)).
$$

## 五、结构化矩阵：优先找常数子式 / Structured matrices: seek constant minors

**中文：** 只要存在一个非零常数 $k$ 阶子式，$D_k$ 就是 $1$。但某个非零的高次子式本身并不具有这个效果。

**English:** A single nonzero constant minor of order $k$ forces $D_k=1$. A nonzero positive-degree minor does not have that effect by itself.

**作业例题：上双对角矩阵 / Homework example: an upper bidiagonal matrix.**

$$
A_{ii}=\lambda-a,\qquad A_{i,i+1}=b_i\ne0,
\qquad\text{其余元素为零 / all other entries zero}.
$$

**中文：** 对 $k<n$，前 $k$ 行、第 $2$ 至 $k+1$ 列组成下三角子矩阵，其对角元为 $b_1,\ldots,b_k$，子式为非零常数 $b_1\cdots b_k$。所以 $D_1=\cdots=D_{n-1}=1$，而 $D_n=(\lambda-a)^n$。

**English:** For $k<n$, the first $k$ rows and columns $2$ through $k+1$ form a lower triangular submatrix with diagonal $b_1,\ldots,b_k$. Its determinant is a nonzero constant. Thus $D_1=\cdots=D_{n-1}=1$, whereas $D_n=(\lambda-a)^n$.

$$
S_A=\operatorname{diag}(\underbrace{1,\ldots,1}_{n-1},(\lambda-a)^n).
$$

**作业例题：伴随结构 / Homework example: a companion structure.**

$$
C(\lambda)=\begin{bmatrix}
\lambda&0&\cdots&0&a_0\\
-1&\lambda&\ddots&\vdots&a_1\\
0&-1&\ddots&0&\vdots\\
\vdots&\ddots&\ddots&\lambda&a_{n-2}\\
0&\cdots&0&-1&\lambda+a_{n-1}
\end{bmatrix}.
$$

**中文：** 第 $2$ 至 $k+1$ 行、前 $k$ 列的子式为 $(-1)^k$，故 $k<n$ 时 $D_k=1$。按最后一列展开，行列式为 $p=\lambda^n+a_{n-1}\lambda^{n-1}+\cdots+a_0$，得到 $S_C=\operatorname{diag}(1,\ldots,1,p)$。

**English:** Rows $2$ through $k+1$ and the first $k$ columns give a minor $(-1)^k$, so $D_k=1$ for $k<n$. Expansion along the last column gives $p=\lambda^n+a_{n-1}\lambda^{n-1}+\cdots+a_0$, hence $S_C=\operatorname{diag}(1,\ldots,1,p)$.

## 六、等价与幺模的判据 / Equivalence and unimodularity tests

**中文：** 对同型多项式矩阵，以下条件等价：幺模等价；相同的 Smith 形；相同的秩及全部非零行列式因子；相同的完整不变多项式列表（包括 $1$）。方阵幺模当且仅当满秩且所有不变多项式均为 $1$，即等价于单位矩阵；这也说明幺模矩阵可分解为有限个初等矩阵的乘积。

**English:** For matrices of the same size, unimodular equivalence, equal Smith forms, equal ranks and all nonzero determinantal divisors, and equal complete invariant lists including ones are equivalent. A square matrix is unimodular exactly when it has full rank and every invariant polynomial is one, equivalently when it is equivalent to the identity. This also yields a factorization into finitely many elementary matrices.

**教学补充反例 / Teaching counterexample：**

$$
A=\operatorname{diag}(\lambda,\lambda),\qquad
B=\operatorname{diag}(1,\lambda^2).
$$

**中文：** 两者行列式相同，但 $D_1(A)=\lambda$、$D_1(B)=1$，所以不等价。行列式只给出最后一个行列式因子，丢失了中间信息。

**English:** The determinants agree, but $D_1(A)=\lambda$ and $D_1(B)=1$, so they are not equivalent. A determinant supplies only the final determinantal divisor and loses the intermediate information.

[阅读导航 / Guide](00_阅读导航.md) · [下一章 / Next](02_初等因子与特征矩阵.md)
