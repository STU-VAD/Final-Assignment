## 全球气候演变 3D 交互可视化：CO₂ 浓度、纬度与温度异常的关系探究（1880–2025）

###### 公开访问 URL
[TODO]

###### 小组成员与贡献

| 姓名 | 学号 | 贡献 |
|------|------|------|
| [TODO] | [TODO] | [TODO] |
| [TODO] | [TODO] | [TODO] |

---

### 1. 动机与目标

"全球变暖"这一结论已被广泛认知，但其中几个关键事实在传统二维图表中难以充分表达：

1. **极地放大效应**：北极升温速度是赤道地区的 3–4 倍，需要同时展示纬度和温度维度
2. **CO₂-温度耦合的纬度差异**：不同纬度带对 CO₂ 的响应强度不同，需多维度对比
3. **时间演化特征**：升温转折点和极端异常年需要动态对比才能识别

这些结论涉及 CO₂、纬度、温度三个维度的耦合关系，二维折线图或热力图只能展示其中两个维度的关系，无法呈现完整的三维结构。因此本项目的目标是构建三维交互可视化，将三个变量映射到空间位置，辅以时间动画，让用户通过旋转视角和切换年份自主探索这些模式。具体围绕三个问题展开：

- **Q1**：不同纬度带的升温速度差异有多大？
- **Q2**：CO₂ 与各纬度带温度变化有怎样的相关结构？
- **Q3**：极端异常年份在空间上有何特征？

目标用户包括三类：

- **气候科学/可视化课程学生**：需要将抽象概念落地为可探索的数据
- **对气候变化感兴趣的公众**：希望通过交互式证据自主验证结论
- **科普教师**：需要直观的演示工具

界面以中文为主，交互设计力求直觉化，无需专业背景即可使用。

---

### 2. 数据

数据来自两个公开数据集：CO₂ 年均浓度来自 NOAA GML（1979–2025，47 条记录），温度异常来自 NASA GISTEMP v4（1880–2025，146 条记录，按 8 个纬度带分别记录，基准期 1951–1980）。

按 Munzner 框架抽象，核心属性的类型如下：年份为 ordinal（sequential），CO₂ 浓度为 quantitative（ratio），温度异常为 quantitative（**diverging**——有正有负），纬度带为 categorical（ordered——从南极到北极有天然空间顺序）。其中温度异常的 diverging 类型直接决定了后续选择发散色板而非彩虹色板。

两个数据集以 year 为主键做左连接，CO₂ 在 1979 年前为空值。温度的 8 个纬度列 melt 为长表格式（146 年 × 8 带 = 1168 行），每行代表某年某纬度带的一次温度观测记录，即 3D 散点图的基本数据项。

---

### 3. 分析任务

在确定可视化方案之前，先明确需要支持用户完成哪些分析任务。按 Munzner 框架的 Why 层定义了 6 个任务：

- **T1 Discover**：探索 CO₂-温度-纬度的三维分布与演变趋势
- **T2 Compare**：比较不同纬度带的 CO₂-温度相关性差异
- **T3 Identify**：识别极端温度异常年份和异常纬度带
- **T4 Browse**：浏览任意年份的温度空间分布模式
- **T5 Locate**：定位升温超过阈值的时间点
- **T6 Summarize**：分析十年际升温加速度和纬度梯度

其中 T1–T3 为核心任务，直接对应三个研究问题；T4 支持探索式假设生成；T5–T6 支持结论验证。这个优先级直接影响视觉通道分配：三个核心变量必须占据精度最高的空间位置通道，纬度带等分类属性则用颜色通道区分。

---

### 4. 视觉编码与交互

#### 4.1 标记与通道

编码面临的核心问题是四个属性（CO₂、纬度、温度、年份）要同时展示，但有效通道有限。按 Munzner 的通道有效性排序，空间位置 > 颜色 > 尺寸 > 形状。因此 CO₂、纬度、温度三个定量变量被分配到 X/Y/Z 空间位置，温度额外冗余编码到颜色通道——3D 视图不可避免会产生遮挡，颜色可以补偿被遮挡的深度信息。年份通过动画帧序列表达，而非强行映射到空间维度。

| 视觉 idiom | Mark | 数据属性→通道映射 | 分析任务 |
|------------|------|-----------------|---------|
| 3D 散点图 | Point | CO₂→X, 纬度→Y, 温度→Z, 温度→颜色(冗余) | T1 发现分布 |
| 温度热力图 | Area | 年份→X, 纬度→Y, 温度→颜色 | T3 识别异常, T4 浏览 |
| CO₂ 时序图 | Line | 年份→X, CO₂→Y, 不确定度→阴影带 | T5 定位阈值 |
| 散点+回归 | Point+Line | CO₂→X, 温度→Y, 纬度→颜色, 斜率→文字 | T2 比较相关性 |
| 柱状图 | Line (bar) | 纬度/十年→X, 统计值→Y, 纬度→颜色 | T6 汇总趋势 |

#### 4.2 页面一：3D 气候仪表板（Plotly）

![3D 气候仪表板截图占位符](screenshots/index-placeholder.png)

主可视化采用 item-set 联动多视图布局，三个面板通过年份滑块同步。核心是 3D 散点图——每个 point 代表某年某纬度带的一次观测，47 帧逐年推进。当前帧为高亮不透明 point，过去 5 帧保留为半透明 point，形成运动轨迹。这种 temporal encoding 使用户能感知数据点随时间的位移方向和速度：北极点快速向高温区移动，直观传达极地放大效应。

热力图作为 overview 视图提供 146 年全局模式，3D 散点作为 detail 视图呈现具体年份的三维结构，二者互补，遵循 Shneiderman 的 overview-first 原则。底部 CO₂ 时序线提供时间维度上的上下文。

#### 4.3 页面二：3D 极地放大观测台（ECharts）

![3D 极地放大观测台截图占位符](screenshots/prototype-placeholder.png)

与 Plotly 版的关键编码差异：point 的颜色通道不再编码温度，改为编码纬度带分类属性。这牺牲了温度的冗余编码，但换来了轨迹追踪能力——用户可在 3D 空间中按颜色追踪同一纬度带的历史路径。三种显示模式（单年/轨迹/全景）本质上是改变数据项的 selection 范围：单年仅显示 8 个 point，轨迹模式显示指定纬度带全部 point，全景模式显示全部 1168 个 point。

#### 4.4 页面三：交叉分析（ECharts）

叙事式布局，文字与图表交替排列。四个核心图表：

1. **双时间序列**：CO₂ 折线 + 8 纬度带温度折线，展示各带的升温差异
2. **散点+回归**：CO₂ vs 温度，每纬度带一组，量化敏感性（北极 ~0.036°C/ppm，赤道 ~0.008°C/ppm）
3. **敏感性柱状图**：回归斜率的直接对比
4. **十年际柱状图**：5 个十年各纬度带平均温度异常，展示升温加速度

#### 4.5 交互设计

| 交互类型 | Munzner 分类 | 解决什么问题 |
|---------|-------------|------------|
| 年份滑块 | Navigate (sequence) | 控制时间帧，三面板同步 |
| 播放/暂停 | Navigate (sequence) | 自动演变动画，支持 T1 |
| 3D 旋转/缩放 | Navigate (viewpoint) | 解决 3D 遮挡，切换视角 |
| 悬停提示 | Select (hover) | 精确读取 item 属性值 |
| 图例过滤 | Filter | 按纬度带逐个对比 |
| 热力图点击 | Select→Navigate | 从 overview 跳到 detail |
| 键盘控制 | Navigate (sequence) | 精细时间浏览 |

设计逻辑：Navigate 类交互（滑块、播放、旋转）服务探索式浏览（T1/T4），Select 类（悬停、点击）服务精确识别（T3），Filter 类（图例）服务分组对比（T2）。

---

### 5. 设计理念

设计理念的要点如下：

- **发散色板**：选择 RdBu_r 而非彩虹色，因为彩虹色不符合感知线性度，容易产生虚假边界感知（Borland & Taylor, 2007）。温度异常为 diverging 数据（正=偏暖，负=偏冷），红蓝发散色对应语义，且对红绿色盲友好。
- **动画与静态互补**：动画在展示连续变化时更有效，但精确比较不如静态图（Tversky et al., 2002）。因此 3D 动画展示时间演变，静态热力图提供精确对比基线。
- **多视图联动**：热力图提供 overview，3D 散点提供 detail，CO₂ 时序提供 context，三面板通过滑块同步时间上下文（Heer et al., 2010; Shneiderman, 1996）。用户无需在不同图表间手动对齐时间状态。

---

### 6. 分析发现

**极地放大效应确认**： 北极 (64N-90N) 温度异常从 1880 年代约 -1.1°C 飙升到 2020 年代约 +2.6°C，2025 年达 **+3.01°C**，全球平均仅升至 **+1.19°C**。升温幅度远超赤道地区，且仍在加速。

**CO₂ 敏感性存在显著纬度梯度**： 回归分析显示北极和北半球中纬带与 CO₂ 强相关（64N-90N R²=0.83，24N-44N R²=0.90），但中高纬南（64S-44S）线性关系极弱（R²=0.03）。敏感性差异显著：北极每增加 1 ppm CO₂ 升温约 0.036°C，赤道仅约 0.008°C。CO₂ 从 336.85 ppm 升至 425.65 ppm（+89 ppm），按北极敏感性计算对应约 +3.2°C 的升温幅度。这表明 +1.19°C 的全球平均数字严重低估了北极地区的实际升温幅度。

**极端年份呈现空间衰减模式**： 热力图上，2016、2023、2024 等异常年呈现"红色脉冲"从极地向赤道衰减的清晰模式。2016 年北极达 **+3.26°C**（历史最高，强厄尔尼诺叠加），甚至超过 2025 年的 +3.01°C，反映了短期波动叠加在长期趋势上的特征。

**南北半球升温不对称**： 高纬北（44N-64N）2025 年异常 +1.99°C，对应高纬南（64S-44S）仅 +0.56°C。这种不对称可能与北半球更大的陆地面积有关——陆地比热容低于海洋，升温响应更快。

---

### 7. 用户研究

邀请 3 名用户使用可视化系统，要求他们完成三个探索任务：在 3D 散点图中找出北极最热年份、在热力图中对比两个年代温差、在分析页面中判断最敏感纬度带。观察操作过程后进行简短访谈，收集反馈。

**优点**： 所有用户均能顺利完成前两个任务。热力图被评为最直观的视图，无需学习即可理解色标含义。3D 散点图的播放动画获得一致好评，用户表示"能清晰看到北极点的运动轨迹"。多视图联动（滑块同步三面板）减少了手动对齐负担。分析页面中的散点回归+斜率标注使 CO₂ 敏感性差异一目了然。

**不足**： 一名用户未理解发散色板零点含义，建议在色标旁标注基准期。另一名用户不理解"敏感性"术语，建议增加解释。

---

### 8. 局限性

1. CO₂ 数据无纬度分解，同年所有纬度带共享相同 X 坐标，降低了信息密度
2. 3D 散点不可避免存在遮挡问题，虽已通过颜色冗余编码缓解
3. 8 个纬度带空间分辨率有限，无法展示经度差异

---

### 9. 参考文献

1. Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
2. Borland, D., & Taylor II, R. M. (2007). Rainbow Color Map (Still) Considered Harmful. *IEEE Computer Graphics and Applications*, 27(2), 14–17.
3. Heer, J., Bostock, M., & Ogievetsky, V. (2010). A Tour Through the Visualization Zoo. *Communications of the ACM*, 53(6), 59–67.
4. Mackinlay, J. (1986). Automating the Design of Graphical Presentations of Relational Information. *ACM Transactions on Graphics*, 5(2), 110–141.
5. Cleveland, W. S., & McGill, R. (1984). Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods. *Journal of the American Statistical Association*, 79(387), 531–554.
6. Shneiderman, B. (1996). The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations. *Proceedings of the 1996 IEEE Symposium on Visual Languages*, 336–343.
7. Tversky, B., Morrison, J. B., & Bétrancourt, M. (2002). Animation: Can It Facilitate? *International Journal of Human-Computer Studies*, 57(4), 247–262.
8. NOAA Global Monitoring Laboratory. (2025). *Globally averaged marine surface annual mean CO₂ data*. https://gml.noaa.gov/ccgg/trends/gl_data.html
9. NASA Goddard Institute for Space Studies. (2025). *GISS Surface Temperature Analysis (GISTEMP v4)*. https://data.giss.nasa.gov/gistemp/
