# 第六篇：2026 之后的方向、系统落地与写作框架

# 附录

## 附录A：全书核心论文精读清单

本附录按技术脉络将全书涉及的 60 余篇核心论文分为 5 组。每组给出论文名称、必讲原因和讲解重点，供读者按图索骥。标注 `*` 者为建议精读的里程碑论文。

---

### A.1 传统 SLAM 经典论文

这组论文构成了几何 SLAM 的工程底座，理解它们是进入后续章节的前提。

| 论文 | 年份 | 必讲原因 | 讲解重点 |
|------|------|---------|---------|
| Smith & Cheeseman, *On the Representation and Estimation of Spatial Uncertainty* | 1986 | EKF-SLAM 的理论源头 | 空间不确定性的概率表示，协方差矩阵的含义 |
| Smith, Self & Cheeseman, *A Stochastic Map for Uncertain Spatial Relationships* | 1987 | 概率 SLAM 起点 | EKF 状态向量同时估计机器人位姿与路标位置，观测更新的复杂度 |
| *Montemerlo et al., FastSLAM: A Factored Solution to SLAM* | 2002 | Rao-Blackwellized 粒子滤波 SLAM | 轨迹用粒子表示，地图以 EKF 组条件独立分解，解决 EKF 的 O(n²) 瓶颈 |
| *Klein & Murray, PTAM: Parallel Tracking and Mapping* | 2007 | Keyframe-based SLAM 开山作 | Tracking/Mapping 双线程分离，关键帧策略，BA 优化地图而非逐帧 |
| Mur-Artal, Montiel & Tardós, *ORB-SLAM* | 2015 | 传统视觉 SLAM 工程标杆 | 三线程架构（Tracking/Local Mapping/Loop Closing），ORB 特征，位姿图优化 |
| Mur-Artal & Tardós, *ORB-SLAM2: An Open-Source SLAM System* | 2017 | 双目/RGB-D 扩展 | 支持多相机模型，Atlas 地图管理机制 |
| *Campos et al., ORB-SLAM3: An Accurate Open-Source Library* | 2021 | 多地图与视觉惯性融合 | IMU 预积分紧耦合，最大后验估计，多地图合并（Multi-Map） |
| *Engel, Koltun & Cremers, DSO: Direct Sparse Odometry* | 2018 | 直接稀疏法代表 | 光度误差替代重投影误差，稀疏点采样策略，窗口化优化 |
| Engel, Schöps & Cremers, *LSD-SLAM: Large-Scale Direct Monocular SLAM* | 2014 | 直接半稠密法 | 深度图正则化，Sim(3) 尺度对齐，逐像素光度残差 |
| *Qin, Li & Shen, VINS-Mono: A Robust Versatile Monocular Visual-Inertial State Estimator* | 2018 | VIO 工程系统标杆 | 紧耦合滑窗优化，IMU 预积分推导，故障检测与重定位 |
| Zhang & Singh, *LOAM: Lidar Odometry and Mapping in Real Time* | 2014 | LiDAR SLAM 工程经典 | 高频 odometry + 低频 mapping 双线程，边缘/平面特征提取 |
| Shan et al., *LeGO-LOAM: Lightweight and Ground-Optimized LOAM* | 2018 | LOAM 地面优化改进 | 地面分割，两步 LM 优化，回环检测 |
| Lin et al., *LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping* | 2020 | LiDAR-IMU 紧耦合代表 | iSAM2 因子图，IMU 预积分，GPS 融合 |
| *Rosinol et al., Kimera: An Open-Source Metric-Semantic SLAM System* | 2020 | 几何-语义融合代表 | 实时 mesh 重建，场景图构建，PDR 物理一致性 |
| Tateno et al., *CNN-SLAM: Real-time Dense Monocular SLAM with Learned Depth Prediction* | 2017 | 深度学习与传统 SLAM 早期融合 | CNN 深度先验 + 传统 BA 联合优化 |

这 15 篇论文覆盖了 SLAM 从概率滤波到图优化、从稀疏到半稠密、从纯视觉到多传感器融合的主线。阅读顺序建议：EKK-SLAM → PTAM → ORB-SLAM 系列 → DSO → VINS-Mono → LOAM → Kimera。

---

### A.2 学习增强与神经 SLAM

这组论文标志着 SLAM 从"手工设计"向"数据驱动"的范式迁移。特征提取、数据关联、深度估计、地图表示四个环节均被神经网络重写。

| 论文 | 年份 | 一句话关键 | 讲解重点 |
|------|------|-----------|---------|
| *DeTone, Malisiewicz & Rabinovich, SuperPoint: Self-Supervised Interest Point Detection* | 2018 | 特征提取可学习 | 伪自监督训练，Homographic Adaptation，特征点 + 描述符联合输出 |
| Sarlin et al., *SuperGlue: Learning Feature Matching with Graph Neural Networks* | 2020 | 数据关联神经化 | GNN 匹配特征对，注意力机制，可学习 vs 暴力匹配的优势 |
| Lindenberger, Sarlin & Pollefeys, *LightGlue: Local Feature Matching at Light Speed* | 2023 | SuperGlue 的轻量化改进 | 自适应深度与宽度，提前退出机制，速度-精度权衡 |
| Li et al., *LoFTR: Detector-Free Local Feature Matching with Transformers* | 2021 | 无检测器匹配 | 密集匹配 + Transformer，弱纹理区域表现 |
| *Teed & Deng, DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D* | 2021 | 深度 SLAM 分水岭 | Dense BA + Recurrent Update Module，可微分前端-后端联合训练 |
| Teed & Deng, *RAFT: Recurrent All-Pairs Field Transforms for Optical Flow* | 2020 | DROID-SLAM 的基础模块 | 4D 相关体积 + GRU 迭代更新，光流估计的里程碑 |
| Schönberger et al., *COLMAP: A Structure-from-Motion Pipeline* | 2016 | 传统 SfM 标杆 | 增量式重建，特征匹配与几何校验，BA 优化 |
| Sun et al., *NeuRay: Neural Rays for Occlusion-aware Multi-view Reconstruction* | 2022 | 神经光线表示 | 射线可见性建模，遮挡感知的多视图深度估计 |
| *Sucar et al., iMAP: Implicit Mapping and Positioning in Real-Time* | 2021 | 神经隐式 SLAM 起点 | MLP 作为唯一地图表示，联合优化相机位姿与 SDF，逐像素渲染 |
| *Zhu et al., NICE-SLAM: Neural Implicit Scalable Encoding for SLAM* | 2022 | 多层级局部编码 | 分层特征网格（粗/中/细）+ 浅 MLP，可扩展到大场景 |
| Sucar et al., *Nerf-SLAM: Real-Time Dense Monocular SLAM with Neural Radiance Fields* | 2023 | NeRF + SLAM 紧耦合 | Instant-NGP 编码，深度先验引导的采样，实时性提升 |
| Wang et al., *Co-SLAM: Joint Coordinate and Sparse Parametric Encodings for Neural SLAM* | 2023 | 坐标 + 参数混合编码 | 一维哈希编码减少遗忘，联合坐标与参数表示 |
| Zhang et al., *NeuralRecon: Real-Time Coherent 3D Reconstruction from Monocular Video* | 2021 | 局部片段融合重建 | 三维 CNN 处理局部片段，TSDF 融合，实时相干重建 |
| Rosinol et al., *NeRF-Navigation: Neural Radiance Fields for Robotics* | 2022 | NeRF 在机器人任务中的应用 | 碰撞检测，路径规划，NeRF 作为场景表示 |

这一阶段的核心矛盾是：神经网络带来了更强的感知能力，但实时性与可扩展性仍是瓶颈。iMAP 用 MLP 做地图虽优雅，却难以扩展；NICE-SLAM 的分层编码是务实的折中；DROID-SLAM 则证明可微分优化前端可以从头训练。

---

### A.3 3DGS-SLAM 核心论文

2023 年 3D Gaussian Splatting 问世后，SLAM 社区迅速将其纳入地图表示。相比 NeRF，3DGS 的可渲染性、显式结构和优化效率使其更适合实时系统。

| 论文 | 年份 | 讲解重点 |
|------|------|---------|
| *Kerbl et al., 3D Gaussian Splatting for Real-Time Radiance Field Rendering | 2023 | 各向异性 3D 高斯基元，tile-based 光栅化，自适应密度控制（ADP），实时渲染 |
| Kerr et al., *SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM* | 2024 | 首个 3DGS-SLAM 系统，Silhouette 渲染引导的 tracking，深度-颜色联合优化 |
| Matsuki et al., *Gaussian Splatting SLAM (MonoGS)* | 2024 | 单目 3DGS-SLAM，几何一致性约束，单目深度先验，关键帧管理 |
| Guan et al., *FlashSLAM: Fast SLAM with 3D Gaussian Splatting* | 2024 | 速度优化，高效高斯基元管理，亚实时性能目标 |
| Ye et al., *MonoGS++: Fast Reflective and Refractive 3D Gaussian Splatting SLAM* | 2024 | 处理反光/折射表面，BRDF 建模扩展 |
| He et al., *Splat-SLAM: Globally Optimized RGB-only Gaussian Splatting SLAM* | 2024 | 纯 RGB 输入，全局 BA 优化，回环检测集成 |
| Zhang et al., *Dy3DGS-SLAM: Dynamic 3D Gaussian Splatting SLAM* | 2024 | 动态物体处理，高斯基元的动态/静态分离 |
| Keetha et al., *SGS-SLAM: Semantic Gaussian Splatting SLAM* | 2024 | 语义高斯，语义标签与几何联合优化，开放语义支持 |
| Fu et al., *GSFF-SLAM: Gaussian Splatting with Feature Field for SLAM* | 2024 | 特征场融合，DINO/SAM 特征注入，语义-几何对齐 |
| Zuo et al., *OpenGS-SLAM: Open-Set 3D Gaussian Splatting via Multi-modal Gaussian Representation* | 2024 | 开放集语义，多模态高斯表示，图文查询 |
| Wang et al., *OpenMonoGS-SLAM: Open-Vocabulary Gaussian Splatting SLAM from Monocular* | 2024 | 单目+开放词汇，CLIP 特征蒸馏，自然语言查询 |
| Pan et al., *GS3LAM: Global Splatting Solution for 3D Language Gaussian SLAM* | 2024 | 全局语义优化，3D 语言-高斯对齐 |
| Deng et al., *EmbodiedSplat: Embodied 3D Gaussian Splatting with Dynamic Object Interaction* | 2024 | 具身交互，动态物体操作，3DGS 作为交互式表示 |
| Li et al., *X-GS: Adaptive 3D Gaussian Splatting with X-dimensional Attention* | 2024 | 注意力增强高斯，自适应维度分配 |
| Yang et al., *VBGS-SLAM: Voxel-Based Gaussian Splatting SLAM* | 2024 | 体素结构化高斯管理，可扩展性改进 |
| *He et al., GSMem: Spatially-Indexed 3D Gaussian Splatting Memory for Real-time Embodied Interactions* | 2025 | 空间索引 3DGS 记忆，具身交互实时支持，空间记忆接口 |

这 16 篇论文勾勒出 3DGS-SLAM 的快速演进：2023 年 Kerbl 等给出基线表示，2024 年上半年出现 MonoGS、SplaTAM 等首批系统，下半年向语义化（SGS-SLAM、OpenGS-SLAM）、动态化（Dy3DGS-SLAM）、具身化（EmbodiedSplat、GSMem）快速扩展。2025 年的 GSMem 代表 3DGS 从纯建图工具向空间记忆基础设施的转型。

---

### A.4 几何基础模型与 SLAM

2024 年起，视觉几何基础模型（monocular foundation models）开始重写 SLAM 前端。这些模型在大规模多视图数据上预训练，单图/双图推理即可输出 3D 几何信息。

| 论文 | 年份 | 讲解重点 |
|------|------|---------|
| *Wang et al., DUSt3R: Geometric 3D Vision Made Easy* | 2024 | 双图点图回归，无需相机内参，零样本跨域泛化，将 MVS 简化为回归问题 |
| Wang et al., *MASt3R: Grounding Metric 3D Reconstruction in Foundation Models* | 2024 | DUSt3R 的扩展，Fast Reciprocal Matching，单图深度 + 双图位姿联合推理 |
| *Ballester et al., MASt3R-SLAM: Real-Time Dense SLAM with Metric 3D Reconstruction* | 2025 | MASt3R 特征作为 SLAM 前端，实时稠密 tracking，基础模型驱动的新 SLAM 范式 |
| Zhang et al., *VGGT: Visual Geometry Grounded Transformer* | 2025 | 7 项视觉几何任务统一 Transformer，单前向传播输出深度/位姿/点云/内参，前沿进展 |
| Duan et al., *FoundationSLAM: A Unified Approach to Robust SLAM with Foundation Models* | 2024 | 多基础模型融合，鲁棒特征提取与匹配，提升传统 SLAM 在困难场景的稳定性 |
| Chen et al., *AIM-SLAM: Adaptive Integration of foundation Models for SLAM* | 2024 | 自适应基础模型集成，按需调用不同模型，效率-精度平衡 |
| Li et al., *CALM: Collaborative Active Learning and Mapping with Foundation Models* | 2024 | 主动学习 + 基础模型，协同探索与建图，减少数据依赖 |

这组论文的共性是：放弃手工设计的特征提取和匹配管线，改用预训练基础模型直接推断几何量。MASt3R-SLAM 标志着一个转折点——SLAM 的前端不再需要逐帧特征检测和匹配，而是由基础模型一次性提供密集几何先验。VGGT 则预示更激进的方向：一个模型同时输出深度、位姿、点云和内参。

---

### A.5 开放词汇、场景图与具身地图

这组论文代表 SLAM 的终极目标：从几何地图升级为机器人可用的空间知识表示。

| 论文 | 年份 | 讲解重点 |
|------|------|---------|
| Huang et al., *VLMaps: Visual-Language Maps for Robot Navigation* | 2023 | 视觉-语言融合地图，CLIP 特征索引，自然语言导航目标定位 |
| Gu et al., *ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning* | 2024 | 开放词汇 3D 场景图，对象级节点，关系边，支持复杂推理 |
| Shah et al., *VLFM: Vision-Language Frontier Maps for Zero-Shot Navigation* | 2023 | 前沿地图 + VLM，零样本目标导航，语义前沿探索 |
| Gao et al., *3D-Mem: 3D Spatial Memory for Embodied Agents* | 2024 | 3D 空间记忆表示，可查询、可更新，具身代理的长期空间记忆 |
| Rosinol et al., *3D Dynamic Scene Graphs: Actionable Spatial Perception* | 2021 | 语义建图综述性贡献，动态场景图，空间感知与行动桥接 |
| Chen et al., *OVO: Open-Vocabulary Occupancy* | 2024 | 开放词汇占据预测，任意类别语义标注，3D 占据网格 |
| Krantz et al., *MapNav: A Map-Based Zero-Shot Language Navigation Framework* | 2024 | 拓扑语义地图导航，地图引导的零样本语言导航 |
| Gao et al., *WMNav: World Model based Navigation with 3D Gaussian Splatting* | 2024 | 世界模型 + 3DGS 导航，预测-规划闭环 |
| Zhang et al., *NaVILA: Natural Language Navigation with Visual Language Models* | 2024 | VLM 驱动自然语言导航，视觉-语言-行动对齐 |
| Liu et al., *NavFoM: Navigation with Foundation Models* | 2024 | 基础模型统一导航框架，多模态感知-决策 |
| Chen et al., *OnlinePG: Online 3D Scene Graph Generation* | 2024 | 在线 3D 场景图生成，流式处理，实时场景图构建 |
| Azuma et al., *OGScene3D: Open-Grounded 3D Scene Understanding* | 2024 | 开放集 3D 场景理解， grounding + 3D 场景分析 |
| Huang et al., *Physically Executable 3D Gaussian Splatting with Geometric Constraints* | 2024 | 物理可执行 3DGS，几何约束，物理一致性 |

这 13 篇论文的共同指向是：地图不再是仅供人看的 3D 模型，而是机器人可查询、可推理、可行动的空间知识库。VLMaps 建立了语言-空间的索引，ConceptGraphs 将地图提升为关系图结构，3D-Mem 和 GSMem 则关注长期记忆的可操作性。2024-2025 年的趋势是 3DGS 作为语义地图的底层表示、VLM/LLM 作为语义理解的上层接口、二者通过开放词汇机制桥接。



---

## 附录B：全书固定写作模板

本书各章遵循统一的结构模板，确保读者在不同技术主题间切换时，始终知道"这一章要解决什么问题""新方法的突破口在哪""还有什么没解决"。

---

### B.1 章节结构模板（10 步）

每章正文按以下 10 步组织，不跳步、不合并。

**1. 本章要解决什么问题**

用 1-2 段直接回答：这一技术分支在 SLAM 版图中的位置是什么？为什么需要专门一章？当前的技术状态卡在哪个具体问题上？

**2. 传统方法怎么做**

简洁概述传统方案的核心流程。不过度展开历史，只讲清楚传统方法的输入输出、关键假设和工程实现路径。已在前章详细讲过的方法，此处直接引用，重复不超过 3 句话。

**3. 关键瓶颈是什么**

直击要害，指出传统方法在精度、效率、泛化性、可扩展性、语义能力五个维度中的哪一个（或几个）出现了瓶颈。瓶颈分析必须具体，避免"效果不够好"之类的笼统表述。

**4. 新方法的核心洞察**

一句话概括新方法的突破口。这句话应该能让读者在读完本章后仍然记得。例如："3DGS 的关键洞察是：用显式的各向异性高斯椭球代替隐式神经网络场，将渲染从射线采样变为光栅化。"

**5. 系统结构**

模块化描述系统的组成部分及其交互关系。用箭头图或流程图表示数据流。每个模块的职责一句话说明，不展开实现细节。

**6. 关键公式或伪代码**

只放最必要的公式或伪代码块。必要性判断标准：删掉后本章的核心思想无法完整表达。公式不超过 5 行，伪代码不超过 15 行。不贴完整源码。

**7. 代表论文精读**

每章精读 2-4 篇代表性论文，使用 B.2 节的论文精读模板。精读论文的选择标准：里程碑意义、方法独特、对后续研究影响深远。

**8. 优点、失败模式、适用场景**

诚实评估。列出新方法的明确优势（≥3 点），然后列出已知的失败模式或局限性（≥2 点），最后给出适用场景建议。避免一味赞美，也避免为批判而批判。

**9. 与具身智能的关系**

说明本章技术在具身智能系统中的角色。它如何支撑感知、导航、操作或世界模型？还有哪些鸿沟需要填补？

**10. 本章一句话总结**

用一句话总结全章核心信息。这句话应当独立成立，读者只看这句话也能抓住本章要义。

---

### B.2 论文精读模板（10 问）

每篇精读论文回答以下 10 个问题，按顺序回答，不跳问。

**1. 论文试图解决什么痛点？**

该论文要解决的具体技术问题是什么？这个问题为什么在当时重要？不超过 3 句话。

**2. 核心假设是什么？**

该方法成立的前提条件有哪些？包括环境假设、传感器假设、数据分布假设。明确区分合理假设和潜在限制性假设。

**3. 输入输出是什么？**

系统输入（传感器类型、分辨率、帧率）和输出（位姿、地图、语义标签等）的精确定义。标称运行环境（室内/室外、动态/静态）。

**4. 地图表示是什么？**

地图的数据结构是什么？稀疏点云、体素网格、神经隐式场、3D 高斯、场景图，还是混合表示？存储复杂度如何？

**5. Tracking 怎么做？**

前端位姿估计的核心方法。特征匹配、直接法、学习法、基础模型法？关键帧策略？与地图的耦合方式？

**6. Mapping 怎么做？**

地图构建和更新的核心方法。BA、滑窗优化、因子图、端到端学习、可微渲染？地图如何随新观测增长或修正？

**7. 优化目标是什么？**

写出（或描述）核心损失函数或目标函数。包括几何项、光度项、语义项、正则项的权重关系。优化变量有哪些？

**8. 相比前作真正推进了什么？**

定量指标上的提升或定性能力上的突破。必须是具体推进，而非"我们做了实验"式的泛泛描述。用数据说话。

**9. 没有解决什么？**

诚实列出该论文明确承认或未涉及的局限性。包括运行条件限制、未处理的 corner case、未公开的训练数据等。

**10. 对后续研究的影响是什么？**

该论文引发了哪些后续工作？哪个技术方向因它而成立？它的思路被哪篇后续论文继承或推翻？

---

### B.3 格式规范

**术语与引用**
- 专业术语首次出现时给出简明解释，如"光度误差（photometric error，即像素亮度差异）"
- 论文引用在正文中标注来源，格式为 `(arXiv)`、`(CVF 开放获取)`、`(IEEE)`、`(SIGGRAPH)` 等
- 不收集参考文献列表于章末

**表格与图表**
- 表格用于结构化对比（如方法对比、精度对比、运行速度对比）
- 每个表格后必须有 ≥50 字的分析解读，说明表格揭示的趋势或关键结论
- 代码块仅用于伪代码或关键公式

**段落与表达**
- 短段落（不超过 5 句），短句子（不超过 30 字）
- 禁止空洞开头："众所周知""值得注意的是""需要指出的是"
- 禁止长句子和绕弯子的表达
- 每句话必须携带实质性信息

---

## 附录C：全书技术主线图

本书的技术主线可以用一条九阶段演进链概括。每个阶段的标志性能力、代表方法、核心矛盾如下。

---

### 阶段一：传统几何 SLAM（1986-2007）

标志性能力：概率状态估计，同时定位与建图的形式化定义。

代表方法：EKF-SLAM、FastSLAM、UKF-SLAM。

核心矛盾：滤波方法的理论优美 vs. 计算复杂度和线性化误差。EKF 的 O(n²) 更新复杂度限制了地图规模，FastSLAM 用 RBPF 缓解了这个问题，但粒子退化始终是天花板。

### 阶段二：视觉 / 激光 / VIO 工程系统（2007-2019）

标志性能力：实时运行、大规模场景、工程鲁棒性。

代表方法：PTAM、ORB-SLAM 1/2/3、DSO、LSD-SLAM、VINS-Mono、LOAM、LIO-SAM、Kimera。

核心矛盾：几何精度已足够高，但地图是"死的"——稀疏点云或 mesh 无法承载语义信息，无法被下游任务直接查询。

### 阶段三：学习特征、匹配、深度、光流（2018-2021）

标志性能力：SLAM 的感知模块被神经网络逐个替换。

代表方法：SuperPoint（学习特征点）、SuperGlue/LightGlue（学习匹配）、Monodepth/AdaBins（学习深度）、RAFT（学习光流）。

核心矛盾：单个模块的替换带来精度提升，但模块间的耦合未被重新设计。SuperPoint + SuperGlue 的组合强大，但后端优化仍然沿用传统 BA。

### 阶段四：DROID-SLAM 类可微优化 SLAM（2021-2023）

标志性能力：前端-后端一体化可微分训练，数据驱动的优化器。

代表方法：DROID-SLAM、DPVO、TartanVO。

核心矛盾：证明了 SLAM 可以端到端学习，但训练数据分布决定了泛化边界。在训练数据分布内表现卓越，跨域时稳定性不如传统方法。

### 阶段五：iMAP / NICE-SLAM / NeRF-SLAM 神经地图（2021-2023）

标志性能力：连续神经场景表示，可渲染的隐式地图。

代表方法：iMAP（MLP 地图）、NICE-SLAM（分层编码）、NeRF-SLAM（Instant-NGP 加速）。

核心矛盾：NeRF 的连续性带来了优美的地图表示，但射线采样的渲染开销难以满足实时性。隐式表示无法直接编辑或语义标注。

### 阶段六：3DGS-SLAM 可渲染显式地图（2023-2025）

标志性能力：各向异性 3D 高斯作为显式地图基元，光栅化渲染实时。

代表方法：SplaTAM、MonoGS、Splat-SLAM、SGS-SLAM、OpenGS-SLAM。

核心矛盾：3DGS 解决了 NeRF 的实时性问题，但高斯基元的无序性带来了新的管理挑战。动态场景、长期运行、多会话融合仍待解决。

### 阶段七：开放词汇语义 3DGS / 场景图（2024-2025）

标志性能力：地图承载开放词汇语义，支持自然语言查询。

代表方法：VLMaps、ConceptGraphs、SGS-SLAM、OpenGS-SLAM、GSFF-SLAM。

核心矛盾：语义标注从封闭类别走向开放词汇，但语义精度与几何精度的耦合关系尚不明确。场景图的自动构建仍依赖启发式规则。

### 阶段八：3D-Mem / GSMem 空间记忆（2024-2025）

标志性能力：地图作为具身代理的长期空间记忆，可查询、可更新、可推理。

代表方法：3D-Mem、GSMem、VLFM。

核心矛盾：空间记忆的表示形式（3DGS vs. 场景图 vs. 体素）尚未收敛。记忆的更新、遗忘、压缩机制处于早期探索阶段。

### 阶段九：VLM / LLM / VLA 具身导航与世界模型（2025- ）

标志性能力：大模型驱动的感知-决策-行动闭环，世界模型预测未来。

代表方法：NaVILA、NavFoM、WMNav、Gemini Robotics。

核心矛盾：VLM/VLA 的行动能力取决于底层空间表示的质量。没有稳定的空间记忆，大模型无法完成需要"记住空间布局"的复杂任务。

---

### 主线图汇总

```
传统几何 SLAM（1986-2007）
    ↓  滤波 → 图优化，稀疏 → 稠密
视觉 / 激光 / VIO 工程系统（2007-2019）
    ↓  感知模块逐个被神经网络替换
学习特征、匹配、深度、光流（2018-2021）
    ↓  可微分优化替代手工设计的前后端
DROID-SLAM 类可微优化 SLAM（2021-2023）
    ↓  连续神经场景表示，可渲染地图
iMAP / NICE-SLAM / NeRF-SLAM 神经地图（2021-2023）
    ↓  显式高斯基元替代隐式场，实时渲染
3DGS-SLAM 可渲染显式地图（2023-2025）
    ↓  开放语义标注，自然语言查询
开放词汇语义 3DGS / 场景图（2024-2025）
    ↓  地图升级为可查询、可更新的空间记忆
3D-Mem / GSMem 空间记忆（2024-2025）
    ↓  大模型驱动感知-决策-行动闭环
VLM / LLM / VLA 具身导航与世界模型（2025- ）
```

这条主线的底层逻辑：地图表示的每一次升级（稀疏点云 → 稠密点云 → 隐式场 → 3D 高斯 → 语义高斯 → 空间记忆），都对应着 SLAM 从"定位工具"向"空间智能基础设施"的角色跃迁。


---

## 附录D：本书最应该反复强调的 10 个判断

这 10 个判断贯穿全书，是对 SLAM 到空间智能演进规律的高度浓缩。每个判断附有简短展开，说明其成立依据和实践含义。

---

### 判断 1：SLAM 的核心不是传感器，而是约束组织

SLAM 常被按传感器类型分类——视觉 SLAM、激光 SLAM、VIO、RGB-D SLAM。这种分类在工程选型时有参考价值，但掩盖了本质。

无论传感器如何变化，SLAM 的核心问题始终是：如何将大量不完美的局部观测组织成全局一致的空间表示。这需要处理三类约束——帧间约束（odometry）、环回约束（loop closure）、先验约束（IMU 预积分、GPS、深度先验）。传感器的差异仅在于约束的来源和精度不同。

ORB-SLAM3 能融合单目、双目、RGB-D 和 IMU，不是因为每种传感器有独立的 SLAM 算法，而是因为它有一套统一的约束管理框架。MASt3R-SLAM 用基础模型替代传统前端，后端仍然是 BA 优化约束。这个判断意味着：学习新的传感器模型比学习新的 SLAM 算法容易得多，真正困难的是约束的检测、验证和优化。

### 判断 2：地图表示决定系统上限

地图是 SLAM 的"中心数据结构"，它决定了系统能回答什么样的问题、支持什么样的下游任务、在多长的时间尺度上保持有效。

稀疏点云地图（ORB-SLAM）只能回答"我在哪"，无法回答"那个红色椅子旁边有什么"。体素网格（KinectFusion）可以回答空间占据问题，但存储开销巨大且分辨率固定。NeRF（iMAP）提供了连续表示和照片级渲染，但无法直接编辑、语义标注或碰撞检测。3D 高斯（MonoGS）兼顾了渲染质量和显式结构，但基元管理仍是开放问题。

这个判断意味着：选择地图表示时，不能只比较渲染质量或定位精度，而要追问——这个表示能否被机器人查询？能否被语言模型理解？能否在运行中增量更新？能否在设备间传输和合并？2025 年后，地图表示的竞争维度已从"建得多好看"转向"用得多方便"。

### 判断 3：传统 SLAM 解决的是几何一致性，具身智能需要语义一致性和任务一致性

传统 SLAM 的优化目标是几何一致性（geometric consistency）——保证地图不畸变、轨迹不漂移。这在地图构建阶段是必要的，但对机器人完成任务远远不够。

语义一致性（semantic consistency）要求地图中的语义标注在空间和时间上稳定。"桌子"在这一帧被检测到，在下一帧不应该变成"椅子"，在世界坐标系中不应该出现在天花板上。任务一致性（task consistency）要求地图的内容和精度适配当前任务。导航任务需要知道通道宽度，操作任务需要知道物体抓取面的精确位置，两者对地图精度的需求不同。

ConceptGraphs 和 VLMaps 的出发点正是这个判断：仅有几何精度的地图无法满足具身任务需求，地图必须承载语义、支持任务导向的查询。

### 判断 4：NeRF 让 SLAM 看见了连续神经地图，但 3DGS 让神经地图更接近实时系统

2021 年 iMAP 首次将 NeRF 引入 SLAM，用 MLP 编码整个场景，通过可微渲染联合优化相机位姿和场景几何。NICE-SLAM 用分层特征网格加速了训练。但射线渲染（ray marching）的固有开销使这些方法难以达到 30 FPS。

2023 年 3D Gaussian Splatting 改变了这一点。高斯基元是显式的，渲染通过 tile-based 光栅化完成，不需要神经网络推理。MonoGS 和 SplaTAM 在 2024 年证明 3DGS-SLAM 可以在消费级 GPU 上实时运行。这个判断的实质是：NeRF 证明了神经地图的可行性，3DGS 证明了神经地图的可用性。

### 判断 5：3DGS-SLAM 的关键不是画质，而是可渲染、可优化、可语义化的地图接口

初看 3DGS-SLAM 容易被其高质量的渲染效果吸引，但这只是表面。真正重要的价值在于 3DGS 提供了一种同时满足三个条件的地图表示：

- **可渲染**（renderable）：光栅化速度足够快，支持实时视图合成
- **可优化**（optimizable）：高斯参数可微，可通过梯度下降调整位置和形状
- **可语义化**（semanticizable）：每个高斯可以附加语义特征向量，支持开放词汇查询

传统点云可优化但不可直接渲染。NeRF 可渲染可优化但不可直接语义化（需要额外网络）。3DGS 是目前唯一同时满足三者的表示。SGS-SLAM 在高斯上附加语义标签，GSFF-SLAM 注入 DINO 特征，OpenGS-SLAM 实现了开放词汇查询——这些扩展之所以可行，正是因为 3DGS 的显式结构提供了可操作的语义接口。

### 判断 6：2025 年以后，SLAM 前端开始被视觉几何基础模型重写

2024 年 DUSt3R 的问世标志了一个拐点：单张或两张 RGB 图像可以直接回归密集 3D 点图，无需相机内参，零样本泛化。MASt3R 在此基础上增加了快速互匹配和单图深度估计。VGGT 更进一步，一个 Transformer 同时输出深度、位姿、点云和相机内参。

MASt3R-SLAM（2025）将这种能力整合进了实时 SLAM 系统：用 MASt3R 的匹配特征替代传统特征点检测和描述，后端仍然用 BA。这意味着 SLAM 前端的设计范式正在从"检测-描述-匹配"向"推理-对应-优化"转型。前端的工程复杂度降低，但对基础模型的推理效率和泛化能力提出了更高要求。

这个判断不意味着传统特征点（ORB、SIFT）会立即消失——它们在资源受限设备和极端光照条件下仍有优势。但长期趋势明确：基础模型将承担越来越大的前端计算负担。

### 判断 7：开放词汇地图是机器人和语言模型之间的空间接口

传统 SLAM 的语义层使用封闭类别（预先定义的 COCO 类别），这在开放世界中远远不够。机器人需要理解"那个半满的咖啡杯在键盘左边"这样的描述，其中"半满"和"左边"都不在 COCO 类别中。

开放词汇地图通过将 CLIP/DINO 等视觉-语言特征与 3D 地图绑定，实现了任意自然语言查询。VLMaps 将 CLIP 特征索引到 2D 网格，ConceptGraphs 构建开放词汇 3D 场景图，OpenGS-SLAM 将 CLIP 特征附加到 3D 高斯。这个判断意味着：地图不再是仅供 SLAM 内部使用的数据结构，而是机器人与大语言模型交互的媒介——LLM 通过地图理解空间，机器人通过地图执行任务。

### 判断 8：具身智能不会淘汰 SLAM，而是要求 SLAM 从定位模块升级为空间记忆模块

一个常见的误解是：有了大模型和端到端学习，SLAM 将被淘汰。恰恰相反——具身智能对空间表示的需求比传统 SLAM 更强烈、更多样。

传统 SLAM 回答"我在哪"和"周围环境的几何结构是什么"。具身智能需要回答"这个物体我之前在哪里见过""那个区域我还没探索过""从 A 到 B 的最安全路径是什么""如果把椅子推到桌子旁边，通道宽度还够不够"。这些问题需要一个可查询、可更新、可推理的空间记忆系统，而不是一个只能输出当前位姿的定位模块。

3D-Mem 和 GSMem 的方向正是这个升级：将 SLAM 的输出从"位姿 + 地图文件"转变为"可操作的空间记忆服务"，支持插入、查询、更新、压缩和遗忘。

### 判断 9：VLM/VLA 的行动能力取决于它是否拥有稳定、可查询、可更新的空间表示

当前 VLM（视觉-语言模型）可以回答关于图像的复杂问题，VLA（视觉-语言-行动模型）可以输出低级控制指令。但当面对需要空间记忆的长期任务时，它们表现急剧下降。

原因明确：LLM 的上下文窗口无法承载精细的空间几何信息，VLM 只能看到当前帧的 2D 投影。没有 3D 空间表示，VLA 无法完成以下任务："去厨房拿放在冰箱旁边的蓝色杯子，然后回到客厅放在茶几上"——这需要记住厨房布局、杯子位置、导航路径，这些远超 2D 视觉的承载能力。

这个判断意味着：VLM/VLA 的上限受限于底层空间表示的质量。空间表示越稳定（几何一致、语义一致、时间一致），上层模型的行动能力越强。GSMem 等空间记忆系统正是为了填补这个鸿沟。

### 判断 10：2026 之后最重要的问题不是"能不能建图"，而是"地图能不能支撑长期、动态、开放世界中的行动"

建图能力本身已趋于成熟。传统 SLAM 在结构化室内环境中可以实现厘米级精度，3DGS-SLAM 可以实时构建视觉质量令人满意的地图，基础模型可以从单图推断密集几何。

真正的挑战在"建图之后"：

- **长期**：地图如何在数周、数月内保持有效？物体移动了怎么办？新区域如何增量融合？记忆如何压缩和遗忘？
- **动态**：如何处理人或车辆的持续移动？动态物体是建图的一部分还是障碍物？动态预测能否融入地图？
- **开放世界**：训练集中没见过的物体类别如何处理？光照变化、季节变化如何保持语义一致性？不同机器人之间的地图如何共享和融合？

这三个问题的交汇点定义了 SLAM 研究下一个十年的核心议程：从"建图系统"到"空间记忆基础设施"。

---

