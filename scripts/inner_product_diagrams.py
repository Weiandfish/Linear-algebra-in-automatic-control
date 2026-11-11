"""Chapter 4 diagrams, using the course's shared dark bilingual design."""
import numpy as np


def register(api):
    diagram, canvas, label, box, arrow, matrix, note = (
        api[k] for k in ("diagram", "canvas", "label", "box", "arrow", "matrix", "note"))
    BLUE, TEAL, ORANGE, PURPLE, MUTED = (
        api[k] for k in ("BLUE", "TEAL", "ORANGE", "PURPLE", "MUTED"))
    original_label = label

    def label(ax, x, y, text, *args, **kwargs):
        item = original_label(ax, x, y, text, *args, **kwargs)
        if "$" not in text:
            # Ordinary bilingual labels retain word spacing and text fonts.
            item._english_translation = True
        return item

    records = {
        "36_inner_product_gram": (
            "Gram 矩阵：把基的几何关系放进坐标公式",
            "A Gram matrix carries geometry into coordinates",
            "同一个坐标列在不同基下，长度未必等于坐标的欧氏长度。",
            "Coordinate length agrees with geometric length only in an orthonormal basis.",
            "本例内积对第一变量共轭线性，标准坐标中为 x* y；一般基中要插入 G。",
            "The inner product is conjugate linear in the first slot. Insert G when the basis is not orthonormal.",
            (("按基逐项计算", [r"$b_1=(1,0),\ b_2=(1,1)$。", r"$G_{ij}=b_i^*b_j$，因此 $G=B^*B$。", r"$x=(0,1)$ 时 $Bx=b_2$，长度平方为 $2$。"]),
             ("换基与合同", [r"新基 $B'=BP$，故 $G'=P^*GP$。", r"$G=G^*$，且 $x^*Gx>0$ 对所有 $x\ne0$。", r"正交规范基下 $G=I$，才有 $\langle Bx,By\rangle=x^*y$。"])),
            (("Compute from the basis", ["The two basis vectors are shown above.", "Every entry is a pairwise inner product of basis vectors.", "The second coordinate vector has geometric squared length two."]),
             ("Change of basis and congruence", ["A change of basis transforms G by congruence.", "The Gram matrix of a basis is Hermitian positive definite.", "An orthonormal basis makes G the identity."])),
            "内积 Inner product · 基 Basis · 长度 Norm · 合同 Congruence"),
        "37_gram_schmidt_unitary": (
            "Gram–Schmidt：减去已有方向，再归一化",
            "Gram-Schmidt: subtract projections, then normalize",
            "从独立的列得到正交规范列，投影系数同时组成 QR 分解。",
            "Independent input columns yield orthonormal columns and an upper triangular factor.",
            "正对角条件固定每列的相位；方阵满秩时，QR 因子唯一。",
            "Positive diagonal entries fix the column phases; a nonsingular square matrix has unique QR factors.",
            (("图中两步计算", [r"$a_1=(1,0),\ a_2=(1,1)$。", r"$u_1=a_1,\ v_2=a_2-u_1(u_1^*a_2)=(0,1)$。", r"$u_2=v_2/\|v_2\|=(0,1)$。"]),
             ("推广到第 j 列", [r"$v_j=a_j-\sum_{i<j}u_i(u_i^*a_j)$。", r"$r_{jj}=\|v_j\|>0,\quad u_j=v_j/r_{jj}$。", r"$A=UR,\quad U^*U=I$；独立性保证 $v_j\ne0$。"])),
            (("Two steps in the example", ["Start with the two input columns above.", "Subtract the component parallel to the first unit vector.", "Normalize the residual to obtain the second unit vector."]),
             ("The general column", ["Subtract all projections onto earlier unit vectors.", "The residual norm is the positive diagonal entry.", "Column independence ensures that every residual is nonzero."])),
            "正交 Orthogonal · 规范化 Normalize · 投影 Projection · 酉 Unitary"),
        "38_projection_adjoint": (
            "幂等只保证投影，自伴才保证正交投影",
            "Idempotence gives a projection; self-adjointness makes it orthogonal",
            "同一向量 x=(1,2)，沿不同补空间投到横轴，得到不同结果。",
            "Project the same vector onto the horizontal axis along two different complements.",
            "左图的核与像不正交；右图满足 Q=Q*=Q²，残差与像正交。",
            "The left kernel is oblique to the image; the right residual is orthogonal to the image.",
            (("斜投影", [r"$P(x_1,x_2)=(x_1+x_2,0),\ P^2=P$。", r"$Px=(3,0),\quad x-Px=(-2,2)$。", r"$\ker P=\operatorname{span}(-1,1)$，且 $P\ne P^*$。"]),
             ("正交投影", [r"$Q(x_1,x_2)=(x_1,0),\ Q=Q^*=Q^2$。", r"$Qx=(1,0),\quad x-Qx=(0,2)$。", r"一般地 $Q=UU^*$，其中 $U^*U=I_r$。"])),
            (("Oblique projection", ["The displayed matrix is idempotent.", "Its residual follows the oblique kernel direction.", "The kernel is not perpendicular to the image."]),
             ("Orthogonal projection", ["The displayed matrix is both self-adjoint and idempotent.", "Its residual is vertical and perpendicular to the image.", "Orthonormal image columns give the factorization shown."])),
            "幂等 Idempotent · 自伴 Self-adjoint · 像 Image · 核 Kernel"),
        "39_normal_schur": (
            "Schur 形：严格上三角部分给出不等式的差额",
            "Schur form: the strict upper triangle measures the inequality gap",
            "特征值相同，矩阵也可能有不同的 Frobenius 范数。",
            "Matrices with identical eigenvalues can have different Frobenius norms.",
            "差额为零等价于正规；这里的三角化必须使用酉相似，才能保持 Frobenius 范数。",
            "A zero gap characterizes normality. Unitary similarity preserves the Frobenius norm.",
            (("从三角形读出差额", [r"$t_{11}=1,\ t_{12}=2,\ t_{21}=0,\ t_{22}=3$。", r"$\sum_i|\lambda_i|^2=10,\quad\|T\|_F^2=14$。", r"差额 $14-10=|2|^2=4$，故 $T$ 不正规。"]),
             ("一般判据", [r"$T=Q^*AQ,\ Q^*Q=I$，$T$ 上三角。", r"$\|A\|_F^2-\sum_i|\lambda_i|^2=\sum_{i<j}|t_{ij}|^2$。", r"差额为零时 $T$ 对角，列向量组成正交规范特征基。"])),
            (("Read the gap", ["The triangular matrix has eigenvalues one and three.", "The squared eigenvalue sum is ten; the squared norm is fourteen.", "The nonzero gap proves this matrix is not normal."]),
             ("The general criterion", ["Use an upper triangular Schur form with a unitary basis.", "Only strict upper triangular entries contribute to the gap.", "Zero gap gives a diagonal form and an orthonormal eigenbasis."])),
            "正规 Normal · 酉相似 Unitary similarity · 差额 Gap · 特征基 Eigenbasis"),
        "40_hermitian_positive": (
            "正定 Hermitian 型：等值线、特征值与主子式",
            "Positive Hermitian forms: level sets, eigenvalues and principal minors",
            "同一二次型可从几何形状、谱和分解三个角度验证。",
            "Verify one quadratic form through its geometry, spectrum and factorization.",
            "正定检验使用顺序主子式；半正定一般要检查全部主子式，不能只看顺序主子式。",
            "Leading principal minors test positive definiteness; semidefiniteness requires all principal minors.",
            (("图中正定例子", [r"$H_{11}=H_{22}=2,\ H_{12}=H_{21}=1$。", r"$\lambda(H)=\{1,3\},\quad\Delta_1=2,\ \Delta_2=3$。", r"$x^*Hx=3|y_1|^2+|y_2|^2>0$，$x\ne0$。"]),
             ("判断前先查 Hermitian", [r"$H=H^*,\ H\succ0\Longleftrightarrow\lambda_j(H)>0$。", r"$H\succ0\Longleftrightarrow H=R^*R$，$R$ 上三角、正对角。", r"$H\succeq0\Longleftrightarrow H=S^*S$；允许 $S$ 奇异。"])),
            (("The positive example", ["The displayed real symmetric matrix is Hermitian.", "Both eigenvalues and both leading principal minors are positive.", "Rotating coordinates yields a sum of positive squares."]),
             ("Check the Hermitian condition first", ["Positive definiteness is equivalent to a positive spectrum.", "The positive definite case has a nonsingular Cholesky factor.", "A semidefinite Gram factor may be singular."])),
            "正定 Positive definite · 主子式 Principal minor · 等值线 Level set"),
    }
    for key, record in records.items():
        zh, en, sub, esub, foot, efoot, panels, epanels, terms = record
        api['DETAILS'][key] = panels
        api['ENGLISH'][key] = (en, esub, efoot, epanels)
        api['LABEL_TERMS'][key] = terms

    def start(key):
        r = records[key]
        fig, ax = canvas(r[0], r[2])
        note(fig, r[4])
        return fig, ax

    @diagram('36_inner_product_gram', records['36_inner_product_gram'][0])
    def gram():
        fig, ax = start('36_inner_product_gram')
        arrow(ax, (.8, 1.7), (4.2, 1.7), MUTED)
        arrow(ax, (.8, 1.7), (.8, 5.1), MUTED)
        arrow(ax, (.8, 1.7), (3.7, 1.7), BLUE)
        arrow(ax, (.8, 1.7), (3.7, 4.6), TEAL)
        label(ax, 2.2, 1.3, r'$b_1=(1,0)$', 17, BLUE)
        label(ax, 2.5, 4.9, r'$b_2=(1,1)$', 17, TEAL)
        label(ax, 6.6, 5.1, '基的 Gram 矩阵 / Gram matrix', 14, BLUE)
        matrix(ax, 5.65, 2.65, [[1, 1], [1, 2]], cell=.85)
        label(ax, 6.5, 2.1, r'$G=B^*B$', 20, BLUE)
        box(ax, 8.2, 2.4, 3.4, 2.4, color=TEAL)
        label(ax, 9.9, 4.3, '坐标中的内积 / Coordinates', 13, TEAL)
        label(ax, 9.9, 3.5, r'$\langle Bx,By\rangle=x^*Gy$', 17)
        label(ax, 9.9, 2.8, r'$\|Bx\|^2=x^*Gx$', 17)
        label(ax, 6.1, .55, r'$x=(0,1)^T:\quad x^*x=1,\qquad x^*Gx=2$', 20, ORANGE)
        return fig

    @diagram('37_gram_schmidt_unitary', records['37_gram_schmidt_unitary'][0])
    def gs():
        fig, ax = start('37_gram_schmidt_unitary')
        label(ax, 2.7, 5.6, '原始列 / Input columns', 17, BLUE)
        label(ax, 9.0, 5.6, '正交规范列 / Orthonormal columns', 17, TEAL)
        for ox in (1.2, 7.5):
            arrow(ax, (ox, 2), (ox+3, 2), MUTED)
            arrow(ax, (ox, 2), (ox, 5), MUTED)
        arrow(ax, (1.2, 2), (3.8, 2), BLUE)
        arrow(ax, (1.2, 2), (3.8, 4.6), ORANGE)
        arrow(ax, (7.5, 2), (10.1, 2), BLUE)
        arrow(ax, (7.5, 2), (7.5, 4.6), TEAL)
        label(ax, 3.1, 1.55, r'$a_1=(1,0)$', 16, BLUE)
        label(ax, 3.2, 4.9, r'$a_2=(1,1)$', 16, ORANGE)
        label(ax, 9.2, 1.55, r'$u_1=(1,0)$', 16, BLUE)
        label(ax, 8.5, 4.9, r'$u_2=(0,1)$', 16, TEAL)
        arrow(ax, (4.6, 3.4), (6.7, 3.4), PURPLE)
        label(ax, 5.65, 4.2, '减投影\nSubtract', 15, PURPLE)
        label(ax, 6.1, .55, r'$A=UR,\qquad U=I,\qquad r_{11}=r_{12}=r_{22}=1,\ r_{21}=0$', 20)
        return fig

    @diagram('38_projection_adjoint', records['38_projection_adjoint'][0])
    def project():
        fig, ax = start('38_projection_adjoint')
        for ox in (1, 7):
            arrow(ax, (ox-.4, 1.4), (ox+4, 1.4), MUTED)
            arrow(ax, (ox, .7), (ox, 4.9), MUTED)
            arrow(ax, (ox, 1.4), (ox+1, 3.4), BLUE)
            label(ax, ox+1, 3.8, r'$x=(1,2)$', 16, BLUE)
        label(ax, 3, 5.35, '斜投影 / Oblique', 19, ORANGE)
        label(ax, 9, 5.35, '正交投影 / Orthogonal', 19, TEAL)
        arrow(ax, (1, 1.4), (4, 1.4), ORANGE)
        arrow(ax, (4, 1.4), (2, 3.4), PURPLE)
        label(ax, 3.5, .9, r'$Px=(3,0)$', 17, ORANGE)
        label(ax, 4.5, 3.2, r'$x-Px$', 17, PURPLE)
        arrow(ax, (7, 1.4), (8, 1.4), TEAL)
        arrow(ax, (8, 1.4), (8, 3.4), PURPLE)
        label(ax, 8.4, .9, r'$Qx=(1,0)$', 17, TEAL)
        label(ax, 10, 2.8, r'$x-Qx$', 17, PURPLE)
        ax.plot([8.25, 8.25, 8], [1.4, 1.65, 1.65], color=TEAL)
        label(ax, 3, .15, r'$P^2=P,\quad P\ne P^*$', 18, ORANGE)
        label(ax, 9, .15, r'$Q^2=Q=Q^*$', 18, TEAL)
        return fig

    @diagram('39_normal_schur', records['39_normal_schur'][0])
    def schur():
        fig, ax = start('39_normal_schur')
        label(ax, 3, 5.5, '上三角但不正规 / Nonnormal triangular', 17, ORANGE)
        label(ax, 9, 5.5, '对角且正规 / Normal diagonal', 17, TEAL)
        matrix(ax, 2.1, 2.7, [[1, 2], [0, 3]], .9, {(0, 1):ORANGE})
        matrix(ax, 8.1, 2.7, [[1, 0], [0, 3]], .9, {(0, 0):TEAL,(1,1):TEAL})
        label(ax, 3, 2.2, r'$\|T\|_F^2=14,\quad\sum|\lambda_i|^2=10$', 17, ORANGE)
        label(ax, 9, 2.2, r'$\|D\|_F^2=10,\quad\sum|\lambda_i|^2=10$', 17, TEAL)
        box(ax, 1, .35, 10, 1.1, color=PURPLE)
        label(ax, 6, .9, r'$\|A\|_F^2-\sum_i|\lambda_i|^2=\sum_{i<j}|t_{ij}|^2\geq0$', 23, PURPLE)
        return fig

    @diagram('40_hermitian_positive', records['40_hermitian_positive'][0])
    def positive():
        fig, ax = start('40_hermitian_positive')
        arrow(ax, (.5, 3), (5.5, 3), MUTED)
        arrow(ax, (3, .5), (3, 5.5), MUTED)
        t = np.linspace(0, 2*np.pi, 240)
        for c, color in ((1, BLUE), (2, TEAL), (4, PURPLE)):
            u=np.sqrt(c/3)*np.cos(t);v=np.sqrt(c)*np.sin(t)
            ax.plot(3+(u+v)/np.sqrt(2),3+(u-v)/np.sqrt(2),color=color,lw=2)
        label(ax, 2.8, 5.8, r'$x^THx=1,2,4\quad(x\in\mathbb{R}^2)$', 17, BLUE)
        label(ax, 5.2, 2.6, r'$x_1$', 15)
        label(ax, 3.4, 5.2, r'$x_2$', 15)
        matrix(ax, 7.2, 3.45, [[2, 1], [1, 2]], .8)
        label(ax, 9.9, 4.3, r'$H=H^*$', 22, BLUE)
        label(ax, 9.1, 2.65, r'$\lambda_1=1,\quad\lambda_2=3$', 19, TEAL)
        label(ax, 9.1, 1.85, r'$\Delta_1=2>0,\quad\Delta_2=3>0$', 19, ORANGE)
        label(ax, 9.1, .9, r'$H\succ0\quad\Longleftrightarrow\quad x^*Hx>0\ (x\ne0)$', 18, PURPLE)
        return fig
