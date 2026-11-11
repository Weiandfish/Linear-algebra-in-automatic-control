# Hermitian 型与正定性

对应第 10(2) 文件第 25—35 页；第 1 部分未包含这些新内容。矩阵条件、二次型条件和谱条件要在同一域与同一种变换下比较。

## 一、实值二次型刻画 Hermitian

$$
A=A^*\Longrightarrow \overline{x^*Ax}=x^*A^*x=x^*Ax\in\mathbb R.
$$

**作业例题：HW10.8。** 若对所有复向量 $x$ 均有 $x^*Ax\in\mathbb R$，置 $H=A-A^*$。

$$
x^*Hx=0,\quad x=e_i\Rightarrow h_{ii}=0,\quad
x=e_i+e_j\Rightarrow h_{ij}+h_{ji}=0,\quad
x=e_i+ie_j\Rightarrow i(h_{ij}-h_{ji})=0.
$$

$$
H=0\Longrightarrow A=A^*.
$$

必须允许复向量测试。实向量只能看见实斜对称矩阵的二次型为零，例如 $\begin{bmatrix}0&1\\-1&0\end{bmatrix}$ 并非 Hermitian。

## 二、Hermitian 运算、分解与标准形

$$
A=H+iK,\quad H=\frac{A+A^*}{2}=H^*,\quad
K=\frac{A-A^*}{2i}=K^*.
$$

分解中的 $K$ 是 Hermitian；真正的斜 Hermitian 部分是 $iK=(A-A^*)/2$。若 $H$ 为 Hermitian，$H^m,H^{-1}$（存在时）也为 Hermitian；实系数线性组合仍 Hermitian。

$$
A=A^*,\ B=B^*:\qquad (AB)^*=BA
\Longrightarrow AB\text{ Hermitian}\iff AB=BA.
$$

$$
A=A^*\Longrightarrow A=U\operatorname{diag}(\lambda_i)U^*,\quad\lambda_i\in\mathbb R,
\qquad x=Uy\Longrightarrow x^*Ax=\sum_i\lambda_i|y_i|^2.
$$

酉变换保留特征值，给出上式的谱标准形。进一步允许可逆合同，非零系数才可归一化到 $\pm1$；不要将合同标准形误作酉相似结果。

## 三、正定与半正定

$$
A\succ0\iff A=A^*,\ x^*Ax>0\ (x\ne0),\qquad
A\succeq0\iff A=A^*,\ x^*Ax\ge0\ (\forall x).
$$

$$
A\succ0\iff\lambda_i>0\ (\forall i)
\iff A=Q^*Q\ (Q\text{ 可逆})
\iff P^*AP=I\ (P\text{ 可逆}).
$$

$$
A\succeq0\iff\lambda_i\ge0\ (\forall i)
\iff A=Q^*Q
\iff P^*AP=\operatorname{diag}(I_r,0),\quad r=\rank A.
$$

半正定的因子 $Q$ 可以奇异。可逆合同保持正定性和半正定性：$x^*P^*APx=(Px)^*A(Px)$。

## 四、主子式与 Cholesky 计算

Sylvester 判据要求先有 $A=A^*$。正定当且仅当所有顺序主子式 $\Delta_k=\det A[1\!:\!k,1\!:\!k]>0$。半正定当且仅当所有主子式非负，不能只检查顺序主子式。

$$
\operatorname{diag}(0,-1):\quad\Delta_1=\Delta_2=0,
\qquad e_2^*Ae_2=-1<0.
$$

**教学补充例题：**

$$
H=\begin{bmatrix}2&1\\1&2\end{bmatrix},\quad
\Delta_1=2,\quad\Delta_2=3,\quad\sigma(H)=\{1,3\},
$$

$$
R=\begin{bmatrix}\sqrt2&1/\sqrt2\\0&\sqrt{3/2}\end{bmatrix},
\qquad H=R^*R,\qquad x^*Hx=\|Rx\|^2>0\ (x\ne0).
$$

对正定 $A$，上三角正对角的 Cholesky 因子唯一。递推时 $r_{kk}=\sqrt{a_{kk}-\sum_{i<k}|r_{ik}|^2}$，再求 $r_{kj}$。

$$
r_{kj}=\frac{a_{kj}-\sum_{i<k}\bar r_{ik}r_{ij}}{r_{kk}}\quad(j>k).
$$

<!-- diagram:40_hermitian_positive:start -->

**图解 · 正定 Hermitian 型：等值线、特征值与主子式**

![正定 Hermitian 型：等值线、特征值与主子式](../../assets/diagrams/40_hermitian_positive.png)

**读图：** 左图是实平面上的三条椭圆等值线，长短轴对应特征值 1、3。右图用正特征值和正顺序主子式验证同一矩阵正定；对复向量的结论由酉谱分解给出。

<!-- diagram:40_hermitian_positive:end -->

## 五、唯一非负平方根

$$
A=U\operatorname{diag}(\lambda_i)U^*\succeq0
\Longrightarrow A^{1/2}=U\operatorname{diag}(\sqrt{\lambda_i})U^*\succeq0,
\quad(A^{1/2})^2=A.
$$

若 $H\succeq0$ 且 $H^2=A$，则 $HA=AH$，每个 $A$ 的特征空间对 $H$ 不变。在特征值 $\lambda$ 的空间内，$H$ 的非负特征值只能是 $\sqrt\lambda$，故限制为 $\sqrt\lambda I$，得到唯一性。与 $A$ 交换的矩阵也保持这些特征空间，因此与 $A^{1/2}$ 交换。

## 六、正定矩阵的广义特征值

**讲义例题：例 4.13，$A\succ0,B\succ0$。**

$$
C=B^{-1/2}AB^{-1/2}\succ0,\qquad
\det(\lambda B-A)=\det B\cdot\det(\lambda I-C).
$$

$$
\det(\lambda B-A)=0\Longrightarrow\lambda\in\sigma(C)\subset(0,\infty).
$$

$B^{-1}A$ 不一定 Hermitian，但与正定 Hermitian 的 $C$ 相似，所以根仍全为正实数。

[中文阅读导航](00_阅读导航.md)
