# 从 Python/Plotly 迁移到 D3.js/npm 设计文档

## 概述

将现有 Python/Plotly.js 可视化实现迁移到 Vue 3 + D3.js + Three.js 技术栈，使用 Vite 构建，TypeScript 开发，GitHub Actions 自动部署。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | latest | 前端框架 |
| TypeScript | latest | 类型安全 |
| Vite | latest | 构建工具 |
| D3.js | v7 | 2D 图表（热图、CO₂ 时序图） |
| Three.js | latest | 3D 散点图 |
| Vitest | latest | 测试框架 |
| uv | latest | Python 依赖管理 |
| GitHub Actions | - | 自动部署 |

## 项目结构

```
src/
├── observable/                 # Vue 应用主目录
│   ├── components/            # Vue 组件
│   │   ├── Scatter3D.vue     # 3D 散点图（Three.js）
│   │   ├── Heatmap.vue       # 热图（D3.js）
│   │   ├── CO2Chart.vue      # CO₂ 时序图（D3.js）
│   │   ├── TimeSlider.vue    # 时间滑块
│   │   └── Controls.vue      # 控制面板
│   ├── data/                 # 数据处理
│   │   ├── types.ts          # TypeScript 类型
│   │   ├── loader.ts         # 数据加载
│   │   └── processor.ts      # 数据处理
│   ├── utils/                # 工具函数
│   ├── App.vue               # 主应用
│   ├── main.ts               # 入口文件
│   ├── package.json          # 项目配置
│   ├── vite.config.ts        # Vite 配置
│   └── tsconfig.json         # TypeScript 配置
├── preprocess/               # Python 数据预处理脚本
│   ├── build_figure.py
│   ├── build.py
│   ├── lat_bands.py
│   └── load_data.py
└── analyse/                  # 保留现有分析页面
```

## 数据流

```
data/*.csv → preprocess/ (Python) → observable/public/data/*.json → observable/src/data/loader.ts → Vue 组件
```

## 组件设计

### Scatter3D.vue - 3D 散点图
- 使用 Three.js 实现 WebGL 3D 渲染
- 复刻现有 Plotly.js 3D 散点图效果
- 显示 CO₂（X）、纬度（Y）、温度异常（Z）
- 颜色编码：RdBu_r 发散调色板
- 时间动画：1979-2025
- 悬停提示：年份、纬度带、CO₂、温度异常

### Heatmap.vue - 温度热图
- 使用 D3.js 实现
- 复刻现有热图效果
- X 轴：年份（1880-2025）
- Y 轴：纬度带（8 行）
- 颜色：温度异常（RdBu_r）
- 黄色竖线指示当前年份

### CO2Chart.vue - CO₂ 时序图
- 使用 D3.js 实现
- 复刻现有时序图效果
- X 轴：年份（1979-2025）
- Y 轴：CO₂ 浓度（ppm）
- 阴影带：不确定度
- 黄色游标指示当前年份

### TimeSlider.vue - 时间滑块
- 复刻现有滑块效果
- 范围：1979-2025
- 支持拖动、点击跳转

### Controls.vue - 控制面板
- 复刻现有控制面板
- 播放/暂停按钮
- 速度选择（0.5×/1×/2×/4×）
- 粒度切换（8 细带/3 粗带/半球）
- 重置按钮

## 交互设计

1. **时间滑块交互**
   - 拖动滑块 → 更新所有图表
   - 点击滑块轨道 → 跳转到目标年份
   - 键盘左右箭头 → 微调年份

2. **播放控制**
   - 点击播放按钮 → 自动滚动 1979→2025
   - 点击暂停按钮 → 停止动画
   - 速度选择 → 0.5×/1×/2×/4×
   - 动画速度：约 200ms/帧

3. **3D 视图交互**
   - 鼠标拖拽 → 旋转视角
   - 滚轮 → 缩放
   - 双击空白处 → 恢复初始视角
   - 悬停点 → 显示提示信息

4. **图例交互**
   - 单击图例 → 隐藏/显示该纬度
   - 双击图例 → 隔离单一纬度

5. **粒度切换**
   - 下拉选择 → 8 细带/3 粗带/半球
   - 切换后重新渲染图表

6. **重置按钮**
   - 点击 → 视角、滑块、过滤全部回到初始状态

## 数据格式

### CO₂ 数据 (co2.json)
```json
{
  "years": [1979, 1980, ...],
  "mean": [336.85, 338.91, ...],
  "unc": [0.10, 0.07, ...]
}
```

### 温度数据 (temperature.json)
```json
{
  "years": [1880, 1881, ...],
  "latitudeBands": ["90S-64S", "64S-44S", ...],
  "anomalies": [[-0.21, 0.33, ...], ...]
}
```

### 合并数据 (combined.json)
```json
{
  "years": [1979, 1980, ...],
  "data": [
    {
      "year": 1979,
      "co2": 336.85,
      "co2Unc": 0.10,
      "temperatures": {
        "90S-64S": -0.21,
        "64S-44S": 0.33,
        ...
      }
    },
    ...
  ]
}
```

## 部署

### GitHub Actions 工作流

**文件：** `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Setup uv
        uses: astral-sh/setup-uv@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: src/observable/package-lock.json

      - name: Install Python dependencies
        run: |
          cd src/preprocess
          uv sync

      - name: Run Python preprocessing
        run: |
          cd src/preprocess
          uv run python build.py

      - name: Install Node.js dependencies
        run: |
          cd src/observable
          npm ci

      - name: Build Vue app
        run: |
          cd src/observable
          npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./src/observable/dist
```

### 构建命令

```bash
# Python 预处理
cd src/preprocess
uv sync
uv run python build.py

# Vue 应用构建
cd src/observable
npm ci
npm run build
```

## 开发命令

```bash
# 启动开发服务器
cd src/observable
npm run dev

# 运行测试
npm run test

# 代码检查
npm run lint

# 类型检查
npm run build
```
