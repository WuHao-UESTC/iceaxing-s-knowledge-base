# 10.1 MIMO 系统

MIMO（Multiple Input Multiple Output）——点对点链路的收发双方均配备多天线。相比仅单端多天线的分集系统，MIMO 带来显著增益：**不增加发射功率或带宽即可大幅提升数据率**。代价：额外天线的部署成本、空间需求（尤其手持设备）、多维信号处理的复杂度。

本章涵盖 MIMO 容量（不同信道知识假设下）、MIMO 最优编解码、非编码系统的传输策略。10.2 节讨论空时编码，10.3 节讨论智能天线。

## 10.1.1 窄带多天线系统模型

$n$ 根发射天线，$m$ 根接收天线，窄带（平坦衰落）点对点通信系统。

> 【插入 Goldsmith 图 10.1】MIMO 系统框图

离散时间模型：

$$\begin{bmatrix} y_1 \\ \vdots \\ y_m \end{bmatrix} = \begin{bmatrix} h_{11} & \dots & h_{1n} \\ \vdots & \ddots & \vdots \\ h_{m1} & \dots & h_{mn} \end{bmatrix} \begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} + \begin{bmatrix} N_1 \\ \vdots \\ N_m \end{bmatrix}$$

简写为：

$$\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{N}$$

- $\mathbf{x}$：$n$ 维发射符号向量
- $\mathbf{y}$：$m$ 维接收符号向量
- $\mathbf{N}$：$m$ 维 AWGN 向量，协方差矩阵归一化为单位阵（不失一般性）
- $\mathbf{H}$：$m \times n$ 信道矩阵，元素 $h_{ij}$ 是从发射天线 $j$ 到接收天线 $i$ 的信道增益——零均值复圆高斯随机变量（Rayleigh 衰落）

**CSI 假设**：接收端能完美估计 $\mathbf{H}$，即每一时刻 $\mathbf{H}$ 在接收端已知。时间依赖性被省略，但 $\mathbf{x}$、$\mathbf{y}$、$\mathbf{N}$、$\mathbf{H}$ 均为随机过程。

**发射功率约束**：

$$\sum_{i=1}^{n} \mathrm{E}[x_i x_i^*] = P \quad \text{或等价地} \quad \operatorname{trace}(\mathrm{E}[\mathbf{x}\mathbf{x}^\dagger]) = P$$

⚡ MIMO 信道的关键特征：一个 $m \times n$ 的矩阵 $\mathbf{H}$ 取代了 SISO 中的标量信道增益。这不仅是维度增加——矩阵的**秩**决定了可同时传输的独立数据流数，矩阵的**奇异值**决定了各流的有效 SNR。

## 10.1.2 发射预编码与接收成形

$R$ symbols/s 的输入数据流被分解为 $r$ 路并行独立数据流，产生 $r$ 元组 $\tilde{\mathbf{x}}$，速率为 $R/r$ symbols/s。天线实际输入 $\mathbf{x}$ 通过对 $\tilde{\mathbf{x}}$ 做线性变换产生：

$$\mathbf{x} = \mathbf{M} \tilde{\mathbf{x}}$$

其中 $\mathbf{M}$ 为 $n \times r$ 固定矩阵——**发射预编码（transmit precoding）**。

接收端对称操作——**接收成形（receiver shaping）**：将信道输出乘以 $r \times n$ 矩阵 $\mathbf{F}$。

> 【插入 Goldsmith 图 10.2】发射预编码与接收成形

整体系统：

$$\begin{aligned} \tilde{\mathbf{y}} &= \mathbf{F} \mathbf{y} \\ &= \mathbf{F} \mathbf{H} \mathbf{x} + \mathbf{F} \mathbf{N} \\ &= \mathbf{F} \mathbf{H} \mathbf{M} \tilde{\mathbf{x}} + \mathbf{F} \mathbf{N} \end{aligned}$$

### 输入协方差的秩 = 独立数据流数

输入协方差矩阵 $\mathbf{Q} = \mathrm{E}[\mathbf{x}\mathbf{x}^\dagger]$ 的秩等于 $r$——同时传输的独立数据流数。例如，若 $\mathbf{x} = \mathbf{M}x$（$\mathbf{M}$ 为常向量），则 $\mathbf{Q} = \mathrm{E}[xx^*] \mathbf{M}\mathbf{M}^\dagger$ 秩为 1——仅传输一路数据流。

### 解码复杂度的核心矛盾

最优解码需最大似然（ML）解调。若调制符号取自字母表 $\mathcal{X}$（大小 $|\mathcal{X}|$），ML 解调需在 $|\mathcal{X}|^r$ 个可能的输入 $r$ 元组中穷搜。

⚡ **无发射端 CSI（CSIT）时，对于非平凡 $\mathbf{H}$，解码复杂度无法降低**——随 $r$（= 同时传输的独立流数）指数增长。即使天线数不大，这通常也是不可承受的。

但若 $\mathbf{H}$ 在接收端测得并反馈至发射端 → 解码复杂度可大幅降低。这正是下一节（10.1.3）并行分解的动机：**用 CSIT 换取解码复杂度的指数级降低**。

## 10.1.3 MIMO 信道的并行分解

本节考虑**完美 CSIT**——收发双方在每一时刻都知道瞬时 $\mathbf{H}$。

### SVD 分解

对信道矩阵做奇异值分解（SVD）：

$$\mathbf{H} = \mathbf{U} \boldsymbol{\Lambda} \mathbf{V}^\dagger \tag{10.1}$$

- $\mathbf{U}$：$m \times m$ 酉矩阵（$\mathbf{U}\mathbf{U}^\dagger = \mathbf{I}_m$）
- $\mathbf{V}$：$n \times n$ 酉矩阵（$\mathbf{V}\mathbf{V}^\dagger = \mathbf{I}_n$）
- $\boldsymbol{\Lambda}$：$m \times n$ 对角矩阵，对角元为 $\mathbf{H}$ 的奇异值 $\sigma_i$

### 预编码与接收成形的选择

选择 $\mathbf{M} = \mathbf{V}^\dagger$（发射预编码）和 $\mathbf{F} = \mathbf{U}^\dagger$（接收成形）：

$$\begin{aligned} \tilde{\mathbf{y}} &= \mathbf{U}^\dagger \mathbf{U} \boldsymbol{\Lambda} \mathbf{V} \mathbf{V}^\dagger \tilde{\mathbf{x}} + \mathbf{U}^\dagger \mathbf{N} \\ &= \boldsymbol{\Lambda} \tilde{\mathbf{x}} + \tilde{\mathbf{N}} \end{aligned}$$

> 【插入 Goldsmith 图 10.3】MIMO 信道的并行分解

### 核心结果：$r$ 个并行无干扰 SISO 信道

MIMO 信道被转化为 $r \leq \min(m, n)$ 个**并行、互不干扰的 SISO 信道**：

$$\tilde{y}_i = \sigma_i \tilde{x}_i + \tilde{N}_i, \quad i = 1, \dots, r$$

其中 $\tilde{\mathbf{N}} = \mathbf{U}^\dagger \mathbf{N}$——乘以酉矩阵不改变白高斯噪声的分布，$\tilde{\mathbf{N}}$ 与 $\mathbf{N}$ 同分布。

### 复杂度降低：指数 → 线性

ML 解调复杂度从 $|\mathcal{X}|^r$ 降至 $r|\mathcal{X}|$——**从指数级降为线性**。因为各 SISO 信道互不干扰，可独立解调。

⚡ 这是 MIMO 通信理论中最优雅的结果之一：**通过酉变换对信道做"对角化"，将空间维度上的交叉干扰转化为并行的标量信道**。SVD 给出了最优的 $\mathbf{M}$ 和 $\mathbf{F}$——$\mathbf{V}^\dagger$ 在发射端将信号"对准"信道的特征方向，$\mathbf{U}^\dagger$ 在接收端将信号从特征方向"分离"出来。

这个并行分解结构不仅是容量分析的基础，也直接指导了实际 MIMO 收发机的设计——多载波调制中的自适应加载在空间维度的对应物。

## 10.1.4 MIMO 信道容量

基于并行分解，MIMO 信道容量（收发双方完美 CSI）有简洁刻画。

### 容量公式

给定发射协方差 $\mathbf{Q} = \mathrm{E}[\mathbf{x}\mathbf{x}^\dagger]$（满足 $\operatorname{Tr}(\mathbf{Q}) \leq P$），MIMO 信道的互信息为 $\log|\mathbf{I} + \mathbf{H}\mathbf{Q}\mathbf{H}^\dagger|$。容量在所有满足功率约束的 $\mathbf{Q}$ 上最大化：

$$C = \max_{\mathbf{Q}: \operatorname{Tr}(\mathbf{Q}) \leq P} \log |\mathbf{I} + \mathbf{H}\mathbf{Q}\mathbf{H}^\dagger| \tag{10.2}$$

将 SVD (10.1) 代入并利用酉矩阵性质，化简为在各并行 SISO 信道上最优功率分配的标量和：

$$C = \max_{\{P_i\}: \sum_i P_i \leq P} \sum_i B \log\left(1 + \frac{\lambda_i^2 P_i}{N_0 B}\right) \tag{10.3}$$

其中 $\lambda_i = \sigma_i$ 是 $\mathbf{H}$ 的奇异值，$\lambda_i^2$ 是第 $i$ 个空间子信道的功率增益。

### 与之前容量公式的统一

(10.3) 与平坦衰落容量 (4.9) 和频率选择性容量 (4.23) **形式完全相同**——都是一组并行 AWGN 信道上的功率最优分配问题。区别在于"子信道"的来源：

| 场景 | 子信道来源 | 注水轴 |
|------|-----------|--------|
| 平坦衰落（时间注水） | $\gamma$ 的不同取值（概率） | 时间 |
| 频率选择性（频率注水） | $H(f)$ 的不同频率段 | 频率 |
| **MIMO（空间注水）** | $\mathbf{H}$ 的奇异值 | 空间 |

### 空间域注水

最优功率分配同样是注水：

$$\frac{P_i}{P} = \begin{cases} \frac{1}{\gamma_0} - \frac{1}{\gamma_i} & \gamma_i \geq \gamma_0 \\ 0 & \gamma_i < \gamma_0 \end{cases} \tag{10.4}$$

其中 $\gamma_i = \lambda_i^2 P/(N_0 B)$ 是将全部功率分配给第 $i$ 个空间子信道时的 SNR。$\gamma_0$ 为公共截止值，由功率约束确定。

容量：

$$C = \sum_{i: \gamma_i \geq \gamma_0} B \log(\gamma_i / \gamma_0) \tag{10.5}$$

### 容量缩放律

MIMO 信道最多支持 $r_{\max} = \min(m, n)$ 个非零奇异值，因此最大复用增益（spatial multiplexing gain）= $\min(m, n)$。

⚡ 在丰富散射（rich scattering）环境中，$\mathbf{H}$ 满秩，奇异值近似相等 → 容量大致为 SISO 容量的 $\min(m, n)$ 倍。这就是第 4 章末尾提到的"容量线性缩放"——不增加带宽和功率，仅靠多天线即可获得 $\min(m, n)$ 倍容量增益。

→ 这是无线通信近二十年来最重要的理论突破之一 $[27, 28, 29]$。MIMO 将"对抗衰落的分集"和"提升容量的空间复用"统一在同一个框架中。详见 [[Goldsmith-无线通信/第4章-无线信道容量#4.2.5 接收分集下的容量|第 4 章 4.2.5 节 MIMO 容量预览]]。

## 10.1.5 波束成形（Beamforming）

### 动机：无瞬时 CSIT 时的低复杂度策略

当发射端**不知道瞬时信道**时，无法做 SVD 并行分解（需要 $\mathbf{M} = \mathbf{V}^\dagger$）。解码复杂度指数级增长 → 策略是保持 $r$ 小。$r = 1$ 的特例——输入协方差矩阵秩为 1——称为**波束成形（beamforming）**。

此时预编码矩阵退化为列向量 $\mathbf{M} = \mathbf{c}$——**波束成形向量**。

> 【插入 Goldsmith 图 10.4】波束成形 MIMO 信道

### 空间匹配滤波

接收端用空间匹配滤波器 $\mathbf{c}^\dagger \mathbf{H}^\dagger / \|\mathbf{c}^\dagger \mathbf{H}^\dagger\|$ 处理：

$$\begin{aligned} \tilde{y} &= \frac{\mathbf{c}^\dagger \mathbf{H}^\dagger}{\|\mathbf{c}^\dagger \mathbf{H}^\dagger\|} \mathbf{y} \\ &= \frac{\mathbf{c}^\dagger \mathbf{H}^\dagger}{\|\mathbf{c}^\dagger \mathbf{H}^\dagger\|} \mathbf{H} \mathbf{c} \, x + \frac{\mathbf{c}^\dagger \mathbf{H}^\dagger}{\|\mathbf{c}^\dagger \mathbf{H}^\dagger\|} \mathbf{N} \\ &= \|\mathbf{H} \mathbf{c}\| \, x + \tilde{N} \end{aligned}$$

其中 $\tilde{N}$ 为零均值、单位方差的 AWGN。

波束成形将整个 MIMO 信道折叠为**单个 SISO AWGN 信道**。ML 解调复杂度仅为 $|\mathcal{X}|$——与 SISO 相同，与天线数无关。

### 瞬时 SNR

给定 $\mathbf{c}$ 和 $\mathbf{H}$，接收 SNR 为：

$$\text{SNR} = \mathbf{c}^\dagger \mathbf{H}^\dagger \mathbf{H} \mathbf{c} \cdot \mathrm{E}[xx^*] = \mathbf{c}^\dagger \mathbf{H}^\dagger \mathbf{H} \mathbf{c} \cdot P$$

### 最优波束成形向量的求解

**优化准则**：选择 $\mathbf{c}$ 使**平均 SNR**（在 $\mathbf{H}$ 的分布上取期望）最大化：

$$\mathrm{E}[\text{SNR}] = P \, \mathbf{c}^\dagger \mathrm{E}[\mathbf{H}^\dagger \mathbf{H}] \, \mathbf{c}$$

约束：$\mathbf{c}^\dagger \mathbf{c} = 1$（满足发射功率约束）。

解：$\mathbf{c}$ = 正定矩阵 $\mathrm{E}[\mathbf{H}^\dagger \mathbf{H}]$ 的**单位范数主特征向量**（最大特征值对应的特征向量）。

这是经典的 Rayleigh 商最大化问题——解是"将发射能量对准平均意义上最强的空间方向"。

### 三种衰落场景下的波束成形行为

#### 1. i.i.d. 衰落

各收发天线对之间的衰落独立同分布 → $\mathrm{E}[\mathbf{H}^\dagger \mathbf{H}]$ 是单位阵的标量倍 → 任意单位范数的 $\mathbf{c}$ 都最优。

不失一般性取 $\mathbf{c} = [1, 0, 0, \dots, 0]^T$——**只用一根发射天线**。

⚡ i.i.d. 衰落下，多发射天线在平均 SNR 意义上**无增益**。但接收 SNR**与接收天线数成正比**——多接收天线确实提升平均接收 SNR。

**物理直觉**：i.i.d. 意味着所有发射-接收路径在统计上完全等价，没有哪个方向"更好"。所有发射功率可集中在任意一根天线上。接收端用多天线做匹配滤波 → 接收分集增益。

#### 2. 独立衰落

$\mathbf{H}$ 各行独立（各接收天线看到的信道向量独立），每行的协方差矩阵 $\mathbf{K}_i$ 是对角阵。则 $\mathrm{E}[\mathbf{H}^\dagger \mathbf{H}] = \sum_{i=1}^m \mathbf{K}_i$ 也是对角阵。

主特征向量仍为 $\mathbf{c} = [0, \dots, 0, 1, 0, \dots, 0]^T$——**选择对全部接收天线具有最大平均信道功率和的发射天线**。同样，多接收天线提升接收 SNR。

#### 3. 相关衰落

$\mathrm{E}[\mathbf{H}^\dagger \mathbf{H}]$ 的主特征向量**可能用到所有发射天线**。

⚡ 相关衰落下，多发射天线**有**增益——空间相关结构意味着存在"优势方向"，将功率分配到与该方向对齐的多根天线可获得更高的平均 SNR。此时**发射分集和接收分集都提供增益**。

### 波束成形 vs 空间复用

| 策略 | $r$ | 解码复杂度 | 需要 CSIT？ | 增益类型 |
|------|-----|-----------|------------|---------|
| **波束成形** | 1 | $O(\vert\mathcal{X}\vert)$ — 线性 | 仅需 $\mathrm{E}[\mathbf{H}^\dagger \mathbf{H}]$ | 分集增益（SNR） |
| **空间复用（注水）** | $\min(m,n)$ | $O(r\vert\mathcal{X}\vert)$ — 线性（有 CSIT 时） | 瞬时 $\mathbf{H}$ | 复用增益（容量 $\times r$） |

⚡ 波束成形和空间复用代表了 MIMO 的两种极限使用模式：**牺牲所有复用换取简单实现和分集增益**（波束成形）vs **充分利用所有空间维度换取最大容量**（空间复用）。实际系统在两者间做折中——$r$ 的选择即是在分集增益和复用增益间做权衡。→ 空时编码（10.2 节）在更一般框架下讨论这个折中。

# 10.2 空时编码（Space-Time Codes）

MIMO 容量结果（10.1.4 节）表明：多天线系统即使在发射端不知道瞬时信道时，互信息也可随天线数线性增长。这激发了**空时编码**的研究——设计实际可用的编码方案以逼近这一巨大的理论容量。

## 核心挑战：无 CSIT 时的多维编码

10.1.3 节展示了若有**完美 CSIT** → SVD 将 MIMO 信道对角化为并行 SISO 信道 → 可复用成熟的 SISO 编解码技术。

但**发射端不知道瞬时信道**时：
- 无法做 SVD 分解
- 编码必须**固有地在空间维度上**工作
- **码字是矩阵（而非向量）**——行对应天线，列对应时间
- 最优 ML 解码复杂度随天线数**指数增长**

⚡ 从向量编码到矩阵编码是质的飞跃。维度增加不仅提升了可达速率上限，也从根本上改变了编码理论的问题陈述——码字设计的搜索空间、距离度量、性能分析全变了。

## 研究方向

空时编码是一个**庞大的研究领域**，以下分支代表了主要探索方向：

**分层空时编码（Layered Space-Time Codes）**：将每根天线的传输视为独立用户，用传统标量码 + 多用户检测技术联合解调。实现相对简单，但作为次优方案通常承受显著的性能损失。

**空时编码 vs 空时信号处理**：
- **空时编码**：设计能充分利用空间维自由度的编码结构
- **空时信号处理**：聚焦估计、均衡和滤波技术，在 MIMO 信道上精确估计传输信号

⚡ 10.1.5 节波束成形代表了一种重要的特例——发射端不利用所有空间维度的自由度（$r=1$），以容量换取极简实现。空时编码则试图在 $r=1$（纯波束成形）和 $r=\min(m,n)$（全空间复用）之间找到最佳折中点。

## 理论与实践的差距

附录 10.C 提供了 Foschini-Gans 结果的关键洞察：对于 $n \times n$ i.i.d. Rayleigh MIMO 信道，即使仅接收端知道信道、发射端平均分配功率，互信息仍随 $n$ 线性增长：

$$\frac{I_n}{n} \to \int_0^4 \log(1 + P\lambda) \, g(\lambda) \, d\lambda$$

其中 $g(\lambda) = \frac{1}{\pi}\sqrt{1/\lambda - 1/4}$（$0 \leq \lambda \leq 4$）——大随机矩阵理论中 Marcenko-Pastur 律的特例。

关键事实：
- 线性增长在**天线数不多时也已观察得到**——不仅是大 $n$ 的渐近结果
- 即使存在天线间**相关衰落**，容量增长率仍为线性（虽然斜率减小）
- 近期结果表明：仅有信道相关矩阵信息（无瞬时 CSI）就能带来**显著容量增益**——这对 SISO 系统不成立
- 某些场景下**波束成形已接近信道容量** → 复杂度仅为全向量编码的一小部分

⚡ 这些新结果表明：MIMO 容量的理论承诺**可以通过合理复杂度的实际技术实现**——空时编码不是纯理论玩具，而是在实际系统设计中逐渐落地的方向。

# 10.3 智能天线（Smart Antennas）

## 基本概念

智能天线 = **天线阵列 + 空间域 + 时间域联合信号处理**。空间处理为系统设计引入了一个全新的自由度，潜在收益包括：

- **覆盖扩展**（range extension）
- **容量增强**
- **更高数据率**
- **更好 BER 性能**

## 为什么需要空间处理

无线通信高性能的两大阻碍：

| 损害 | 来源 | 系统影响 |
|------|------|----------|
| **同信道干扰（CCI）** | 其他用户 | 限制系统容量（可服务的用户数） |
| **多径效应 → ISI + 衰落** | 反射/散射/绕射 | 限制数据率，恶化 BER |

**智能天线的核心洞察**：干扰信号和多径分量通常从**不同方向**到达接收端 → 空间处理可**利用到达角差异**：

1. **抑制同信道干扰** → 提升系统容量（更多用户可被服务）
2. **衰减多径分量** → 减少 ISI 和平坦衰落 → 更高数据率、更好 BER

⚡ 这与第 7 章分集的视角一致，但智能天线更进一步——分集被动利用多天线接收到的多个独立衰落副本，而智能天线**主动在空间维度上做滤波**，选择性接收有用信号方向、抑制干扰方向。

## 系统定位

**手持终端**：复杂度 + 天线阵列物理空间需求 → 下一代系统中仍不太可能在小型、轻量、低功耗手持设备中部署。

**基站**：可以使用天线阵列 + 发射端空时处理来降低同信道干扰和多径，获得与接收端智能天线类似的性能优势。这是智能天线的主要应用场景。

⚡ 基站端的智能天线部署符合无线系统设计的基本原则：**将复杂度推向基础设施，保持终端简单**。这与 [[Goldsmith-无线通信/第1章-无线通信导论#1.3 技术挑战|第 1 章讨论的终端硬件约束]] 完全一致——处理负担转移至固定基站，代价是瓶颈与单点故障。

## MIMO vs 智能天线

| 维度 | MIMO (10.1) | 智能天线 (10.3) |
|------|------------|----------------|
| 天线配置 | 收发双方多天线 | 通常指接收端阵列（或发射端赋形） |
| 核心目标 | 提升链路容量（空间复用） | 抑制干扰 + 改善链路质量 |
| 处理方法 | SVD 并行分解 / 空时编码 | 空间滤波（波束指向 + 零陷） |
| 理论基础 | 信息论（容量公式） | 阵列信号处理（波达方向估计） |
| 对信道的利用 | 将多径视为额外自由度 | 将多径视为需抑制的损害 |

实际上两者正**逐步融合**——MIMO 系统可以利用智能天线的空间滤波思想降低干扰，智能天线也可用 MIMO 的空间复用提升容量。现代基站同时追求两者的收益：**用波束成形对抗干扰，用空间复用提升容量**。