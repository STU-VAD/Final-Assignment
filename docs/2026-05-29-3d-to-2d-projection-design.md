# 3D 转 2D 投影模式设计

## 概述

为 3D 散点图添加 4 种视图模式，用户可通过按钮组自由切换。3D 全景 + 3 个正交投影面，通过相机动画平滑过渡，并修正散点始终全量显示的问题。

## 视图模式

| 模式 | 投影 | 相机 eye | up | 说明 |
|------|------|----------|-----|------|
| 3D 默认 | perspective | `{1.5, -1.5, 0.8}` | `{0,0,1}` | 当前斜视角 |
| 面 A | orthographic | `{0, -2.5, 0}` | `{0,0,1}` | CO₂ × 温度异常 |
| 面 B | orthographic | `{2.5, 0, 0}` | `{0,0,1}` | 纬度 × 温度异常 |
| 面 C | orthographic | `{0, -0.01, 2.5}` | `{0,1,0}` | CO₂ × 纬度 |

面 C 俯视时 up 改为 `{0,1,0}`，避免视线与 up 平行导致万向锁。

## 交互设计

### 触发方式

在 ControlBar 播放按钮和年份之间添加按钮组：

```
[▶ 播放]  [3D] [CO₂×T] [Lat×T] [CO₂×Lat]  2025  ━━━━滑块━━━━  统计数据
```

当前激活按钮 `#e94560` 填充，其余透明底 + `#e94560` 边框。

### 布局

右侧热力图和底部 CO₂ 时序图不受影响，布局不变。

## 状态与数据流

### 新增状态

```typescript
type ViewMode = '3d' | 'faceA' | 'faceB' | 'faceC'
const viewMode = ref<ViewMode>('3d')
```

`viewMode` 归属 `App.vue`，通过 prop 传给 `ClimateChart.vue`。

### 数据流

```
ControlBar 按钮点击
    ↓ $emit('update:viewMode', mode)
App.vue (viewMode ref)
    ↓ :viewMode prop
ClimateChart.vue (watch → 相机动画)
```

## 动画实现

### 切换到 2D（两步走）

```
Step 1: Plotly.relayout({
  'scene.camera': { eye, center, up, projection: { type: 'perspective' } }
})
→ Plotly 内置插值，约 400ms

Step 2: setTimeout(400ms) → Plotly.relayout({
  'scene.camera.projection.type': 'orthographic'
})
```

### 回到 3D

```
Step 1: Plotly.relayout({ 'scene.camera.projection.type': 'perspective' })
Step 2: Plotly.relayout({ 'scene.camera': { 默认位置 } })
```

## 散点显示修正

### 当前问题

`buildHistoryTrail` 过滤 `year < currentYear`，导致当前年份之后的数据不可见。

### 修正

去掉 `buildHistoryTrail` 中的年份过滤，始终显示所有 47 年数据。当前年份通过 `buildCurrentYearTrace` 大号高亮叠在底层散点之上。

仅修改 `useScatter3D.ts` 中 `buildHistoryTrail` 的一行过滤条件。

## 涉及文件

| 文件 | 改动 |
|------|------|
| `src/observable/src/App.vue` | 新增 `viewMode` ref，传递给子组件 |
| `src/observable/src/components/ControlBar.vue` | 新增模式按钮组，emit `update:viewMode` |
| `src/observable/src/components/ClimateChart.vue` | watch `viewMode`，执行相机动画 |
| `src/observable/src/composables/useScatter3D.ts` | 修正 `buildHistoryTrail` 过滤条件 |

## 相机参数表

```typescript
const CAMERA_PRESETS: Record<ViewMode, CameraPreset> = {
  '3d':    { eye: {x:1.5, y:-1.5, z:0.8}, center: {x:0,y:0,z:0}, up: {x:0,y:0,z:1} },
  'faceA': { eye: {x:0, y:-2.5, z:0},     center: {x:0,y:0,z:0}, up: {x:0,y:0,z:1} },
  'faceB': { eye: {x:2.5, y:0, z:0},      center: {x:0,y:0,z:0}, up: {x:0,y:0,z:1} },
  'faceC': { eye: {x:0, y:-0.01, z:2.5},  center: {x:0,y:0,z:0}, up: {x:0,y:1,z:0} },
}
```

## 边界情况

- 播放动画进行中切换模式：相机动画独立于帧动画，互不影响
- 2D 模式下拖动时间轴：帧动画照常工作
- 重复点击当前模式：不做任何操作
