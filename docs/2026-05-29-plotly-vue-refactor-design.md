# Plotly.js Vue 组件化重构设计

## 背景

当前 Vue 实现使用 Three.js + D3，与原型的 Plotly.js 实现完全脱节。
目标：以 `index-plotly-legacy.html` 为参考，用 Plotly.js 重写 Vue 组件。

## 架构

```
src/observable/src/
├── App.vue                        # 布局、数据加载、动画状态
├── main.ts                        # 入口
├── components/
│   ├── ClimateChart.vue           # 单个 Plotly figure（3 subplot）
│   └── ControlBar.vue             # 播放/暂停、年份滑块、统计
├── composables/
│   ├── useScatter3D.ts            # 3D scatter trace 数据
│   ├── useHeatmap.ts              # heatmap trace 数据
│   └── useTimeSeries.ts           # time series trace 数据
├── data/
│   ├── climate-data.ts            # 静态配置
│   └── loader.ts                  # 加载 combined.json
└── types.ts                       # 类型定义
```

## 数据流

1. App.vue 加载 `combined.json`，持有 `currentYear`、`isPlaying` 状态
2. ClimateChart 接收 data + currentYear，用 composables 组装 Plotly traces
3. 动画用 Plotly 原生 `addFrames` + `animate` 机制
4. ControlBar 通过 emit 控制播放/暂停/年份跳转

## Plotly subplot 布局

- 3D scatter (scene): domain x=[0, 0.62], 全高
- Heatmap (xaxis/yaxis): domain x=[0.62, 1.0], y=[0.32, 1.0]
- Time series (xaxis2/yaxis2): domain x=[0, 1.0], y=[0, 0.32]

## 主题

- paper_bgcolor: #0f1419
- font color: #f2f5fa
- RdBu diverging colorscale
- 中文纬度标签

## 数据

复用已有的 `public/data/combined.json`，不再内联数据。

## 依赖变更

- 安装: plotly.js-dist
- 移除: echarts, echarts-gl (刚装的), three, d3 (已移除)
