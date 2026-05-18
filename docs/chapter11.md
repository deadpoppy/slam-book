# 第三篇：3D Gaussian Splatting SLAM：2024–2026 的主战场

# 第11章 早期 3DGS-SLAM：SplaTAM、MonoGS 与 Gaussian SLAM

第10章论证了 3D Gaussian Splatting（3DGS）作为场景表示的结构性优势：显式参数化支持随机访问、可微光栅化带来实时渲染、α-混合天生适合密度建模。这些特性为 SLAM 提供了全新的技术选项。2023 年底到 2024 年初，三个几乎同时出现的系统——SplaTAM、MonoGS 和 FlashSLAM——以不同的切入点验证了"地图能渲染"这一思想在 SLAM 中的工程可行性。它们共同定义了 3DGS-SLAM 的第一代范式。

这三个系统分工明确：SplaTAM 证明了 RGB-D 输入下 3DGS 可以同时做到精确跟踪和高保真建图；MonoGS 把问题推向更难的单目设定，展示了 3DGS 在无任何深度先验时的潜力；FlashSLAM 则指出纯梯度下降式跟踪的瓶颈，用特征匹配加速跟踪pipeline。三者叠加，勾勒出早期 3DGS-SLAM 的技术版图。

---

## 11.1 SplaTAM：Splat, Track & Map 3D Gaussians

### 11.1.1 核心问题

Dense SLAM 需要同时估计相机轨迹和重建稠密三维场景。NeRF-SLAM 系列（如 NICE-SLAM、Point-SLAM）使用隐式或半隐式表示，渲染需要耗时的光线 march，地图扩展缺乏结构化的密度控制机制。SplaTAM 问了一个直接的问题：如果把场景表示为显式的 3D Gaussian 集合，是否能让 tracking、mapping 和 rendering 都变得更快、更可控？

答案是肯定的。SplaTAM 的地图是一张 3D Gaussian 参数表，渲染是光栅化而非光线求交，地图扩展通过"在需要的地方添加新的 Gaussian"完成。整个系统围绕可微渲染构建，把"渲染-比较-回传梯度"作为 tracking 和 mapping 的统一优化机制。

### 11.1.2 高斯地图表示

SplaTAM 对每个 Gaussian 做了简化：强制各向同性（isotropic），每个 Gaussian 仅由 8 个参数描述——位置 $\mu \in \mathbb{R}^3$、RGB 颜色 $c \in \mathbb{R}^3$、半径 $r \in \mathbb{R}^+$ 和不透明度 $o \in [0,1]$。空间影响函数为：

$$
f(x) = o \cdot \exp\left(-\frac{\|x - \mu\|^2}{2r^2}\right)
$$

各向同性的牺牲是表达能力——无法描述细长的结构如电线、杆状物体。但收益也很显著：参数更少、光栅化更快、梯度传播更稳定。SplaTAM 的实验表明，对于室内 RGB-D SLAM，各向同性 Gaussian 足以重建出厘米级精度的几何。

### 11.1.3 Tracking：通过可微渲染优化位姿

SplaTAM 的 tracking 模块接收当前 RGB-D 帧，通过可微光栅化将当前高斯地图投影到相机坐标系，生成颜色图、深度图和轮廓图（silhouette map）。优化目标为：

$$
\mathcal{L}_{\text{track}} = \lambda_c \|C_{\text{render}} - C_{\text{obs}}\|_1 + \lambda_d \|D_{\text{render}} - D_{\text{obs}}\|_1 + \lambda_s \|S_{\text{render}} - S_{\text{obs}}\|_1
$$

其中轮廓图 $S$ 是关键创新。SplaTAM 渲染一张二值化的 silhouette mask，标识"哪些像素被至少一个 opaque Gaussian 覆盖"。在跟踪时，loss 只施加在有可靠地图覆盖的像素上，避免新观测区域或空洞区域的干扰。这相当于给跟踪过程增加了一个"自信区域掩码"，大幅提升了在大运动和无纹理场景下的鲁棒性。

位姿优化在 SE(3) 流形上进行，使用解析梯度通过光栅化反向传播。每帧跟踪通常需要 50–100 次迭代收敛。

### 11.1.4 Mapping：关键帧驱动的地图更新

Mapping 线程维护一个关键帧窗口。当新关键帧被选中时，系统执行以下操作：

1. **高斯初始化**：将新关键帧的深度图反投影到 3D，在每个有效深度像素处初始化一个 Gaussian。
2. **联合优化**：固定相机位姿，在当前窗口内的所有关键帧上优化 Gaussian 参数（位置、颜色、半径、不透明度）。
3. **密化（Densification）**：检查当前渲染误差大的区域，在这些区域添加新的 Gaussian。
4. **剪枝（Pruning）**：移除透明度过低或对渲染贡献极小的高斯。

高斯参数通过 Adam 优化器更新。Mapping loss 与 tracking loss 形式相同，但只优化地图参数而不动位姿。

### 11.1.5 Silhouette 驱动的地图扩展

SplaTAM 的轮廓 mask 不仅用于 tracking，还用于控制地图扩展。当渲染的 silhouette 在某个区域为 0（即没有 Gaussian 覆盖该区域），而深度观测在该区域有有效读数时，系统将反投影这些新观测点并实例化为新的 Gaussian。这种"只在需要的地方生长"的策略避免了冗余 Gaussian 的堆积。

### 11.1.6 实验结果

SplaTAM 在 Replica、ScanNet、ScanNet++ 和 TUM-RGBD 四个数据集上进行了评估。在 Replica 上，SplaTAM 的 ATE RMSE 约为 0.3–0.6 cm，比 Point-SLAM 提升约 2 倍。新视角合成质量同样领先：PSNR 在 Replica office 场景达到约 35 dB，LPIPS 低至 0.07。渲染速度达到 400 FPS（分辨率 $876 \times 584$），远超 NeRF-based SLAM 的个位数 FPS。

### 11.1.7 论文精读

**论文试图解决什么痛点？**
NeRF-SLAM 系列在 dense RGB-D SLAM 中占据主导，但隐式表示导致渲染慢、地图扩展缺乏结构化控制、无法显式判断"某区域是否已被建图"。SplaTAM 要做一个渲染快、地图扩展结构化、支持显式空间查询的 dense SLAM。

**核心假设是什么？**
RGB-D 输入提供足够的几何先验，使得各向同性 3D Gaussian 足以表达室内场景；可微光栅化提供的梯度足够精确，可以直接优化相机位姿。

**输入输出是什么？**
输入：RGB-D 图像序列，已知相机内参。输出：相机轨迹（SE(3) 位姿序列）、3D Gaussian 地图（位置和属性）、新视角合成（颜色和深度渲染）。

**地图表示是什么？**
各向同性 3D Gaussian 集合，每个 Gaussian 8 参数：位置 $\mu$、颜色 $c$、半径 $r$、不透明度 $o$。

**Tracking 怎么做？**
当前帧位姿通过可微渲染与已有地图比较，最小化颜色、深度和轮廓的渲染误差，使用解析梯度在 SE(3) 上优化。轮廓 mask 限制 loss 只在有地图覆盖的可靠区域上计算。

**Mapping 怎么做？**
关键帧维护滑动窗口，窗口内固定位姿优化 Gaussian 参数（Adam）。新关键帧触发深度反投影初始化新的 Gaussian，之后通过渲染误差驱动的 densification 和透明度驱动的 pruning 控制地图规模。

**优化目标是什么？**
Tracking 和 mapping 共享相同的渲染误差 loss：$\ell_1$ 颜色误差 + $\ell_1$ 深度误差 + $\ell_1$ 轮廓误差，通过权重平衡。

**相比前作真正推进了什么？**
首次将 3DGS 引入 dense RGB-D SLAM，用显式 Gaussian 替代隐式/半隐式表示，渲染速度从几 FPS 提升到数百 FPS。轮廓 mask 同时服务于 tracking 鲁棒性和地图结构化扩展，是同时期工作中最完整的系统级设计。

**没有解决什么？**
各向同性 Gaussian 无法精确表达细长结构。纯梯度下降 tracking 在大运动和运动模糊下仍可能失败。没有回环检测，长序列会累积漂移。依赖 RGB-D 输入，无法处理纯 RGB 场景。

**对后续研究的影响是什么？**
SplaTAM 证明了 3DGS-SLAM 的基本可行性，定义了"tracking by rendering + mapping by differentiable splatting"的范式。后续工作在它的基础上引入各向异性 Gaussian、特征匹配辅助跟踪、以及回环闭合。

---

## 11.2 MonoGS / Gaussian Splatting SLAM：单目 Gaussian SLAM

### 11.2.1 核心问题

SplaTAM 依赖 RGB-D 输入，深度传感器提供了至关重要的几何尺度。但纯单目相机是最常见、最便宜的传感器，也是 SLAM 中最难处理的设定：没有绝对深度，尺度模糊，几何初始化困难。MonoGS 要做的是把 3DGS-SLAM 从 RGB-D 推进到单目。

MonoGS 是首个主要依赖 3D Gaussian Splatting 的单目 dense SLAM 系统，同时也支持 stereo 和 RGB-D 输入。它运行速度约为 3 FPS（单目输入），在当时已接近实时。

### 11.2.2 从 SfM 到 SLAM：在线高斯初始化

原始 3DGS（Kerbl et al., 2023, ACM TOG）需要 COLMAP 提供的精确位姿作为先验，在离线状态下优化 Gaussian。MonoGS 必须在线地、从无到有地构建 Gaussian 地图，同时估计位姿。这是一个"先有鸡还是先有蛋"的问题：精确地图需要好位姿，好位姿又依赖好地图。

MonoGS 的解决方案分两步：

**第一步：初始地图构建。** 前两帧通过特征匹配（SuperPoint + LightGlue）和三角测量获得稀疏 3D 点，将这些点转换为初始 Gaussian。初始 Gaussian 具有较大的协方差（各向同性球体），半径设置为平均场景深度的 10%–20%，以表达初始深度的不确定性。

**第二步：增量式 densification。** 对于新关键帧，系统利用已有的多视图位姿估计深度图，在高图像梯度区域或深度不连续区域初始化新的 Gaussian。与 SplaTAM 直接反投影深度不同，MonoGS 的 densification 需要考虑深度的不确定性——新 Gaussian 的半径与其深度估计的不确定性成正比。深度不确定区域获得更大的初始半径，从而在后续优化中有更大的自由度调整。

### 11.2.3 Tracking：直接优化与解析 Jacobian

MonoGS 的 tracking 直接对当前帧位姿进行优化，loss 为光度误差：

$$
\mathcal{L}_{\text{track}} = (1 - \lambda) \|C_{\text{render}} - C_{\text{obs}}\|_1 + \lambda (1 - \text{SSIM}(C_{\text{render}}, C_{\text{obs}}))
$$

相比 SplaTAM，MonoGS 的 tracking 有两个关键差异：

1. **没有深度监督**：单目输入下，跟踪只能依赖光度一致性。这导致 tracking 的收敛 basin 比 RGB-D 版本窄，对初始位姿更敏感。
2. **解析 Jacobian**：MonoGS 推导了位姿对渲染像素的解析 Jacobian（在 SE(3) 流形上），避免了数值微分的高昂开销。这是 MonoGS 能在 3 FPS 运行的关键。

### 11.2.4 几何正则化

单目 SLAM 面临严重的几何歧义：纹理缺乏区域可以收缩为薄片（plane collapse），细长物体会被拉成"面条"。MonoGS 引入两项正则化来对抗这些问题：

**各向同性正则化（Isotropic Regularization）：** 惩罚过度拉伸的 Gaussian。Loss 项为：

$$
\mathcal{L}_{\text{iso}} = \lambda_{\text{iso}} \sum_i \|\Sigma_i - \frac{\text{tr}(\Sigma_i)}{3} I\|_F
$$

其中 $\Sigma_i$ 是第 $i$ 个 Gaussian 的协方差矩阵。此项强迫 Gaussian 接近球形，避免极端拉伸。

**几何验证（Geometric Verification）：** 在 densification 时，通过多视图一致性检查新三角化点的可靠性。只有被至少两个视角以一致深度观测到的点才允许实例化为 Gaussian。

### 11.2.5 关键帧管理与窗口优化

MonoGS 维护一个局部关键帧窗口（通常 3–5 帧）。每个新关键帧加入窗口时，触发 densification 和一轮 joint optimization——同时优化窗口内所有关键帧的位姿和地图 Gaussian 参数。

关键帧选择策略基于视角变化：当当前帧与最后一个关键帧的平移或旋转超过阈值时，触发新关键帧。这保证了地图更新的均匀性。

### 11.2.6 实验结果

MonoGS 在 Replica 和 TUM-RGBD 上进行了评估（单目输入）。在 Replica 上，ATE RMSE 约为 1–2 cm，新视角合成 PSNR 达到 25 dB 以上。对于单目 SLAM，这是当时最好的结果。

MonoGS 的渲染质量尤其突出：透明物体（如玻璃杯）、细长结构（如电线）都被高保真重建。这是传统特征点法或甚至 NeRF-SLAM 难以企及的——显式 Gaussian 可以自然地表达半透明材质和复杂几何。

### 11.2.7 论文精读

**论文试图解决什么痛点？**
3DGS 在离线新视角合成中表现出色，但需要预先知道精确位姿。单目 SLAM 没有精确位姿，也没有深度图，如何在线地从零开始构建 Gaussian 地图？

**核心假设是什么？**
单目相机的连续帧间运动足够小，使得光度 tracking 可以收敛；多视图三角化提供的稀疏深度足以"引导"Gaussian 的增量初始化；几何正则化可以抑制单目重建固有的歧义。

**输入输出是什么？**
输入：单目 RGB 图像序列（也支持 stereo/RGB-D），已知内参。输出：相机轨迹（SE(3) 位姿，绝对尺度由 stereo 或 RGB-D 提供，单目下尺度不确定）、3D Gaussian 地图、新视角合成。

**地图表示是什么？**
各向异性 3D Gaussian，每个 Gaussian 由位置 $\mu$、协方差矩阵 $\Sigma$（通过缩放-旋转分解参数化）、颜色 $c$（球谐系数）和不透明度 $o$ 描述。比 SplaTAM 更完整的参数化，但增加了优化复杂度。

**Tracking 怎么做？**
固定 Gaussian 地图，通过可微光栅化渲染当前视角，最小化光度误差（L1 + SSIM），使用解析 Jacobian 在 SE(3) 上梯度下降优化位姿。

**Mapping 怎么做？**
关键帧窗口内的多帧联合优化，同时调整位姿和 Gaussian 参数。新关键帧触发深度估计和 densification，在深度不连续和高梯度区域插入新 Gaussian。周期性执行 opacity pruning 和 Gaussian merging 保持地图紧凑。

**优化目标是什么？**
Tracking：L1 颜色误差 + (1 - SSIM)。Mapping：相同的光度误差 + 各向同性正则化 + 深度平滑项（RGB-D 模式下）。

**相比前作真正推进了什么？**
首次实现单目 3DGS-SLAM，突破了 3DGS 依赖离线 SfM 位姿的限制。解析 Jacobian 让 tracking 速度提升数个量级。几何正则化和验证机制使得单目下的 Gaussian densification 成为可能。

**没有解决什么？**
3 FPS 的速度不够实时。单目 tracking 的收敛 basin 窄，大运动下容易失败。没有回环检测。单目尺度模糊问题未根本解决。densification 策略仍较启发式。

**对后续研究的影响是什么？**
MonoGS 证明 3DGS 可以处理最困难的单目 SLAM 设定，启发了大量后续工作。它的解析 Jacobian 和几何正则化成为后续 3DGS-SLAM 的标准组件。它也揭示了速度瓶颈：每帧数十次可微渲染迭代太慢，需要更快的跟踪策略。

---

## 11.3 FlashSLAM：加速 RGB-D Gaussian SLAM

### 11.3.1 核心问题

SplaTAM 和 MonoGS 的 tracking 都依赖梯度下降迭代——每帧需要 50–100 次可微渲染和反向传播。这在两个场景下成为瓶颈：

1. **稀疏视角**：当帧率降低（如每隔 5–10 帧取一帧），相邻帧间的运动增大，梯度下降需要更多迭代才能收敛，甚至可能陷入局部最优。
2. **大相机运动**：快速旋转或平移时，渲染图像与观测差异巨大，光度 loss 的 basin of attraction 不足以拉回正确位姿。

FlashSLAM 的洞察是：tracking 和 mapping 应该解耦。Tracking 负责快速估计位姿，不需要可微渲染；Mapping 负责高保真 Gaussian 优化，可以较慢进行。

### 11.3.2 Tracking：特征匹配 + 点云注册

FlashSLAM 的 tracking 模块不使用可微渲染。它采用了一个预训练的特征匹配网络（LoFTR），在当前帧与参考关键帧之间提取稀疏但可靠的特征匹配点。然后将这些匹配点提升到 3D（使用深度图），通过点云注册（Point Cloud Registration，具体使用 Kabsch 算法）直接求解相对位姿。

具体流程为：

1. **特征匹配**：当前帧与最近的参考关键帧通过预训练 LoFTR 网络提取密集对应点，再用 RANSAC 剔除外点。
2. **3D 点云构建**：利用深度图将匹配点反投影为两组 3D 点云。
3. **点云注册**：通过 Kabsch 算法求解两组点云之间的刚性变换（SE(3)）。
4. **多帧验证**：将估计的位姿与多个参考关键帧交叉验证，取一致性最好的结果。

这一流程的核心优势在于速度：特征匹配 + 点云注册的耗时约为 80 ms，比 SplaTAM 的梯度下降 tracking 快 90%。更重要的是，特征匹配对大运动不敏感——只要两帧之间有可匹配的特征，即使运动很大也能获得合理的初始对应。相比之下，梯度下降 tracking 的 basin of attraction 受限于帧间运动幅度，大运动时渲染图像与观测差异巨大，loss landscape 可能不存在通往全局最优的梯度路径。

### 11.3.3 Mapping：高斯优化与深度噪声建模

FlashSLAM 的 mapping 线程与 SplaTAM 类似：使用可微渲染优化 Gaussian 参数。但 FlashSLAM 增加了一个关键组件——**深度噪声建模**。

消费级 RGB-D 相机（如 iPhone 的 LiDAR）的深度图存在显著的噪声，特别是在边缘和远距离区域。FlashSLAM 在 tracking 中对深度进行不确定性加权，在 mapping 中对深度 loss 施加鲁棒核函数（Huber loss）。这使得它在低质量深度输入下仍能保持稳定。

### 11.3.4 实验结果

FlashSLAM 在 Replica、TUM-RGBD、ScanNet 和 ScanNet++ 上进行了评估。在 Replica 上平均 ATE 为 0.55 cm，与 SplaTAM 相当。在稀疏设置下（每 5 帧取一帧），FlashSLAM 的跟踪精度比 SplaTAM 提升 92%。Tracking 时间稳定在 80 ms 以下。

FlashSLAM 还展示了在 iPhone 采集的真实数据上的鲁棒性，验证了消费级设备上的实用性。

### 11.3.5 评价

FlashSLAM 的价值在于揭示了早期 3DGS-SLAM 的一个关键设计抉择：tracking 是否必须与 rendering 绑定？FlashSLAM 的答案是否定的。通过特征匹配和点云注册解耦 tracking，系统在速度和鲁棒性上获得了显著提升。

但这种解耦也有代价：特征匹配在低纹理区域可能失败（如 FlashSLAM 在 Replica office4 上的跟踪误差增大）；tracking 不再直接优化渲染质量，可能导致 tracking 和 mapping 之间的小不一致。后续工作（如第 12 章将讨论的）尝试在两者之间找到更好的平衡。

---

## 11.4 系统模式总结：第一代 3DGS-SLAM 的共性结构

SplaTAM、MonoGS 和 FlashSLAM 虽然侧重点不同，但共同定义了 3DGS-SLAM 的第一代系统架构。本节提炼五个核心模式，它们构成后续章节的技术基础。

### 11.4.1 Tracking by Rendering

这三个系统都验证了"通过渲染来跟踪"的核心思想：将当前地图渲染到相机视角，与观测图像比较，通过渲染误差反向传播到位姿参数。

| 系统 | Tracking 监督信号 | 优化方法 | 平均耗时/帧 |
|------|------------------|---------|-----------|
| SplaTAM | 颜色 + 深度 + 轮廓 | 梯度下降 (SE(3)) | ~2.7 s |
| MonoGS | 颜色 (L1 + SSIM) | 梯度下降 + 解析 Jacobian | ~0.33 s |
| FlashSLAM | 无渲染（特征匹配+点云注册） | Kabsch/ICP | ~0.08 s |

**分析：** 纯梯度下降 tracking（SplaTAM）最通用但最慢，每帧需要数十到上百次渲染迭代。解析 Jacobian（MonoGS）将速度提升约 8 倍，但仍受限于渲染开销。FlashSLAM 彻底绕过渲染做 tracking，速度最快，但依赖特征匹配的质量。这个 trade-off 成为后续 3DGS-SLAM 研究的主线：如何在保持渲染质量的同时加速 tracking。

### 11.4.2 Mapping by Differentiable Splatting

Mapping 是三个系统共同使用可微渲染的环节。固定相机位姿后，通过渲染误差优化 Gaussian 参数（位置、协方差、颜色、不透明度）。

可微 splatting 相比 NeRF 的光线 march 有两个结构性优势：

1. **速度快**：光栅化复杂度与像素数线性相关，而非与采样点数相关。渲染速度从 NeRF 的几 FPS 提升到 3DGS 的数百 FPS。
2. **梯度精确**：每个像素对可见 Gaussian 参数的梯度有闭式表达，避免了体渲染中采样噪声带来的梯度方差。

Mapping loss 通常包括颜色项 $\mathcal{L}_{\text{color}}$、深度项 $\mathcal{L}_{\text{depth}}$（RGB-D 模式）和正则化项 $\mathcal{L}_{\text{reg}}$：

$$
\mathcal{L}_{\text{map}} = \lambda_c \mathcal{L}_{\text{color}} + \lambda_d \mathcal{L}_{\text{depth}} + \lambda_r \mathcal{L}_{\text{reg}}
$$

### 11.4.3 Keyframe-Based Optimization

三个系统都采用关键帧驱动的优化策略。关键帧选择通常基于视角变化（平移/旋转阈值）或时间间隔。非关键帧只用于 tracking 不参与 mapping，从而控制计算量。

关键帧窗口通常维护 3–5 帧，在窗口内执行 joint optimization（同时优化位姿和地图）。窗口外的关键帧被固定，不再参与优化。这种滑动窗口机制平衡了计算效率和地图一致性。

### 11.4.4 Gaussian Densification and Pruning

地图的"生长"和"修剪"是 3DGS-SLAM 的核心操作：

**Densification（密化）：** 在渲染误差大、地图覆盖不足的区域添加新的 Gaussian。SplaTAM 通过 silhouette mask 识别未覆盖区域；MonoGS 在高图像梯度和深度不连续处插入；FlashSLAM 遵循类似的误差驱动策略。

具体操作中，densification 通常包括两个子操作：
- **克隆（Clone）**：对一个已有 Gaussian 进行复制并微调位置。
- **分裂（Split）**：将一个大 Gaussian 替换为两个更小的 Gaussian（通常沿最大梯度方向）。

**Pruning（剪枝）：** 移除对渲染贡献极低的 Gaussian。通常基于透明度阈值（$\alpha < \alpha_{\min}$）或可见性计数（从未被观测到的 Gaussian）。

| 操作 | 触发条件 | 效果 |
|------|---------|------|
| 克隆 | 位置梯度大且 Gaussian 小 | 在精细区域增加密度 |
| 分裂 | 投影半径超过阈值 | 用多个小 Gaussian 替代大 Gaussian |
| 剪枝 | 透明度 < 阈值 或 观测次数 < 阈值 | 移除漂浮物和冗余 Gaussian |

### 11.4.5 Pose-Map Joint Optimization

在关键帧时刻，系统执行 pose-map joint optimization：同时优化关键帧位姿和 Gaussian 参数。这与传统 SLAM 的 BA（Bundle Adjustment）本质相同，只是把路标点替换为 Gaussian 参数。

Joint optimization 的 loss 为所有关键帧上的渲染误差之和：

$$
\mathcal{L}_{\text{joint}} = \sum_{k \in \mathcal{W}} \|C_{\text{render}}(G, T_k) - C_{\text{obs},k}\|_1
$$

其中 $\mathcal{W}$ 是关键帧窗口，$G$ 是所有 Gaussian 参数，$T_k$ 是第 $k$ 帧的位姿。梯度同时对 $G$ 和 $T_k$ 传播，实现 pose 和 map 的联合精修。

这种联合优化是 3DGS-SLAM 与传统特征点法 SLAM 的核心差异：传统 BA 优化 3D 点位置，而 3DGS-SLAM 优化 Gaussian 的完整参数集（位置、协方差、颜色、不透明度），优化变量更多但也更具表达力。

### 11.4.6 系统级对比

| 维度 | SplaTAM | MonoGS | FlashSLAM |
|------|---------|--------|-----------|
| 输入 | RGB-D | 单目/RGB-D/Stereo | RGB-D |
| 高斯类型 | 各向同性 | 各向异性 | 各向异性 |
| Tracking 方法 | 梯度下降渲染 | 梯度下降 + 解析 Jacobian | 特征匹配 + Kabsch |
| Mapping 方法 | 可微 splatting | 可微 splatting | 可微 splatting |
| Densification | 深度反投影 + Silhouette | 深度估计 + 梯度区域 | 深度反投影 + 误差驱动 |
| 关键机制 | Silhouette mask | 解析 Jacobian + 各向同性正则 | 深度噪声建模 |
| Replica ATE | ~0.3–0.6 cm | ~1–2 cm | ~0.55 cm |
| Tracking 速度 | ~2.7 s/帧 | ~0.33 s/帧 | ~0.08 s/帧 |
| 渲染速度 | ~400 FPS | ~3 FPS 实时 | 未报告 |
| 回环检测 | 无 | 无 | 无 |

**分析：** 三个系统覆盖了从 RGB-D 到单目、从纯梯度下降到特征辅助的不同设计空间。SplaTAM 在 RGB-D 条件下 tracking 和 mapping 精度最高，但速度最慢。MonoGS 突破了单目限制，但速度仅为 3 FPS。FlashSLAM 速度最快，但跟踪精度受限于特征匹配质量。三者都没有回环检测，这是第一代系统的最大共同短板。

### 11.4.7 第一代系统的共同局限

三个系统共享若干根本性局限：

**没有回环检测。** 长序列运行时，tracking drift 会累积。这是第一代 3DGS-SLAM 的最大短板，后续工作通过引入子图管理和回环闭合解决。

**高斯管理依赖启发式阈值。** Densification 和 pruning 的阈值通常手动设定，对不同场景的适应性差。自适应阈值和基于学习的策略是后续研究方向。

**跟踪与建图速度不匹配。** Mapping 通常比 tracking 慢一个数量级。在 SplaTAM 中，mapping 每帧约 4.9 s，tracking 约 2.7 s，均远非实时。MonoGS 的 3 FPS 和 FlashSLAM 的跟踪提速缓解了这一问题，但 mapping 速度仍是瓶颈。

**缺乏全局一致性约束。** 滑动窗口 optimization 只保证局部一致性，无法纠正早期的 pose drift。全局 BA 或 pose graph optimization 的缺失限制了可重建的场景规模。

---

## 11.5 与具身智能的关系

3DGS-SLAM 的第一代系统为具身智能提供了前所未有的地图表示。传统 SLAM 输出点云或网格，机器人很难直接利用。3DGS 地图可以实时渲染出新视角的图像和深度，这为机器人规划提供了两个独特能力：

1. **视觉想象（Visual Imagining）**：机器人可以在地图上"假想"一个视角，渲染出该视角的 RGB-D 图像，用于路径规划或目标检测的模拟。
2. **可微交互（Differentiable Interaction）**：由于地图参数可微，机器人可以把下游任务的目标（如"看到某个物体"）反向传播为对相机路径或地图的梯度，实现端到端的主动感知。

但第一代系统的速度限制了这种潜力。3 FPS（MonoGS）或 2.7 s/帧（SplaTAM tracking）无法满足机器人实时控制的需求。FlashSLAM 的提速方向是正确的，但 mapping 仍不够快。第 12 章将讨论 2025 年的工程化进展，这些进展使 3DGS-SLAM 的速度和鲁棒性接近实际部署的要求。

---

**本章一句话总结：** SplaTAM、MonoGS 和 FlashSLAM 共同证明 3D Gaussian Splatting 可以作为 SLAM 的统一场景表示，但它们的速度瓶颈和缺失的回环检测也明确指出了下一代系统需要攻克的工程方向。

---
