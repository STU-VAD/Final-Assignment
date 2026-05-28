# 3D 转 2D 投影模式 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 3D 散点图添加 4 种视图模式（3D + 3 个正交投影面），用户通过按钮组切换，相机动画平滑过渡，并修正散点始终全量显示。

**Architecture:** 在现有 Vue 组件架构上扩展 — App.vue 新增 `viewMode` 状态，ControlBar 新增按钮组，ClimateChart 通过 watch 触发 Plotly 相机动画（两步走：先移相机再切正交）。useScatter3D 提供相机预设参数。

**Tech Stack:** Vue 3 Composition API, Plotly.js, TypeScript

---

## 文件结构

| 文件 | 操作 | 职责 |
|------|------|------|
| `src/observable/src/types.ts` | 修改 | 新增 `ViewMode` 类型、`CameraPreset` 接口 |
| `src/observable/src/composables/useScatter3D.ts` | 修改 | 修正散点过滤；导出 `CAMERA_PRESETS` |
| `src/observable/src/App.vue` | 修改 | 新增 `viewMode` ref，传递给子组件 |
| `src/observable/src/components/ControlBar.vue` | 修改 | 新增模式按钮组 UI |
| `src/observable/src/components/ClimateChart.vue` | 修改 | watch `viewMode`，执行相机动画 |

---

### Task 1: 新增类型定义和相机预设

**Files:**
- Modify: `src/observable/src/types.ts`
- Modify: `src/observable/src/composables/useScatter3D.ts`

- [ ] **Step 1: 在 types.ts 中添加 ViewMode 和 CameraPreset**

在 `src/observable/src/types.ts` 末尾追加：

```typescript
export type ViewMode = '3d' | 'faceA' | 'faceB' | 'faceC'

export interface CameraPreset {
  eye: { x: number; y: number; z: number }
  center: { x: number; y: number; z: number }
  up: { x: number; y: number; z: number }
}
```

- [ ] **Step 2: 在 useScatter3D.ts 中导出 CAMERA_PRESETS**

在 `src/observable/src/composables/useScatter3D.ts` 中：

1. 在文件顶部 import 区域添加：

```typescript
import type { CameraPreset, ViewMode } from '../types'
```

2. 在 `export function useScatter3D()` 之前添加：

```typescript
export const CAMERA_PRESETS: Record<ViewMode, CameraPreset> = {
  '3d':    { eye: { x: 1.5, y: -1.5, z: 0.8 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceA': { eye: { x: 0, y: -2.5, z: 0 },     center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceB': { eye: { x: 2.5, y: 0, z: 0 },      center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceC': { eye: { x: 0, y: -0.01, z: 2.5 },  center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 1, z: 0 } },
}
```

3. 更新 return 语句，添加 `CAMERA_PRESETS`：

```typescript
return { buildCurrentYearTrace, buildHistoryTrail, buildSceneLayout, CAMERA_PRESETS }
```

- [ ] **Step 3: 验证构建**

Run: `cd src/observable && npx vue-tsc --noEmit`
Expected: 无类型错误

- [ ] **Step 4: 提交**

```bash
git add src/observable/src/types.ts src/observable/src/composables/useScatter3D.ts
git commit -m "feat: 添加 ViewMode 类型和相机预设参数"
```

---

### Task 2: 修正散点全量显示

**Files:**
- Modify: `src/observable/src/composables/useScatter3D.ts`

- [ ] **Step 1: 移除 buildHistoryTrail 的年份过滤**

在 `src/observable/src/composables/useScatter3D.ts` 的 `buildHistoryTrail` 函数中，删除 `if (item.year >= currentYear) continue` 这一行。

将：

```typescript
for (const item of data.data) {
  if (item.year >= currentYear) continue
  for (const band of BAND_8) {
```

改为：

```typescript
for (const item of data.data) {
  for (const band of BAND_8) {
```

- [ ] **Step 2: 启动 dev server 验证散点全量显示**

Run: `cd src/observable && npx vite --open`
Expected: 拖动时间轴时，所有 47 年的散点始终可见，当前年份高亮

- [ ] **Step 3: 提交**

```bash
git add src/observable/src/composables/useScatter3D.ts
git commit -m "fix: 散点图始终显示全部年份数据"
```

---

### Task 3: App.vue 新增 viewMode 状态

**Files:**
- Modify: `src/observable/src/App.vue`

- [ ] **Step 1: 添加 viewMode 状态和传递**

在 `src/observable/src/App.vue` 中：

1. 在 import 区域添加 `ViewMode` 类型导入：

```typescript
import type { CombinedData, TemperatureData, ViewMode } from './types'
```

2. 在 `const isPlaying = ref(false)` 后添加：

```typescript
const viewMode = ref<ViewMode>('3d')
```

3. 在 template 的 `<ClimateChart>` 上添加 `:viewMode` prop：

```html
<ClimateChart
  v-if="combinedData && tempData"
  :combinedData="combinedData"
  :tempData="tempData"
  :currentYear="currentYear"
  :isPlaying="isPlaying"
  :viewMode="viewMode"
/>
```

4. 在 template 的 `<ControlBar>` 上添加 `:viewMode` prop 和 `@update:viewMode` 事件：

```html
<ControlBar
  :currentYear="currentYear"
  :minYear="1979"
  :maxYear="2025"
  :isPlaying="isPlaying"
  :stats="stats"
  :viewMode="viewMode"
  @toggle-play="togglePlay"
  @update:year="setYear"
  @update:viewMode="viewMode = $event"
/>
```

- [ ] **Step 2: 验证构建**

Run: `cd src/observable && npx vue-tsc --noEmit`
Expected: 类型错误（因为子组件还没接收新 prop），这是预期的，Task 4 和 5 会修复

- [ ] **Step 3: 提交**

```bash
git add src/observable/src/App.vue
git commit -m "feat: App.vue 添加 viewMode 状态管理"
```

---

### Task 4: ControlBar 新增模式按钮组

**Files:**
- Modify: `src/observable/src/components/ControlBar.vue`

- [ ] **Step 1: 更新 props 和 emits**

在 `src/observable/src/components/ControlBar.vue` 的 `<script setup>` 中：

1. 在 import 区域添加：

```typescript
import type { ViewMode } from '../types'
```

2. 更新 `defineProps` 添加 `viewMode`：

```typescript
defineProps<{
  currentYear: number
  minYear: number
  maxYear: number
  isPlaying: boolean
  stats: { co2: string; arcticTemp: string } | null
  viewMode: ViewMode
}>()
```

3. 更新 `defineEmits` 添加 `update:viewMode`：

```typescript
defineEmits<{
  'toggle-play': []
  'update:year': [year: number]
  'update:viewMode': [mode: ViewMode]
}>()
```

- [ ] **Step 2: 添加模式按钮组模板**

在 `<template>` 的 `<button class="play-btn">` 之后、`<div class="year-display">` 之前插入：

```html
<div class="mode-btns">
  <button
    v-for="m in modes"
    :key="m.id"
    class="mode-btn"
    :class="{ active: viewMode === m.id }"
    @click="$emit('update:viewMode', m.id)"
    :title="m.tip"
  >{{ m.label }}</button>
</div>
```

在 `<script setup>` 的 `defineEmits` 之后添加 modes 定义：

```typescript
const modes: { id: ViewMode; label: string; tip: string }[] = [
  { id: '3d',    label: '3D',      tip: '三维全景' },
  { id: 'faceA', label: 'CO₂×T',   tip: 'CO₂ × 温度异常' },
  { id: 'faceB', label: 'Lat×T',   tip: '纬度 × 温度异常' },
  { id: 'faceC', label: 'CO₂×Lat', tip: 'CO₂ × 纬度' },
]
```

- [ ] **Step 3: 添加按钮样式**

在 `<style scoped>` 末尾追加：

```css
.mode-btns {
  display: flex;
  gap: 4px;
}
.mode-btn {
  padding: 4px 8px;
  background: transparent;
  color: #6b7a94;
  border: 1px solid #1a2540;
  border-radius: 3px;
  cursor: pointer;
  font-family: inherit;
  font-size: 10px;
  transition: all 0.2s;
  white-space: nowrap;
}
.mode-btn:hover {
  border-color: #e94560;
  color: #e94560;
}
.mode-btn.active {
  background: #e94560;
  border-color: #e94560;
  color: #fff;
}
```

- [ ] **Step 4: 验证构建**

Run: `cd src/observable && npx vue-tsc --noEmit`
Expected: ControlBar 无类型错误（ClimateChart 可能仍有错误，Task 5 修复）

- [ ] **Step 5: 提交**

```bash
git add src/observable/src/components/ControlBar.vue
git commit -m "feat: 控制栏添加视图模式按钮组"
```

---

### Task 5: ClimateChart 相机动画

**Files:**
- Modify: `src/observable/src/components/ClimateChart.vue`

- [ ] **Step 1: 更新 props**

在 `src/observable/src/components/ClimateChart.vue` 的 props 中添加 `viewMode`：

```typescript
import type { CombinedData, TemperatureData, ViewMode } from '../types'

const props = defineProps<{
  combinedData: CombinedData | null
  tempData: TemperatureData | null
  currentYear: number
  isPlaying: boolean
  viewMode: ViewMode
}>()
```

- [ ] **Step 2: 导入 CAMERA_PRESETS**

在 useScatter3D 解构中添加 `CAMERA_PRESETS`：

```typescript
const { buildCurrentYearTrace, buildHistoryTrail, buildSceneLayout, CAMERA_PRESETS } = useScatter3D()
```

- [ ] **Step 3: 添加相机切换函数**

在 `updateChart()` 函数之后添加：

```typescript
let modeTransitionTimer: number | null = null

function switchCamera(mode: ViewMode) {
  if (!chartRef.value || !initialized) return

  const preset = CAMERA_PRESETS[mode]
  const isFaceMode = mode !== '3d'

  if (modeTransitionTimer) {
    clearTimeout(modeTransitionTimer)
    modeTransitionTimer = null
  }

  if (isFaceMode) {
    // Step 1: 在透视模式下移到目标位置
    Plotly.relayout(chartRef.value, {
      'scene.camera': {
        eye: preset.eye,
        center: preset.center,
        up: preset.up,
        projection: { type: 'perspective' },
      },
    })
    // Step 2: 动画结束后切换正交投影
    modeTransitionTimer = window.setTimeout(() => {
      if (!chartRef.value) return
      Plotly.relayout(chartRef.value, {
        'scene.camera.projection.type': 'orthographic',
      })
    }, 450)
  } else {
    // 回到 3D：先切回透视，再移相机
    Plotly.relayout(chartRef.value, {
      'scene.camera.projection.type': 'perspective',
    })
    modeTransitionTimer = window.setTimeout(() => {
      if (!chartRef.value) return
      Plotly.relayout(chartRef.value, {
        'scene.camera': {
          eye: preset.eye,
          center: preset.center,
          up: preset.up,
        },
      })
    }, 50)
  }
}
```

- [ ] **Step 4: 添加 watch viewMode**

在已有的 `watch(() => props.isPlaying, ...)` 之后添加：

```typescript
watch(() => props.viewMode, (newMode, oldMode) => {
  if (newMode === oldMode) return
  switchCamera(newMode)
})
```

- [ ] **Step 5: 清理 timer**

在 `onBeforeUnmount` 中添加 timer 清理：

```typescript
onBeforeUnmount(() => {
  if (chartRef.value && initialized) {
    Plotly.purge(chartRef.value)
  }
  if (modeTransitionTimer) clearTimeout(modeTransitionTimer)
})
```

- [ ] **Step 6: 验证构建和效果**

Run: `cd src/observable && npx vite --open`
Expected:
1. 控制栏出现 4 个模式按钮，默认 3D 高亮
2. 点击 CO₂×T → 相机平滑旋转到正面 + 正交
3. 点击 3D → 相机回到斜视角
4. 其他面类似

- [ ] **Step 7: 提交**

```bash
git add src/observable/src/components/ClimateChart.vue
git commit -m "feat: 3D 散点图支持视图模式切换和相机动画"
```
