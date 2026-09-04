---
title: 基于 FPGA 的双模式便携式实时多音色合成器键盘项目规划书
author: 项目技术规划稿
date: 2026-09
lang: zh-CN
toc: true
toc-depth: 3
toc-title: 目录
geometry: margin=2.2cm
fontsize: 10.5pt
documentclass: ctexart
mainfont: Noto Serif CJK SC
sansfont: Noto Sans CJK SC
monofont: Noto Sans Mono CJK SC
CJKmainfont: Noto Serif CJK SC
CJKsansfont: Noto Sans CJK SC
CJKmonofont: Noto Sans Mono CJK SC
header-includes:
  - |
    \usepackage{booktabs}
  - |
    \usepackage{longtable}
  - |
    \usepackage{array}
  - |
    \usepackage{float}
  - |
    \usepackage{fancyhdr}
  - |
    \usepackage{etoolbox}
  - |
    \apptocmd{\maketitle}{\thispagestyle{empty}\newpage}{}{}
  - |
    \pagestyle{fancy}
  - |
    \fancyhf{}
  - |
    \fancyhead[L]{FPGA 双模式便携式实时多音色合成器}
  - |
    \fancyhead[R]{项目规划书}
  - |
    \fancyfoot[C]{\thepage}
  - |
    \setlength{\headheight}{15pt}
  - |
    \setlength{\parindent}{2em}
  - |
    \setlength{\parskip}{0.35em}
---

# 文档说明

本文档面向“基于 FPGA 的实时多音色合成电子乐器引擎”方向，给出一套可直接用于项目立项、系统方案评审、团队分工、RTL 开发、PCB 设计、测试验证和现场答辩准备的完整工程规划。

项目核心不是把 FPGA 当作普通 MCU 使用，而是把 **演奏动作采集、手势识别、音符调度、逐样本音频合成、多声部混音、数字音频效果、可视化反馈和 I2S 输出** 组织成可验证、可并行、可流水的硬件数据通路。所有可闻音频均由 FPGA 根据实时演奏事件逐音、逐样本产生，不播放整段预录 PCM。

> **项目一句话定义：**
>
> 一台由 4x8 力度感应 RGB Pad 与二维电容触控演奏面组成、具备 PolyKey 与 Chord-Strum 双演奏模式、在 FPGA 内实现 32 复音/64 独立振荡器、物理拨弦建模、ADSR、DSP 效果、实时频谱与低延迟验证的便携式纯硬件电子乐器。

---

# 1. 项目背景与赛题理解

## 1.1 赛题核心约束

本项目需要围绕以下几条硬约束展开：

1. 至少 2 个独立可控演奏维度，并能完成选音、触发、拨弦、力度等实际演奏动作采集。
2. 音频合成完整通路由 FPGA HDL 硬件逻辑实现，逐样本实时运算。
3. 控制信号到音频输出总延迟不高于 10 ms，拓展目标不高于 5 ms。
4. 基础复音数不低于 4，具备单音变调、ADSR、多声部混音。
5. 禁止通过预录 PCM、整段录音触发、预置音频流等方式规避实时合成。
6. 拓展评分鼓励 32 复音、32 路以上加法分量、更多 FM 运算单元或并行物理建模单元。
7. 现场需要能够验证独立振荡器数量、频谱峰、纯硬件通路和低延迟。

因此，作品评价不能只看“能不能发声”，而要同时证明：

- **交互有创新性；**
- **硬件并行规模足够大；**
- **逐样本实时性确实存在；**
- **延迟可以被仪器测出来；**
- **振荡器数量可以被频谱和 RTL 双重证明；**
- **作品是乐器，而不是播放设备。**

## 1.2 设计策略

针对这些要求，本项目采取四条主线：

- 交互主线：32 个力度 Pad + XY 电容触摸演奏面 + 编码器；
- 合成主线：32 复音、每复音 2 振荡器，形成 64 个独立振荡器；
- 第二音源主线：并行 Karplus-Strong 物理弦模型服务于拨弦模式；
- 证明主线：专用 Oscillator Test、Latency Test、FFT/频谱和 RTL 统计页面。

---

# 2. 项目定位与产品形态

## 2.1 产品定位

产品定位为“便携式双范式演奏 FPGA 合成器”，而不是传统钢琴键盘的简单缩小版。

左侧 4x8 Pad 负责离散音乐语义：音符、和弦、调式、指法、力度和持续压力；右侧电容触摸板负责连续控制：滑音、颤音、音色变化、扫弦方向、扫弦速度和拨弦位置。

两种演奏模式分别服务于不同的音乐表达：

- **PolyKey Mode：** Pad 按下直接发声，触摸板实时改变音高、音色或效果参数；
- **Chord-Strum Mode：** Pad 只负责选择和弦或指法，不直接发声，手指划过触摸板中的虚拟弦区域后才真正触发音频。

这种设计使项目同时具备“电子合成器”和“新型数字拨弦乐器”的表现力。

## 2.2 建议外观尺寸

建议整机控制在以下范围：

| 项目       |                        建议值 |     |
| -------- | -------------------------: | --- |
| 整机宽度     |               300 - 340 mm |     |
| 整机深度     |               120 - 160 mm |     |
| 厚度       |                 25 - 35 mm |     |
| Pad 数量   |                     32，4x8 |     |
| 单 Pad 尺寸 |              22 - 28 mm 方形 |     |
| 触摸面尺寸    |  90 - 120 mm x 70 - 100 mm |     |
| OLED     | 1.3 - 2.4 英寸，建议 128x64 或更高 |     |
| 编码器      |                      4 个为宜 |     |
| 模式按键     |                    3 - 5 个 |     |

## 2.3 人机界面布局建议
![[FPGA双模式便携合成器项目规划书 2026-09-01 20.00.04.excalidraw]]
```text
+----------------------------------------------------------------+
|                                                                |
|  4x8 Pressure RGB Pad                  OLED      ENC1 ENC2      |
|                                                                |
|  [] [] [] [] [] [] [] []              +------+     O    O       |
|  [] [] [] [] [] [] [] []              |      |     O    O       |
|  [] [] [] [] [] [] [] []              | OLED |   ENC3 ENC4      |
|  [] [] [] [] [] [] [] []              +------+                  |
|                                                                |
|                             +------------------------------+   |
|  MODE  OCT-  OCT+  HOLD     |                              |   |
|                             |       XY TOUCH SURFACE       |   |
|                             |                              |   |
|                             +------------------------------+   |
|                                                                |
|         USB-C / DEBUG / LINE OUT / HEADPHONE / POWER           |
+----------------------------------------------------------------+
```

---

# 3. 总体目标与量化指标

## 3.1 分级目标

项目指标建议分为“保底指标、正式目标、冲分目标”三档，以控制研发风险。

| 指标       |   保底指标 |                    正式目标 |                 冲分目标 |
| -------- | -----: | ----------------------: | -------------------: |
| 独立演奏维度   |      2 |                    5 以上 |                 6 以上 |
| Pad 数量   |        |                         |                      |
| 基础复音     |      8 |                      32 |               32 或更高 |
| 独立振荡器    |     16 |                      64 |             128 运算单元 |
| 物理弦模型    |      4 |                       8 |                   16 |
| 采样率      | 48 kHz |                  96 kHz |               96 kHz |
| 音频位宽     | 24 bit |                  24 bit |               24 bit |
| 合成算法     |        |                         |                      |
| DSP 效果   |  Delay | Chorus + Delay + Reverb |             加动态滤波/饱和 |
| 实测延迟     | < 5 ms |               < 2 ms 目标 |              1 ms 量级 |
| OLED 可视化 |     参数 |                 波形 + 频谱 | 频谱 + Voice Map + 性能页 |
| RGB 指示   |   基础亮灭 |              压力/音阶/和弦反馈 |                 动画引导 |
| 现场验证     |    8 路 |                    64 路 |          64/128 运算单元 |

## 3.2 正式版建议指标

正式版建议统一按以下指标设计：

- 32 个独立力度感应 RGB Pad；
- XY 连续电容触控，输出 X、Y、速度、方向等特征；
- 32 复音；
- 64 独立振荡器；
- 8 路以上并行 Karplus-Strong 物理弦模型；
- 96 kHz / 24-bit Stereo I2S；
- ADSR、Pitch Bend、Aftertouch、FM Index、Filter、Pan；
- Chorus、Delay、Reverb 至少三种音频处理；
- OLED 实时波形和频谱；
- 控制到音频输出实际延迟目标 < 2 ms，保证 < 5 ms；
- 64 振荡器专用测试模式；
- 外部不提供任何可被直接播放的完整乐器 PCM 采样。

## 3.3 整理产品功能
### 基础声音部分
1. 音调
	- 钢琴全音调（pad部分按键设置）
2. 音色：
	- 自带音色：采用振荡器生成基础波形合成
	- 采样器（麦克风采集）
3. 响度
	- 通过按键轻重区分音量大小（按键采用霍尔效应等方案）
	- 加一个业余模式，即不区分
	- 加一个响度旋钮
4. 音效
	- 触摸板实现颤音，滑音，扫弦等
### 声音合成
1. 复音：>32路
2.  dsp
### 外观与功能
1. 1个触摸板 
2. 1个4 * 8的pad整列
3. 编码器旋钮4个
4. 轻触开关5个
5. 侧边按钮：开关
6. PAD侧面的预设方案切换按钮
7. 并口屏一块
8. 外接显示屏接口（显示）
9. 串口接口（配置接口）
10. I2S接口
---

# 4. FPGA 与主控平台选择

## 4.1 首选：Tang Mega 60K

正式版本优先推荐 Tang Mega 60K。其主要优势是：

- LUT4 约 59.9K；
- FF 约 59.9K；
- BSRAM 约 2.124 Mbit；
- 118 个 18x18 乘法器；
- 多个 PLL；
- 板载 DDR3 可用于非关键缓存或扩展实验；
- 无硬核 SoC，系统“纯 FPGA 硬件合成”的叙事更加干净。

对于 32 复音、64 振荡器、ADSR、基础 FM、8 路物理弦、混音、Delay/Chorus/Reverb 和 OLED 可视化，60K 是相对平衡的方案。

## 4.2 备选：Tang Mega 138K

若后期发现以下任一目标需要明显增加资源，可切换 Mega 138K：

- 32 Voice x 4 FM Operator；
- 128 个以上并行运算单元；
- 16 - 32 条物理弦；
- 更高阶混响网络；
- 更大规模实时 FFT；
- 多个并行滤波器组；
- 同时保留大量调试和可视化逻辑。

Mega 138K 官方资料给出的资源约为 138.2K LUT、6.12 Mbit BSRAM 和 298 个 18x18 乘法器。其资源冗余明显更大，但板上存在 RISC-V 硬核时，项目文档应明确：**硬核处理器不参与控制到音频的实时生成通路。**

## 4.3 为什么不优先 Nano 20K / Primer 25K

20K/25K 仍然适合早期算法验证，但作为最终版本会更容易受到以下约束：

- DSP 乘法器数量有限；
- BSRAM 不够宽裕；
- 64 独立振荡器 + 物理建模 + 效果 + 可视化同时存在时资源紧张；
- 需要频繁时分复用，降低“显式并行规模”的展示效果。

因此建议开发阶段可以在小板上单模块验证，但最终整机以 60K 为最低目标。

---

# 5. 系统总体架构

## 5.1 功能框图

```text
                 +-------------------------+
32 Pressure Pads | Pad Scan / ADC Interface|
---------------->| Baseline / Trigger      |
                 | Velocity / Aftertouch   |
                 +------------+------------+
                              |
                              v
                 +-------------------------+
XY Capacitive -->| Touch Scan Engine       |
Surface          | Centroid / Gesture      |
                 | X Y Vx Vy Speed Dir     |
                 +------------+------------+
                              |
Encoder/Button ------------------------------+
                              |               |
                              v               |
                 +-------------------------+  |
                 | Performance Engine      |<-+
                 | Mode FSM                |
                 | Scale / Chord Mapper    |
                 | Note Event Scheduler    |
                 +------------+------------+
                              |
               +--------------+----------------+
               |                               |
               v                               v
     +----------------------+        +----------------------+
     | Poly Synth Engine    |        | Physical String      |
     | 32 Voices            |        | Engine               |
     | 64 Oscillators       |        | 8/16 KS Strings      |
     | Wavetable / FM       |        | Pluck / Damping      |
     | Per-Voice ADSR       |        | Pitch / Position     |
     +----------+-----------+        +----------+-----------+
                |                               |
                +---------------+---------------+
                                v
                       +------------------+
                       | Stereo Mixer     |
                       | Pan / Gain       |
                       +--------+---------+
                                v
                       +------------------+
                       | Global Filter    |
                       +--------+---------+
                                v
                       +------------------+
                       | Chorus / Delay   |
                       +--------+---------+
                                v
                       +------------------+
                       | Reverb / Limiter |
                       +--------+---------+
                                v
                       +------------------+
                       | I2S TX 96 kHz    |
                       +--------+---------+
                                v
                            External DAC
                                |
                      Headphone / Line Out

         +---------------------------------------------+
         | Visualization / Diagnostics                 |
         | OLED UI / Waveform / Spectrum / Voice Map   |
         | RGB Pad Engine / Latency Test / OSC Test    |
         +---------------------------------------------+
```

## 5.2 数据通路原则

系统划分为三类数据通路：

### A. Fast Event Path

负责 Note On、Strum Crossing、Gate 等必须快速响应的事件，不经过长时间平滑滤波。

```text
Sensor Raw -> Threshold/Hysteresis -> Event -> Synth Trigger
```

### B. Expression Path

负责 Pressure、Aftertouch、Touch X/Y、滑动速度等连续参数，可使用 IIR、移动平均和非线性映射。

```text
Sensor Raw -> Filter -> Normalize -> Curve -> Parameter Router
```

### C. Audio Sample Path

固定由音频 sample tick 驱动，确保每个声部在规定时间内完成一次运算并进入混音器。

```text
sample_tick -> voice compute -> mix -> DSP -> I2S
```

三条路径互不阻塞，是降低演奏延迟和抖动的关键。

---

# 6. 双模式演奏设计

# 6.1 Mode A：PolyKey Mode

Pad 直接对应音符，每次按下立即产生 Note On。

推荐映射：

| 演奏输入 | 音乐参数 |
|---|---|
| Pad 位置 | Note / Scale Degree |
| Pad 初始压力斜率 dP/dt | Velocity |
| Pad 持续压力 P(t) | Poly Aftertouch |
| Touch X | Pitch Bend / Glide |
| Touch Y | Filter Cutoff / FM Index / Timbre |
| Touch 横向速度 | Vibrato 深度 |
| Touch 纵向速度 | FX Send / Expression |
| Encoder | ADSR / Wave / Filter / FX |

### 6.1.1 压力一传感器双用途

压力波形既可以提取按下瞬间的速度，也可以提取持续压力：

```text
Pressure
   ^
   |        /----------------
   |       /
   |      /
   |_____/
          ^          ^
          |          |
        dP/dt       P(t)
          |          |
       Velocity   Aftertouch
```

这使单个 Pad 同时拥有传统键盘 Velocity 和高级控制器 Aftertouch 两个维度。

### 6.1.2 音阶映射

建议支持：

- Chromatic；
- Major；
- Natural Minor；
- Pentatonic；
- Blues；
- 用户自定义音阶。

4x8 Pad 可以使用“等距音程网格”映射，例如横向 +1 或 +2 半音，纵向 +5 或 +7 半音，以形成更适合和弦的几何结构。

---

# 6.2 Mode B：Chord-Strum Mode

该模式是项目核心差异化设计。

Pad 按下不发声，只改变当前和弦、调式或指法状态；触摸板划动跨越虚拟弦时才触发物理弦模型或合成器声部。

## 6.2.1 Pad 和弦逻辑

可采用下列方案：

- 8 列：I、II、III、IV、V、VI、VII、VIII；
- 4 行：Triad、7th、Sus/Add、Inversion/Extension。

也可以切换为 32 个固定和弦槽位，由 OLED/编码器选择 Key 和 Scale 后自动重新映射。

## 6.2.2 触摸板虚拟弦

将触摸板划分为 6 - 8 条虚拟弦区域。

```text
String 1  --------------------------------
String 2  --------------------------------
String 3  --------------------------------
String 4  --------------------------------
String 5  --------------------------------
String 6  --------------------------------
```

手指轨迹从上一帧位置到当前帧位置若跨越某条弦的边界，则产生 `string_cross_event`。

## 6.2.3 表情参数映射

| 手势特征 | 物理/音乐参数 |
|---|---|
| 划动方向 | Up Stroke / Down Stroke |
| 划动速度 | 拨弦力度 |
| 跨弦间隔 | 琶音速度 |
| Touch X | 拨弦位置 / Brightness |
| Touch Y | 弦区选择或音色参数 |
| Pad Pressure | Palm Mute / Damping |
| 持续按压 | Sustain / Chord Hold |

这种交互能够在答辩中直接展示“选和弦”和“真正触发拨弦”属于两个独立的演奏动作维度。

---

# 7. 32 路压力 Pad 硬件方案

## 7.1 传感器方案选择

### 方案 A：FSR / 压阻薄膜

优点：

- 结构直观；
- 可测持续压力；
- 容易实现 Aftertouch；
- 与硅胶 Pad 配合成熟。

缺点：

- 个体一致性一般；
- 存在温漂和零点漂移；
- 需要逐键校准。

**推荐作为正式版主方案。**

### 方案 B：压电片

优点是对敲击瞬态非常敏感，Velocity 非常好测；缺点是难以稳定测持续压力。因此可以用于实验版或与 FSR 组合，不建议作为唯一压力传感器。

### 方案 C：应变片/微型压力传感器

精度更高，但机械设计与成本明显增加，不适合 32 键大规模铺设。

## 7.2 扫描方案

推荐采用：

```text
32 FSR -> 电阻分压
       -> 2 x 16:1 Analog MUX
       -> ADC
       -> FPGA
```

ADC 推荐规格方向：

- 12 - 16 bit；
- 总采样率 500 kSPS - 2 MSPS；
- SPI 或并口；
- 低转换延迟；
- 外部基准稳定。

以 1 MSPS 为例，32 路轮询理论每键约 31.25 kSPS，即使考虑 MUX 建立时间和滤波，仍远高于演奏所需的 1 - 4 kHz 控制刷新率。

## 7.3 Pad 采样处理

每键保存以下状态：

```text
raw_pressure[i]
baseline[i]
pressure[i]
velocity[i]
gate[i]
aftertouch[i]
peak[i]
```

处理过程：

```text
ADC Raw
  -> Baseline Subtraction
  -> Clamp
  -> Fast Trigger Branch
  -> Expression Filter Branch
  -> Nonlinear Curve
  -> Velocity / Aftertouch
```

## 7.4 快速触发支路

为了避免滤波引入延迟，Note On 不应等待长窗口平均。

建议逻辑：

```text
if pressure_raw > TH_ON
and previous_state == RELEASED
and confirm_count >= N_fast
    -> NOTE_ON
```

并使用 `TH_ON > TH_OFF` 的滞回防抖。

N_fast 建议为 1 - 3 个高速采样点。

## 7.5 Velocity 估算

可在越过低阈值后，在固定的短窗口内统计：

- 峰值；
- 最大一阶差分；
- 固定时间后的压力；
- 两者加权。

例如：

$$
V = a\cdot \max(\Delta P) + b\cdot P(t_0 + T_v)
$$

最终映射到 0 - 127 或内部 10 - 12 bit 表情值。

## 7.6 Pad 校准

OLED 中加入 Calibration 页面：

1. 无按压采集 1 - 2 s 基线；
2. 逐键轻按；
3. 逐键重按；
4. 保存 `baseline/min/max/gain`；
5. FPGA 内用 BRAM/寄存器保存校准系数。

若需要断电保存，可将参数写入外部 Flash，但运行时参数处理仍在 FPGA 中完成。

---

# 8. XY 电容触摸演奏面方案

## 8.1 设计目标

触摸面需要至少输出：

```text
touch_valid
x
 y
vx
vy
speed
direction
```

可选扩展：

- contact_strength；
- touch_area；
- 多点触控；
- hover/proximity。

正式版单点高刷新率优先于复杂多点。

## 8.2 推荐技术路线

推荐采用“**自研电极 + 前端测量 + FPGA 坐标/手势计算**”。

触摸 PCB 采用 X/Y 电极阵列，例如：

```text
X electrodes: 12 - 16 条
Y electrodes: 8 - 12 条
```

可以使用三种实现层级：

### 路线 1：FPGA 直接 RC 充放电计时

FPGA 控制 GPIO 对电极充放电，通过阈值比较器测量达到门限所需时间。

优点：自研程度最高；缺点：模拟稳定性、IO 模式、EMI 和人体环境影响较大。

### 路线 2：模拟前端 + 比较器 + FPGA 计时

外部模拟电路只完成激励、放大/比较，FPGA 完成通道扫描、计时、基线、坐标、质心和手势。

**这是最推荐的“自研程度与工程稳定性折中方案”。**

### 路线 3：电容采集 IC 输出原始通道值

专用芯片只采原始电容数据，不在芯片内部完成坐标、手势或演奏语义判断；FPGA 读取原始通道值后自行计算。

这是风险最低的备份方案。

## 8.3 坐标质心计算

对 X 轴电极：

$$
X = \frac{\sum_i iC_i}{\sum_i C_i}
$$

对 Y 轴类似：

$$
Y = \frac{\sum_j jC_j}{\sum_j C_j}
$$

为了降低硬件除法成本，可采用：

- 倒数 LUT；
- 归一化近似；
- 定点迭代；
- 时间复用除法器。

触摸刷新只需 1 - 4 kHz，因此无需为坐标除法占用大量实时音频资源。

## 8.4 手势算法

每一帧计算：

$$
V_x = X[n]-X[n-1]
$$

$$
V_y = Y[n]-Y[n-1]
$$

$$
S \approx |V_x|+|V_y|
$$

并由符号判断方向。

### 虚拟弦跨越检测

假设每条弦的边界坐标为 `B[k]`，当：

```text
Y_prev < B[k] <= Y_now
```

或反向跨越时，立即产生拨弦事件。

该路径不等待完整的手势结束，因此触发延迟非常低。

---

# 9. 编码器、按键、OLED 与 RGB 反馈

## 9.1 旋转编码器

建议 4 个带按压编码器：

| 编码器  | 默认功能                  |
| ---- | --------------------- |
| ENC1 | Attack / 主参数 1        |
| ENC2 | Decay/Release / 主参数 2 |
| ENC3 | Filter / Timbre       |
| ENC4 | FX Mix / Master       |

编码器处理由 FPGA 完成：

```text
A/B -> synchronizer -> debounce -> quadrature decoder -> delta
```

## 9.2 功能按键

建议至少：

- MODE；
- OCT-；
- OCT+；
- HOLD；
- SHIFT；
- HOME/BACK。

## 9.3 RGB Pad

每个 Pad 配一个 RGB LED，亮度与颜色用于反馈：

### PolyKey Mode

- 根音：特殊颜色；
- 调内音：常亮；
- 当前按下：高亮；
- 压力：亮度；
- Release：渐隐。

### Chord-Strum Mode

- 当前和弦 Pad：高亮；
- 和弦构成音：相关 Pad 联动；
- 拨弦方向：流水动画；
- 节拍训练：LED 指引。

RGB 总功耗必须有限制。FPGA 内建议加入全局亮度限制和峰值电流策略。

## 9.4 OLED 页面规划

建议至少 7 个页面：

1. **Home**：Mode、Preset、Key、Octave、Polyphony；
2. **Synth**：Wave、Detune、FM、ADSR；
3. **Filter**：Cutoff、Resonance；
4. **FX**：Chorus、Delay、Reverb；
5. **Scope**：波形；
6. **Spectrum**：实时频谱；
7. **Performance/Test**：Active Voice、OSC Count、Fs、Latency、Throughput。

---

# 10. FPGA 时钟、复位与实时调度

## 10.1 时钟域规划

建议至少分为：

| 时钟域 | 典型频率 | 功能 |
|---|---:|---|
| sys_clk | 100 - 200 MHz | 主 RTL、传感器、调度 |
| audio_mclk | 24.576 MHz 或相关倍频 | 96 kHz 音频 |
| i2s_bclk | 6.144 MHz | 96k x 2ch x 32slot |
| oled_spi | 10 - 40 MHz | OLED |
| adc_spi | 10 - 50 MHz | 压力 ADC |

如果大部分音频运算都在 `sys_clk` 下完成，则 `sample_tick` 只作为每个采样周期的启动脉冲，最后将结果送到 I2S 时钟域。

## 10.2 sample_tick

96 kHz 下：

$$
T_s = 10.4167 \mu s
$$

若系统时钟 150 MHz，则每个采样周期约有：

$$
150\text{M}/96\text{k} \approx 1562
$$

个系统时钟周期。

因此即使并非所有运算都“完全空间并行”，也有足够周期进行受控时间复用。但从比赛展示角度，独立振荡器应保留独立相位、频率、包络状态，避免把所有声部压缩成无法说明独立性的单一状态机。

## 10.3 确定性调度

每个 sample 周期按固定顺序：

```text
sample_tick
  -> latch performance parameters
  -> oscillator/string compute
  -> voice mix
  -> master DSP
  -> saturate
  -> push to I2S FIFO/register
```

若最大路径无法在一个周期内完成，应采用固定流水级，而不是运行时间不确定的控制结构。

---

# 11. Poly Synth Engine 设计

## 11.1 32 Voice / 64 Oscillator

正式版结构：

```text
Voice 0 : OSC_A + OSC_B + ADSR + Pan
Voice 1 : OSC_A + OSC_B + ADSR + Pan
...
Voice31 : OSC_A + OSC_B + ADSR + Pan
```

每个独立振荡器至少包含：

- 独立相位累加器；
- 独立频率/相位增量；
- 独立波形选择或运算单元；
- 独立幅度/包络控制；
- 可被单独测试和静音。

这有利于符合振荡器统计规则。

## 11.2 DDS 相位累加器

采用 32-bit phase accumulator：

$$
phase[n+1] = phase[n] + phase\_inc
$$

$$
phase\_inc = \frac{f}{F_s}2^{32}
$$

MIDI/音阶频率可使用 ROM 保存相位增量，而不是实时计算指数函数。

## 11.3 波形生成

建议分两类：

### 算术波形

- Saw：直接取相位高位；
- Square/Pulse：比较相位；
- Triangle：对 saw 进行折叠。

### LUT 波形

- Sine；
- 非完整采样的单周期 wavetable；
- 经过设计的周期谐波表。

注意：使用单周期 wavetable 只是合成器波形生成方法，不等同于整段 PCM 乐器录音。

## 11.4 抗混叠策略

基础版可先使用直接 DDS；正式版至少建议实现一种简化抗混叠策略：

- Band-limited wavetable 多表；
- PolyBLEP；
- 高频下自动降低谐波丰富波形的增益；
- 轻量 oversampling 只用于音质，不计入吞吐评分。

为降低开发风险，推荐“多级 band-limited wavetable + 直接算术波形”组合。

## 11.5 ADSR

每声部状态机：

```text
IDLE -> ATTACK -> DECAY -> SUSTAIN -> RELEASE -> IDLE
```

包络可使用线性或指数近似。

推荐内部 envelope 为 18 bit 无符号定点。

## 11.6 Voice Allocation

32 个 Pad 不代表同时最多只有 32 个音符事件。需要处理重触发、Hold 和长 Release，因此需要 Voice Allocator。

优先级建议：

1. IDLE voice；
2. RELEASE 且幅度最低；
3. 最老 voice；
4. 必要时 voice steal。

Voice allocator 只处理演奏事件，不进入逐样本高频路径。

---

# 12. FM 合成扩展

## 12.1 基础 2-Operator FM

每个 Voice 可选择：

```text
Modulator -> Carrier phase modulation -> output
```

其核心：

$$
y[n] = \sin(\phi_c[n] + I\sin(\phi_m[n]))
$$

其中 I 由 Touch Y、Aftertouch 或 Encoder 控制。

## 12.2 冲分 4-Operator FM

Mega 138K 或资源允许时，可升级为 4 Operator，并预置若干算法拓扑。

若 32 Voice x 4 Operator，则可形成 128 个独立 FM 运算单元，用于冲击高并行规模指标。

## 12.3 FM 与双振荡器的关系

正式版不必所有 Voice 永远运行 FM。推荐 Synth Preset 决定路径：

- Dual Wavetable；
- 2-op FM；
- Wavetable + FM Modulator；
- Unison Detune。

这样兼顾资源和音色多样性。

---

# 13. Chord-Strum 物理弦模型

## 13.1 为什么采用 Karplus-Strong

Karplus-Strong 非常适合本项目，因为：

- 它是真正的逐样本物理/波导类建模；
- 与“触摸划过虚拟弦”具有自然的因果关系；
- BRAM 和简单乘加即可实现；
- 多条弦可以并行复制；
- 拨弦力度、阻尼、亮度、音高都可连续调节。

## 13.2 单弦结构

```text
          +-----------------------------------+
          |                                   |
Exciter ->+-> Variable Delay Line -> LPF -> g +----> output
          |                                   |
          +-----------------------------------+
```

激励器可使用 LFSR noise、短脉冲或带限噪声。

## 13.3 音高

近似：

$$
f \approx \frac{F_s}{N}
$$

其中 N 为延迟长度。为了获得更准确音高，可以加入分数延迟插值：

- 一阶线性插值；
- all-pass fractional delay。

## 13.4 阻尼与音色

Pad Pressure 映射阻尼：

```text
Pressure low  -> open string, long decay
Pressure high -> palm mute, short decay
```

Touch X 映射拨弦位置或滤波亮度；Touch 速度映射激励幅度。

## 13.5 并行规模

正式版目标至少 8 条独立物理弦。

若一个和弦有 6 个音，则 6 条弦可以同时保持独立的延迟线状态。额外 2 条可用于重叠 Release 或扩展和弦。

资源允许时做 16 条，可支持更复杂的重叠拨弦与共振。

---

# 14. 数字音频格式与定点设计

## 14.1 推荐位宽

| 数据 | 位宽建议 |
|---|---:|
| Phase | 32 bit unsigned |
| Wave sample | 18 bit signed |
| Envelope | 18 bit unsigned |
| Voice product | 36 bit |
| Voice mixer accumulator | 40 - 48 bit signed |
| DSP internal | 24 - 32 bit signed |
| I2S output | 24 bit signed |

## 14.2 饱和与舍入

多声部相加禁止直接截断。推荐：

```text
wide accumulator
 -> headroom scaling
 -> rounding
 -> soft limiter/saturation
 -> 24-bit output
```

## 14.3 定点验证

所有 DSP 模块必须有 Python/MATLAB 参考模型或高精度软件模型，用于比较：

- 幅频响应；
- 定点误差；
- 溢出；
- 极端参数稳定性。

软件模型只用于开发验证，不参与最终运行。

---

# 15. Mixer、Pan 与动态管理

## 15.1 Voice Mixer

每 Voice 输出先乘 Pan 系数再进入左右声道累加。

可采用 equal-power pan LUT：

```text
L = cos(theta)
R = sin(theta)
```

也可以使用简单线性近似降低资源。

## 15.2 Headroom

32 Voice x 2 OSC 全部同时满幅会溢出，因此需要：

- 每声部预留 6 - 12 dB；
- active voice count 自动归一化可选；
- master limiter 兜底。

不建议使用“声音一多就明显变小”的激进自动归一化，应保持音乐动态。

---

# 16. FPGA 内 DSP 效果

## 16.1 效果链建议

```text
Voice/String Mix
   -> Global Filter
   -> Chorus
   -> Delay
   -> Reverb
   -> Limiter
   -> I2S
```

## 16.2 Global Filter

至少实现：

- 一阶 LPF 或 SVF；
- 正式版推荐 biquad low-pass。

Touch Y 可实时控制 cutoff，Pressure 可控制 resonance 或 envelope amount。

## 16.3 Chorus

Chorus 由短延迟 + LFO 调制形成：

```text
input -> variable delay -> mix dry/wet
              ^
              |
             LFO
```

需要分数延迟插值，以减少“跳点”噪声。

## 16.4 Delay

使用 BSRAM 或 DDR3 环形缓冲。

正式演奏链更推荐优先使用片内 BSRAM，以减少外存控制复杂度和不确定延迟；长延迟可作为后期扩展再使用 DDR3。

参数：

- delay time；
- feedback；
- wet/dry；
- high-frequency damping。

## 16.5 Reverb

推荐 Schroeder/Freeverb 风格：

```text
4 - 8 x Comb
   -> 2 - 4 x All-pass
   -> Wet Mix
```

先实现 4 Comb + 2 All-pass，资源稳定后再扩展。

## 16.6 Limiter

基础版用软饱和或快速峰值限制即可，不需要复杂 look-ahead。

目标是防止 32 Voice 极端叠加时 DAC 输出削顶。

---

# 17. I2S、DAC 与模拟音频

## 17.1 I2S 格式

建议：

- Sample rate：96 kHz；
- Word：24 bit；
- Slot：32 bit；
- Stereo。

则：

$$
BCLK = 96000 \times 2 \times 32 = 6.144\text{ MHz}
$$

FPGA 生成：

- MCLK（视 DAC 需要）；
- BCLK；
- LRCK；
- SDATA。

## 17.2 DAC 选择原则

不建议把最终 DAC 型号过早锁死，应按以下指标筛选：

- 支持 96 kHz / 24 bit I2S；
- 时钟接口简单；
- 低延迟数字滤波选项；
- 布板要求可控；
- 有成熟参考设计；
- 输出可以方便接线路输出/耳放。

正式 PCB 前再决定具体器件。

## 17.3 模拟输出

建议：

```text
DAC
 -> Reconstruction/Output Stage
 -> Line Out
 -> Headphone Amplifier
 -> 3.5 mm Headphone
```

如空间有限，可只保留 Line Out + 耳机输出二选一，但现场演示建议同时具备耳机和外接音箱能力。

---

# 18. 极低延迟设计

## 18.1 延迟预算

正式目标：整体 < 2 ms。

建议预算：

| 环节 | 目标 |
|---|---:|
| 压力/触摸扫描 | 0.1 - 0.6 ms |
| 事件判定 | < 0.05 ms |
| 等待下一个音频 sample | < 0.011 ms @ 96k |
| 合成流水 | < 0.05 ms |
| DSP | < 0.1 ms，固定流水 |
| I2S 帧等待 | < 0.011 ms |
| DAC 数字滤波/模拟 | 依器件，尽量低延迟 |
| 总目标 | 1 - 2 ms |

真正的最大风险通常不是 FPGA 合成，而是传感器扫描和 DAC 内部数字滤波，因此器件选型必须关注 group delay。

## 18.2 双路径传感器处理

核心原则：

```text
Raw Sensor
  |\
  | +-> FAST EVENT -> Note/Strum Trigger
  |
  +----> SMOOTH EXPRESSION -> Pressure/XY/FX
```

## 18.3 避免音频大 FIFO

音频路径不应使用几十毫秒级的缓冲。I2S 输出只保留 1 - 数个 sample 的弹性缓存即可。

---

# 19. Latency Test Mode

## 19.1 必须做硬件测量

增加两个调试 GPIO：

- `DBG_EVENT`：检测到按键/拨弦事件时翻转；
- `DBG_AUDIO`：该事件对应的第一个有效音频 sample 进入输出通路时翻转。

示波器测：

```text
DBG_EVENT  ____|------------------------------
DBG_AUDIO  _________|-------------------------
               <--- dt --->
```

该测量能证明数字链路延迟和抖动。

## 19.2 完整声学延迟

若需要更严格，可以：

- 输入事件 GPIO 作为触发；
- DAC 线路输出接示波器第二通道；
- 测从事件到模拟波形明显变化的时间。

报告中同时给出“数字链路延迟”和“端到端模拟输出延迟”。

---

# 20. Oscillator Competition Test Mode

## 20.1 目标

在现场一键进入测试模式，让所有独立振荡器以不同频率工作。

菜单：

```text
OSC TEST
Count: 4 / 8 / 16 / 32 / 64
Spacing: 30 Hz / 50 Hz / Custom
Level: -24 dBFS
START
```

## 20.2 频率设计

避免所有频率构成简单倍频关系，以防谱峰重合。

可选择在 200 Hz - 5 kHz 区间放置非整倍数频率。

每个振荡器的增益降低，防止 64 路叠加削顶。

## 20.3 吞吐量展示

对于 64 独立振荡器、96 kHz：

$$
64\times96000 = 6.144\text{ M oscillator-samples/s}
$$

OLED 显示：

```text
ACTIVE OSC : 64
SAMPLE RATE: 96.0 kHz
THROUGHPUT : 6.144 M OSC-s/s
XRUN       : 0
```

如果升级 128 Operator：

$$
128\times96000 = 12.288\text{ M op-samples/s}
$$

---

# 21. OLED 实时可视化

## 21.1 波形

从最终音频流按固定步长抽样，将 128 - 256 个点写入显示缓冲。

OLED 刷新率 20 - 60 FPS 即可，完全不需要与 96 kHz 音频同步刷新。

## 21.2 频谱

推荐两个实现等级：

### Level A：Goertzel Filter Bank

例如 16 或 32 个固定频带，开发简单、资源可控。

### Level B：64/128/256 Point FFT

正式版建议 128 Point FFT，使用 window + magnitude approximation。

OLED 仅显示 32 - 64 个柱状频带即可。

## 21.3 Voice Map

显示当前活跃声部：

```text
V01 ###      V09 ####
V02 #####    V10 #
V03 --       V11 ###
...
```

或使用 32 个小格表示 Voice 状态，对评委非常直观。

---

# 22. LED 曲目引导与脱机扩展

这是后期拓展功能，不应优先于合成引擎。

## 22.1 曲目数据格式

不要存 PCM，只保存事件：

```text
time
pad_id
note/chord
expected_duration
velocity_hint
```

FPGA 根据时间点点亮相应 Pad，用户实际按下后才产生音频。

## 22.2 节拍引导

Pad 可以按 Beat/Sub-beat 做动画：

- 下一步淡亮；
- 当前拍高亮；
- 演奏正确后转为确认状态。

---

# 23. 蓝牙/App 扩展边界

蓝牙不是核心，最后再做。

允许传输：

- Preset 参数；
- Scale/Chord Map；
- LED Theme；
- 曲目事件；
- 用户键位映射；
- 演奏事件日志。

不建议传输并回放：

- 完整 PCM 乐器采样；
- 整段伴奏用于冒充实时合成；
- 由手机算好后的实时音频流。

如果需要“录音回传”，可以将 FPGA 实时产生的最终音频向外录制，但应明确录音是导出结果，而不是后续现场发声的来源。

---

# 24. 电源与 PCB 架构

## 24.1 电源树

典型结构：

```text
USB-C 5V / Battery
   |
   +-> FPGA board power input
   +-> 3.3V Digital
   +-> ADC/AFE low-noise rail
   +-> DAC analog rail
   +-> Headphone amp rail
   +-> RGB LED rail
```

RGB LED 和音频模拟部分尽量不要共享高阻抗供电路径。

## 24.2 地与布局

建议：

- FPGA 高速数字区、ADC/传感区、DAC 模拟区分区；
- DAC 输出远离 RGB PWM 和高速 SPI；
- ADC 基准和模拟地做局部安静区域；
- 电容触摸区域下方避免高速时钟和大面积动态数字走线；
- I2S 走线短、参考平面连续；
- 耳放远离 FPGA PLL 和 DC/DC。

## 24.3 结构层级

推荐：

```text
Top silicone/acrylic panel
Pad light guide
Pressure mechanical layer
Sensor PCB
Touch PCB / Control PCB
FPGA SOM/Carrier
DAC/Audio board
Bottom shell
```

第一版可模块化，决赛版再合并 PCB。

---

# 25. FPGA RTL 模块划分

建议工程目录：

```text
rtl/
  top.sv

  clock/
    pll_audio.sv
    reset_sync.sv
    sample_tick.sv

  input/
    adc_spi_if.sv
    pad_mux_ctrl.sv
    pad_scanner.sv
    pressure_baseline.sv
    velocity_detect.sv
    aftertouch_filter.sv

    cap_scan.sv
    touch_baseline.sv
    touch_centroid.sv
    gesture_detect.sv
    string_crossing.sv

    encoder.sv
    button_debounce.sv

  performance/
    mode_controller.sv
    scale_mapper.sv
    chord_generator.sv
    note_event_fifo.sv
    voice_allocator.sv
    parameter_router.sv

  synth/
    phase_accumulator.sv
    waveform_gen.sv
    wavetable_rom.sv
    adsr.sv
    oscillator.sv
    dual_osc_voice.sv
    oscillator_bank.sv

    fm_operator.sv
    fm_voice.sv

    ks_exciter.sv
    ks_delay_line.sv
    ks_string.sv
    string_bank.sv

  dsp/
    mixer.sv
    pan.sv
    biquad.sv
    chorus.sv
    delay.sv
    reverb_comb.sv
    reverb_allpass.sv
    limiter.sv

  audio/
    i2s_tx.sv
    audio_clocking.sv

  visual/
    oled_spi.sv
    font_rom.sv
    ui_renderer.sv
    waveform_capture.sv
    fft_core.sv
    spectrum_mapper.sv
    rgb_engine.sv

  debug/
    latency_test.sv
    oscillator_test.sv
    performance_counter.sv
    debug_gpio.sv

sim/
  tb_oscillator.sv
  tb_adsr.sv
  tb_ks_string.sv
  tb_mixer.sv
  tb_i2s.sv
  tb_full_audio_path.sv

model/
  reference_dds.py
  reference_adsr.py
  reference_ks.py
  reference_fx.py

docs/
  architecture.md
  fixed_point.md
  latency_budget.md
  resource_report.md
  validation_report.md
```

---

# 26. 模块接口规范建议

所有演奏事件采用统一内部事件格式，可定义类似：

```text
note_event:
  valid
  event_type
  source_id
  note
  velocity
  pressure
  x
  y
  timestamp
```

连续参数采用定点统一范围，例如：

```text
0x0000 = 0.0
0xFFFF = 1.0
```

Pitch Bend 单独使用 signed Q 格式。

所有模块尽量使用 `valid/ready` 或明确 sample strobe，不让控制模块直接依赖长组合路径。

---

# 27. FPGA 资源预算

以下为规划阶段预算，不是最终综合结果。

## 27.1 Mega 60K 资源目标

| 模块 | LUT 预算 | DSP 预算 | BSRAM 预算 | 备注 |
|---|---:|---:|---:|---|
| Input/Touch | 3K - 5K | 2 - 6 | 少量 | 坐标/滤波 |
| 64 Oscillator | 8K - 15K | 20 - 50 | 200 - 500 Kb | 视 LUT/算术实现 |
| ADSR/Allocator | 3K - 5K | 0 - 8 | 少量 | 32 Voice |
| 8 KS Strings | 4K - 8K | 8 - 16 | 300 - 700 Kb | delay line |
| Mixer/Pan | 2K - 4K | 8 - 16 | 少量 | stereo |
| Chorus/Delay | 3K - 6K | 4 - 12 | 300 - 700 Kb | 环形缓存 |
| Reverb | 4K - 8K | 8 - 20 | 300 - 600 Kb | 先做轻量版 |
| OLED/FFT/RGB | 4K - 8K | 8 - 20 | 100 - 300 Kb | 可裁剪 |
| Debug/Test | 2K - 4K | 少量 | 少量 | 决赛保留 |

实际设计应预留 15 - 20% LUT 和 10 - 20% BSRAM 余量，避免后期时序收敛困难。

## 27.2 资源降级开关

从第一天就用参数开关：

```text
ENABLE_FM
ENABLE_KS
ENABLE_CHORUS
ENABLE_REVERB
ENABLE_FFT
NUM_VOICES
OSC_PER_VOICE
NUM_STRINGS
SAMPLE_RATE_MODE
```

这样可快速做资源和时序消融。

---

# 28. 测试与验证体系

## 28.1 模块级仿真

必须覆盖：

- DDS 频率误差；
- 波形幅值；
- ADSR 状态转换；
- Voice steal；
- 压力 trigger hysteresis；
- Velocity；
- Touch centroid；
- 弦边界 crossing；
- KS 衰减和音高；
- Mixer 溢出；
- Delay/Reverb 稳定性；
- I2S 格式。

## 28.2 音频离线比对

仿真产生 PCM/WAV，仅用于验证输出，不作为最终乐器输入。

与 Python reference 比较：

- FFT 主峰；
- RMS；
- THD 近似；
- 包络曲线；
- KS 音高和衰减；
- FX impulse response。

## 28.3 板级测试

按照顺序：

1. 时钟与复位；
2. 固定正弦 I2S；
3. DAC 输出；
4. 单振荡器；
5. 8/32/64 振荡器；
6. 压力 ADC；
7. 单 Pad；
8. 32 Pad；
9. Touch；
10. 双模式；
11. DSP；
12. OLED/RGB；
13. 端到端延迟；
14. 长时间稳定性。

## 28.4 稳定性测试

至少进行：

- 连续运行 2 - 8 小时；
- 全 32 Voice 连续触发；
- 快速扫弦；
- 最大 FX feedback 合法范围；
- 频繁切换模式；
- RGB 满负荷动画；
- 电池/USB 供电切换（若支持）。

记录：

```text
underrun_count
overrun_count
max_voice_count
max_mixer_level
sensor_error_count
I2S_sync_error
```

---

# 29. 现场演示脚本设计

演示应按“先音乐性，再硬核指标”展开。

## 29.1 30 秒产品演奏

- 开机进入 Home；
- PolyKey Mode 演奏一段旋律；
- 用 Pressure 做强弱；
- 用 Touch X 做 Pitch Bend；
- 用 Touch Y 做音色变化；
- 开启 Chorus/Reverb。

## 29.2 30 秒 Chord-Strum

- 切换 Chord-Strum；
- Pad 选择 Am7；
- 手指下扫、上扫；
- 快慢扫弦对比；
- Pressure 做闷音；
- OLED 显示当前 chord 与虚拟弦状态。

## 29.3 30 秒并行能力

进入 OSC TEST：

- 8 -> 32 -> 64；
- OLED 显示 Active OSC 和吞吐量；
- 外接频谱仪/示波器观察多谱峰。

## 29.4 30 秒低延迟

进入 Latency Test：

- 示波器显示 EVENT GPIO；
- 同时显示 DAC/audio GPIO；
- 直接读出 dt；
- 连续触发证明延迟抖动很小。

## 29.5 30 秒 RTL 佐证

准备一页架构图和 4 个关键 RTL 文件：

- oscillator.sv；
- adsr.sv；
- ks_string.sv；
- i2s_tx.sv。

解释没有 PCM 播放模块，没有软件音频线程。

---

# 30. 研发阶段与里程碑

推荐以 14 周为一个完整研发周期。若时间更多，可以把每阶段拉长。

| 周期 | 任务 | 里程碑 |
|---|---|---|
| W1 | 板卡、DAC、I2S、工程框架 | 固定正弦从 DAC 发声 |
| W2 | DDS/Wavetable、音符频率表 | 单音可变调 |
| W3 | ADSR、Voice、Mixer | 8 复音稳定 |
| W4 | 32 Voice / 64 OSC | 64 路测试模式可见谱峰 |
| W5 | 单压力传感器、ADC/MUX | 单 Pad Velocity/Pressure |
| W6 | 32 Pad 扫描、RGB | 完整 Pad Matrix |
| W7 | Touch 原型 | X/Y 连续坐标稳定 |
| W8 | Gesture/Strum | 上扫/下扫/速度检测 |
| W9 | PolyKey 完整 | 模式 A 可正式演奏 |
| W10 | KS 物理弦 | Chord-Strum 可正式演奏 |
| W11 | Filter/Delay/Chorus | 至少 2 种 DSP |
| W12 | Reverb/OLED Scope/Spectrum | 拓展功能完成 |
| W13 | Latency/Stress/Resource | 完整测试报告 |
| W14 | PCB/结构优化、演示脚本 | 决赛/答辩版本冻结 |

### Gate 机制

每两周进行一次 Gate Review：

- Gate 1：稳定 I2S；
- Gate 2：64 OSC；
- Gate 3：完整交互；
- Gate 4：双模式；
- Gate 5：DSP + 可视化；
- Gate 6：测试与演示。

任何 Gate 未通过，不继续盲目叠加功能。

---

# 31. 团队分工建议

如果 4 人团队：

| 角色 | 主要负责 |
|---|---|
| A：系统/音频 FPGA | 时钟、DDS、Voice、Mixer、I2S、集成 |
| B：DSP/物理建模 | FM、KS、Filter、Chorus、Delay、Reverb |
| C：交互/传感 FPGA | Pad、ADC、Touch、Gesture、Encoder、校准 |
| D：硬件/UI/验证 | PCB、电源、DAC、OLED、RGB、结构、示波器测试 |

所有人必须共同维护：

- Git；
- 模块接口文档；
- 测试用例；
- 周资源报告；
- 演示脚本。

如果只有 3 人，可合并 B 与 A 或 D 与 C。

---

# 32. BOM 方向与成本控制

以下仅为类别规划，不锁定具体采购价格。

| 类别 | 数量 | 优先级 |
|---|---:|---|
| Tang Mega 60K | 1 | 必须 |
| 24-bit I2S DAC | 1 | 必须 |
| Headphone/Line Output | 1 | 必须 |
| FSR/压阻传感器 | 32 | 必须 |
| 16:1 Analog MUX | 2 - 4 | 必须 |
| 12/16-bit ADC | 1 - 2 | 必须 |
| Touch AFE/Comparator | 若干 | 必须 |
| Touch Electrode PCB | 1 | 必须 |
| RGB LED | 32 | 必须 |
| OLED | 1 | 必须 |
| Rotary Encoder | 4 | 建议 |
| USB-C Power | 1 | 必须 |
| Battery/BMS | 1 | 可选 |
| BLE Module | 1 | 后期 |
| 外壳/硅胶 Pad | 1 套 | 必须 |

成本原则：

- 优先把预算投入稳定传感、DAC 和机械结构；
- 不为了“高级 DAC”牺牲项目进度；
- 触摸和压力传感的一致性比外观灯效更重要；
- 第一版模块化，第二版再集成。

---

# 33. 主要风险与应对

## 33.1 电容触摸不稳定

**风险：** 人体、接地、湿度、外壳、电源噪声导致漂移。

**应对：**

- 先做 4x4/8x4 小面积电极验证；
- 自动 baseline tracking；
- 触摸区远离高速数字；
- 保留专用 raw channel debug 页面；
- 准备“原始电容 IC + FPGA 手势”的备份方案。

## 33.2 32 FSR 一致性差

**应对：** 每键校准、机械预压统一、非线性曲线 LUT、动态 baseline。

## 33.3 64 OSC + DSP 资源超标

**应对：** 从第一天使用可配置参数和效果开关；先守住 64 OSC，再裁剪 Reverb/FFT；必要时升级 138K。

## 33.4 音频削顶

**应对：** 宽累加器、固定 headroom、master limiter、专用 maximum stress test。

## 33.5 DAC 延迟过高

**应对：** 选型时查数字滤波 group delay；优先低延迟模式；保留 48/96 kHz 测试。

## 33.6 现场无法证明“独立振荡器”

**应对：** 每个 oscillator 保持独立 phase/freq/envelope state；专用 64 频率 Test Mode；RTL generate 结构清楚可查。

## 33.7 作品像 MIDI 控制器而不像合成器

**应对：** 强调 FPGA 内音源、物理建模、DSP、频谱和 I2S；演示时不连接电脑也能独立演奏。

---

# 34. 项目核心创新点表述

## 创新点 1：双范式演奏交互

同一硬件表面在 PolyKey 与 Chord-Strum 两种模式下具有不同演奏语义，实现“直接键击合成”和“先选和弦、后扫弦触发”两套演奏逻辑。

## 创新点 2：压力与二维连续手势的多维表情融合

从 32 路压力信号同时提取 Velocity 和 Aftertouch，并从 XY 触控获取位置、方向、速度和跨弦事件，使演奏控制维度远高于基础要求。

## 创新点 3：高并行多复音 FPGA 合成引擎

32 Voice x 2 Oscillator 形成 64 个具有独立相位、频率和包络状态的实时硬件振荡器，并通过专用频谱模式证明并行吞吐量。

## 创新点 4：触摸拨弦与物理建模一体化

手指真实跨越虚拟弦的事件直接激励 FPGA 内 Karplus-Strong 物理模型，拨弦速度、位置和压力分别映射激励、亮度和阻尼。

## 创新点 5：确定性全硬件低延迟通路

传感器触发采用 Fast Event Path，连续表情采用 Smooth Expression Path，音频使用固定 sample pipeline，避免软件调度和长缓冲产生随机延迟。

## 创新点 6：可验证的 FPGA 性能可视化

系统自带 Active Voice、OSC Count、Throughput、FFT Spectrum、Latency Debug 页面，使高复音、实时性和纯硬件路径可现场直接测量，而不是仅靠文字说明。

---

# 35. 申报/答辩叙事建议

建议始终围绕以下逻辑：

> **问题：** 传统便携电子键盘输入维度少，MCU/DSP 串行音频框架在大规模多声部和确定性低延迟方面难以同时做到高表现力与高并行度。
>
> **方法：** 设计 32 路压力 Pad + XY 触摸双交互面，将演奏动作硬件化为事件和连续参数；利用 FPGA 并行流水结构实现 64 独立振荡器、多物理弦和全硬件 DSP。
>
> **结果：** 实现 32 复音、双模式、多音色、≥5 维表情、96 kHz/24-bit I2S、<5 ms 且目标 <2 ms 的确定性演奏链路，并可通过频谱、GPIO 和 RTL 三重验证。
>
> **价值：** 不是简单复刻传统键盘，而是构建一种适合 FPGA 并行计算特性的全新便携数字乐器交互形态。

避免把重点放在“做了一个漂亮 UI”或“手机 App 很丰富”。真正的评分核心应该是：

1. 交互维度；
2. 64/128 运算规模；
3. 纯硬件逐样本生成；
4. 低延迟；
5. 物理建模；
6. 可验证性。

---

# 36. 最终交付物清单

## 36.1 硬件

- 完整便携合成器整机；
- FPGA 主板/核心板；
- 32 路压力 Pad 板；
- XY Touch 板；
- DAC/耳放板；
- RGB/OLED/Encoder；
- 外壳与面板；
- 调试接口和测试点。

## 36.2 FPGA 工程

- 完整 Gowin 工程；
- 可一键综合的顶层；
- 约束文件；
- RTL 模块；
- 仿真 testbench；
- Reference model；
- 各版本 bitstream。

## 36.3 文档

- 系统设计说明书；
- 原理图和 PCB；
- 传感器校准报告；
- FPGA 资源与时序报告；
- 定点设计说明；
- 延迟测量报告；
- 64 OSC 频谱测试报告；
- 长时间稳定性测试报告；
- 演示手册；
- 答辩 PPT。

## 36.4 视频/证据

- PolyKey 演奏视频；
- Chord-Strum 演奏视频；
- 64 OSC 频谱仪视频；
- GPIO/DAC 延迟示波器视频；
- OLED Spectrum/Voice Map 视频；
- RTL 关键模块录屏。

---

# 37. 第一阶段立即执行清单

在正式做整机前，建议马上完成以下 10 件事：

1. 确认最终 FPGA 使用 Mega 60K 还是 138K，默认先选 Mega 60K；
2. 选择一颗成熟的 I2S DAC 模块完成原型；
3. 建立 Gowin 工程和统一 RTL 目录；
4. 实现 96 kHz/24-bit I2S 固定正弦输出；
5. 实现 32-bit DDS + Sine/Saw/Square；
6. 实现 ADSR 和 8 Voice；
7. 扩展到 32 Voice/64 OSC，并先做 Competition Test Mode；
8. 用 1 个 FSR + ADC 做 Velocity/Aftertouch 原型；
9. 用小尺寸电极板验证 Touch raw 数据和 centroid；
10. 把所有模块的输入输出接口在 `architecture.md` 中冻结 V0.1。

只有第 7 项和第 9 项都成功后，再开始正式 32 Pad PCB 和大尺寸触摸面板。

---

# 38. 关键设计决策摘要

| 决策项 | 建议 |
|---|---|
| FPGA | Tang Mega 60K 首选，138K 升级 |
| 音频 | 96 kHz / 24-bit Stereo I2S |
| 主合成 | 32 Voice / 64 OSC DDS/Wavetable/FM |
| 拨弦合成 | 8 - 16 Karplus-Strong String |
| Pad | 4x8 FSR/压阻 + RGB |
| 压力采集 | Analog MUX + 外部 ADC + FPGA 处理 |
| Touch | 自研 X/Y 电极，原始测量 + FPGA centroid/gesture |
| 模式 A | Pad direct note + Touch expression |
| 模式 B | Pad chord select + Touch strum trigger |
| DSP | Filter + Chorus + Delay + Reverb + Limiter |
| 可视化 | OLED 参数/波形/频谱/性能页 |
| 低延迟 | Fast Event Path + Fixed Audio Pipeline |
| 现场证明 | 64 OSC Test + FFT + GPIO/DAC Latency Test |
| MCU | 不进入实时音频与演奏核心通路 |
| PCM | 不使用整段预录 PCM 发声 |

---

# 39. 验收标准

项目冻结前必须满足：

### 功能验收

- [ ] 32 个 Pad 全部可独立检测；
- [ ] 每个 Pad 有可感知 Velocity；
- [ ] 每个 Pad 有持续 Pressure/Aftertouch；
- [ ] Touch X/Y 连续、无明显跳变；
- [ ] 上扫/下扫识别可靠；
- [ ] PolyKey 可完整演奏；
- [ ] Chord-Strum 可完整演奏；
- [ ] 至少 2 种明显不同音色；
- [ ] 至少 2 种 DSP 效果，正式目标 3 种；
- [ ] 32 复音实际可用；
- [ ] 64 独立 oscillator 可现场验证。

### 性能验收

- [ ] 96 kHz I2S 无 underrun；
- [ ] 连续 2 小时无异常；
- [ ] 64 oscillator test 无错误；
- [ ] 总延迟 < 5 ms；
- [ ] 正式目标 < 2 ms；
- [ ] 综合资源留有合理余量；
- [ ] 时序全部收敛。

### 合规验收

- [ ] 无预录整段 PCM 播放路径；
- [ ] 关键音频通路均有 RTL；
- [ ] 每个独立 oscillator 可在 RTL 中定位；
- [ ] 现场可演示不同 oscillator 频率谱峰；
- [ ] 无电脑情况下可独立演奏。

---

# 40. 参考资料与版本说明

本规划书以用户提供的 2026 赛题要求为主要约束，并在 2026 年 9 月核对了 Sipeed Tang 系列公开资料。

板卡资源规划参考：

- Sipeed Wiki，Tang Mega 60K Dock Hardware Parameters；
- Sipeed Wiki，Tang Mega 138K Dock Hardware Parameters；
- Sipeed Tang FPGA Series Product Comparison；
- 全国大学生嵌入式芯片与系统设计竞赛公开信息。

当前公开资料中，Tang Mega 60K 典型资源为 59,904 LUT4、2,124 Kbit BSRAM、118 个 18x18 Multiplier；Tang Mega 138K 典型资源为 138,240 LUT4、6,120 Kbit BSRAM、298 个 18x18 Multiplier。具体芯片版本、IDE 版本、引脚、电气限制和板卡 Revision 应在正式 PCB 设计前再次以当时官方文档为准。

---

# 附录 A：推荐开发优先级

```text
P0  I2S + DAC
 |
P1  DDS + ADSR
 |
P2  32 Voice / 64 OSC
 |
P3  Oscillator Test + Latency Test skeleton
 |
P4  Pressure Pad prototype
 |
P5  32 Pad Matrix
 |
P6  XY Touch prototype
 |
P7  PolyKey Mode
 |
P8  Chord-Strum + KS
 |
P9  DSP
 |
P10 OLED/RGB Visualization
 |
P11 PCB Integration
 |
P12 BLE / Song Guide / Advanced FX
```

原则：**先守住合成核心和可验证指标，再做外围炫技功能。**

# 附录 B：建议的最小可行版本 MVP

如果项目进度发生严重延误，必须保留以下 MVP：

- 16 或 32 Pad；
- Pressure + Touch 两类独立交互；
- 32 复音；
- 64 独立 oscillator；
- ADSR；
- PolyKey + 简化 Strum；
- 1 种 KS 物理弦；
- 1 - 2 种 DSP；
- I2S DAC；
- OLED 参数页；
- 64 OSC Test；
- Latency GPIO Test；
- < 5 ms 实测。

FFT、复杂混响、BLE、曲目下载都可以延期，但 **64 OSC、低延迟证明、双交互、双模式** 不应被删除。

# 附录 C：最终推荐方案一句话冻结版

**Tang Mega 60K + 4x8 FSR RGB Pressure Pads + FPGA 自研 XY Touch Gesture Engine + 32 Voice/64 Oscillator Wavetable/FM Synth + 8-16 Karplus-Strong Physical Strings + ADSR/Mixer/Filter/Chorus/Delay/Reverb + 96 kHz/24-bit I2S DAC + OLED Waveform/Spectrum/Performance UI + Hardware Oscillator/Latency Verification。**
