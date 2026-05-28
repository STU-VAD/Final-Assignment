# D3.js/npm 迁移实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 Python/Plotly.js 可视化实现迁移到 Vue 3 + D3.js + Three.js 技术栈

**Architecture:** 使用 Vue 3 构建 UI 框架，D3.js 实现 2D 图表，Three.js 实现 3D 散点图，Vite 构建，TypeScript 开发

**Tech Stack:** Vue 3, TypeScript, Vite, D3.js v7, Three.js, Vitest, uv

---

### Task 1: 项目初始化

**Files:**
- Create: `src/observable/package.json`
- Create: `src/observable/vite.config.ts`
- Create: `src/observable/tsconfig.json`
- Create: `src/observable/index.html`
- Create: `src/observable/src/main.ts`
- Create: `src/observable/src/App.vue`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "climate-viz",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "d3": "^7.9.0",
    "three": "^0.160.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.0",
    "vitest": "^1.2.0",
    "@types/d3": "^7.4.0",
    "@types/three": "^0.160.0"
  }
}
```

- [ ] **Step 2: 创建 vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173
  },
  build: {
    outDir: 'dist'
  }
})
```

- [ ] **Step 3: 创建 tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 4: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="/vite.svg">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>气候可视化</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 5: 创建 main.ts**

```typescript
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

- [ ] **Step 6: 创建 App.vue**

```vue
<template>
  <div id="app">
    <h1>气候可视化</h1>
  </div>
</template>

<script setup lang="ts">
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
```

- [ ] **Step 7: 安装依赖并验证**

```bash
cd src/observable
npm install
npm run dev
```

Expected: 开发服务器启动，浏览器打开 http://localhost:5173 显示 "气候可视化"

- [ ] **Step 8: 提交**

```bash
git add src/observable/
git commit -m "feat: 初始化 Vue 3 + Vite + TypeScript 项目"
```

---

### Task 2: 数据预处理脚本迁移

**Files:**
- Create: `src/preprocess/pyproject.toml`
- Modify: `src/preprocess/build.py`
- Modify: `src/preprocess/load_data.py`
- Modify: `src/preprocess/lat_bands.py`
- Modify: `src/preprocess/build_figure.py`

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[project]
name = "climate-viz-preprocess"
version = "1.0.0"
description = "Climate data preprocessing"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.2.0",
    "numpy>=1.26.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 2: 更新 load_data.py 输出 JSON**

```python
import pandas as pd
import json
from pathlib import Path

def load_co2_data(csv_path: str) -> dict:
    """Load CO2 data and return as dictionary."""
    df = pd.read_csv(csv_path, comment='#')
    return {
        'years': df['year'].tolist(),
        'mean': df['mean'].tolist(),
        'unc': df['unc'].tolist()
    }

def load_temperature_data(csv_path: str) -> dict:
    """Load temperature data and return as dictionary."""
    df = pd.read_csv(csv_path)
    lat_bands = [col for col in df.columns if col not in ['Year', 'Glob', 'NHem', 'SHem']]
    return {
        'years': df['Year'].tolist(),
        'latitudeBands': lat_bands,
        'anomalies': df[lat_bands].values.tolist()
    }

def save_json(data: dict, output_path: str):
    """Save data as JSON file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 3: 更新 build.py 输出 JSON**

```python
from load_data import load_co2_data, load_temperature_data, save_json
import json

def main():
    # Load data
    co2_data = load_co2_data('../../data/co2_annmean_gl.csv')
    temp_data = load_temperature_data('../../data/ZonAnn.Ts+dSST.csv')
    
    # Create combined data
    combined_data = {
        'years': co2_data['years'],
        'data': []
    }
    
    for i, year in enumerate(co2_data['years']):
        year_data = {
            'year': year,
            'co2': co2_data['mean'][i],
            'co2Unc': co2_data['unc'][i],
            'temperatures': {}
        }
        
        # Find temperature data for this year
        if year in temp_data['years']:
            year_idx = temp_data['years'].index(year)
            for j, band in enumerate(temp_data['latitudeBands']):
                year_data['temperatures'][band] = temp_data['anomalies'][year_idx][j]
        
        combined_data['data'].append(year_data)
    
    # Save JSON files
    save_json(co2_data, '../observable/public/data/co2.json')
    save_json(temp_data, '../observable/public/data/temperature.json')
    save_json(combined_data, '../observable/public/data/combined.json')
    
    print("Data preprocessing complete!")

if __name__ == '__main__':
    main()
```

- [ ] **Step 4: 运行预处理脚本**

```bash
cd src/preprocess
uv sync
uv run python build.py
```

Expected: 看到 "Data preprocessing complete!" 并在 `src/observable/public/data/` 目录生成 JSON 文件

- [ ] **Step 5: 提交**

```bash
git add src/preprocess/
git commit -m "feat: 更新 Python 预处理脚本输出 JSON"
```

---

### Task 3: TypeScript 数据类型定义

**Files:**
- Create: `src/observable/src/data/types.ts`

- [ ] **Step 1: 创建 types.ts**

```typescript
export interface CO2Data {
  years: number[]
  mean: number[]
  unc: number[]
}

export interface TemperatureData {
  years: number[]
  latitudeBands: string[]
  anomalies: number[][]
}

export interface YearData {
  year: number
  co2: number
  co2Unc: number
  temperatures: Record<string, number>
}

export interface CombinedData {
  years: number[]
  data: YearData[]
}

export interface VisualizationState {
  currentYear: number
  isPlaying: boolean
  playbackSpeed: number
  granularity: 'fine' | 'medium' | 'hemisphere'
  selectedBands: string[]
}
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/data/types.ts
git commit -m "feat: 添加 TypeScript 数据类型定义"
```

---

### Task 4: 数据加载器

**Files:**
- Create: `src/observable/src/data/loader.ts`

- [ ] **Step 1: 创建 loader.ts**

```typescript
import type { CO2Data, TemperatureData, CombinedData } from './types'

export async function loadCO2Data(): Promise<CO2Data> {
  const response = await fetch('/data/co2.json')
  return response.json()
}

export async function loadTemperatureData(): Promise<TemperatureData> {
  const response = await fetch('/data/temperature.json')
  return response.json()
}

export async function loadCombinedData(): Promise<CombinedData> {
  const response = await fetch('/data/combined.json')
  return response.json()
}
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/data/loader.ts
git commit -m "feat: 添加数据加载器"
```

---

### Task 5: 数据处理器

**Files:**
- Create: `src/observable/src/data/processor.ts`

- [ ] **Step 1: 创建 processor.ts**

```typescript
import type { CombinedData, YearData } from './types'

export function filterByYear(data: CombinedData, year: number): YearData | undefined {
  return data.data.find(d => d.year === year)
}

export function filterByYearRange(data: CombinedData, startYear: number, endYear: number): CombinedData {
  return {
    ...data,
    data: data.data.filter(d => d.year >= startYear && d.year <= endYear)
  }
}

export function getTemperatureRange(data: CombinedData): [number, number] {
  let min = Infinity
  let max = -Infinity
  
  for (const yearData of data.data) {
    for (const temp of Object.values(yearData.temperatures)) {
      min = Math.min(min, temp)
      max = Math.max(max, temp)
    }
  }
  
  return [min, max]
}

export function getCO2Range(data: CombinedData): [number, number] {
  const co2Values = data.data.map(d => d.co2)
  return [Math.min(...co2Values), Math.max(...co2Values)]
}
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/data/processor.ts
git commit -m "feat: 添加数据处理器"
```

---

### Task 6: 温度热图组件

**Files:**
- Create: `src/observable/src/components/Heatmap.vue`

- [ ] **Step 1: 创建 Heatmap.vue**

```vue
<template>
  <div ref="chartRef" class="heatmap"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as d3 from 'd3'
import type { CombinedData } from '../data/types'

const props = defineProps<{
  data: CombinedData
  currentYear: number
}>()

const chartRef = ref<HTMLElement>()

const margin = { top: 20, right: 30, bottom: 30, left: 80 }
const width = 800 - margin.left - margin.right
const height = 400 - margin.top - margin.bottom

function drawChart() {
  if (!chartRef.value || !props.data) return

  // Clear previous chart
  d3.select(chartRef.value).selectAll('*').remove()

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Get unique years and latitude bands
  const years = props.data.years
  const bands = Object.keys(props.data.data[0]?.temperatures || {})

  // Create scales
  const x = d3.scaleBand()
    .domain(years.map(String))
    .range([0, width])
    .padding(0.1)

  const y = d3.scaleBand()
    .domain(bands)
    .range([0, height])
    .padding(0.1)

  // Color scale (RdBu_r diverging)
  const colorScale = d3.scaleSequential(d3.interpolateRdBu)
    .domain([-3, 3])

  // Draw heatmap cells
  svg.selectAll('rect')
    .data(props.data.data)
    .enter()
    .append('rect')
    .attr('x', d => x(String(d.year)) || 0)
    .attr('y', d => {
      const band = Object.keys(d.temperatures)[0]
      return y(band) || 0
    })
    .attr('width', x.bandwidth())
    .attr('height', y.bandwidth())
    .attr('fill', d => {
      const temp = Object.values(d.temperatures)[0]
      return colorScale(temp)
    })

  // Add current year indicator
  svg.append('line')
    .attr('x1', x(String(props.currentYear)) || 0)
    .attr('x2', x(String(props.currentYear)) || 0)
    .attr('y1', 0)
    .attr('y2', height)
    .attr('stroke', '#fbbf24')
    .attr('stroke-width', 2)

  // Add axes
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x).tickValues(years.filter((_, i) => i % 10 === 0).map(String)))

  svg.append('g')
    .call(d3.axisLeft(y))
}

onMounted(() => {
  drawChart()
})

watch(() => props.currentYear, () => {
  drawChart()
})
</script>

<style scoped>
.heatmap {
  width: 100%;
  height: 400px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/components/Heatmap.vue
git commit -m "feat: 添加温度热图组件"
```

---

### Task 7: CO₂ 时序图组件

**Files:**
- Create: `src/observable/src/components/CO2Chart.vue`

- [ ] **Step 1: 创建 CO2Chart.vue**

```vue
<template>
  <div ref="chartRef" class="co2-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as d3 from 'd3'
import type { CombinedData } from '../data/types'

const props = defineProps<{
  data: CombinedData
  currentYear: number
}>()

const chartRef = ref<HTMLElement>()

const margin = { top: 20, right: 30, bottom: 30, left: 60 }
const width = 800 - margin.left - margin.right
const height = 300 - margin.top - margin.bottom

function drawChart() {
  if (!chartRef.value || !props.data) return

  // Clear previous chart
  d3.select(chartRef.value).selectAll('*').remove()

  const svg = d3.select(chartRef.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Filter data for CO2 (1979+)
  const co2Data = props.data.data.filter(d => d.year >= 1979)

  // Create scales
  const x = d3.scaleLinear()
    .domain([1979, 2025])
    .range([0, width])

  const y = d3.scaleLinear()
    .domain([330, 430])
    .range([height, 0])

  // Draw uncertainty band
  const area = d3.area<{ year: number; co2: number; co2Unc: number }>()
    .x(d => x(d.year))
    .y0(d => y(d.co2 - d.co2Unc))
    .y1(d => y(d.co2 + d.co2Unc))
    .curve(d3.curveMonotoneX)

  svg.append('path')
    .datum(co2Data)
    .attr('fill', '#66c2ff')
    .attr('fill-opacity', 0.3)
    .attr('d', area)

  // Draw line
  const line = d3.line<{ year: number; co2: number }>()
    .x(d => x(d.year))
    .y(d => y(d.co2))
    .curve(d3.curveMonotoneX)

  svg.append('path')
    .datum(co2Data)
    .attr('fill', 'none')
    .attr('stroke', '#66c2ff')
    .attr('stroke-width', 2)
    .attr('d', line)

  // Add current year indicator
  const currentData = co2Data.find(d => d.year === props.currentYear)
  if (currentData) {
    svg.append('circle')
      .attr('cx', x(currentData.year))
      .attr('cy', y(currentData.co2))
      .attr('r', 5)
      .attr('fill', '#fbbf24')
  }

  // Add axes
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d3.format('d')))

  svg.append('g')
    .call(d3.axisLeft(y))
}

onMounted(() => {
  drawChart()
})

watch(() => props.currentYear, () => {
  drawChart()
})
</script>

<style scoped>
.co2-chart {
  width: 100%;
  height: 300px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/components/CO2Chart.vue
git commit -m "feat: 添加 CO₂ 时序图组件"
```

---

### Task 8: 3D 散点图组件

**Files:**
- Create: `src/observable/src/components/Scatter3D.vue`

- [ ] **Step 1: 创建 Scatter3D.vue**

```vue
<template>
  <div ref="chartRef" class="scatter3d"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import type { CombinedData, YearData } from '../data/types'

const props = defineProps<{
  data: CombinedData
  currentYear: number
}>()

const chartRef = ref<HTMLElement>()
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let points: THREE.Points

function initScene() {
  if (!chartRef.value) return

  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x1a1a1a)

  // Camera
  camera = new THREE.PerspectiveCamera(75, chartRef.value.clientWidth / chartRef.value.clientHeight, 0.1, 1000)
  camera.position.set(50, 50, 50)
  camera.lookAt(0, 0, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(chartRef.value.clientWidth, chartRef.value.clientHeight)
  chartRef.value.appendChild(renderer.domElement)

  // Add axes
  const axesHelper = new THREE.AxesHelper(50)
  scene.add(axesHelper)
}

function updatePoints() {
  if (!props.data) return

  // Remove existing points
  if (points) {
    scene.remove(points)
  }

  // Get current year data
  const yearData = props.data.data.find(d => d.year === props.currentYear)
  if (!yearData) return

  // Create geometry
  const geometry = new THREE.BufferGeometry()
  const positions: number[] = []
  const colors: number[] = []

  const bands = Object.keys(yearData.temperatures)
  bands.forEach((band, i) => {
    const temp = yearData.temperatures[band]
    const co2 = yearData.co2
    const lat = (i - 3.5) * 20 // Map to -70 to 70

    positions.push(co2 / 10, lat, temp * 10)

    // Color based on temperature (RdBu_r)
    const color = new THREE.Color()
    if (temp < 0) {
      color.setHSL(0.6, 1, 0.5 + temp / 6)
    } else {
      color.setHSL(0, 1, 0.5 - temp / 6)
    }
    colors.push(color.r, color.g, color.b)
  })

  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))

  const material = new THREE.PointsMaterial({ size: 5, vertexColors: true })
  points = new THREE.Points(geometry, material)
  scene.add(points)
}

function animate() {
  requestAnimationFrame(animate)
  renderer.render(scene, camera)
}

onMounted(() => {
  initScene()
  updatePoints()
  animate()
})

onBeforeUnmount(() => {
  if (renderer) {
    renderer.dispose()
  }
})

watch(() => props.currentYear, () => {
  updatePoints()
})
</script>

<style scoped>
.scatter3d {
  width: 100%;
  height: 500px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/components/Scatter3D.vue
git commit -m "feat: 添加 3D 散点图组件"
```

---

### Task 9: 时间滑块组件

**Files:**
- Create: `src/observable/src/components/TimeSlider.vue`

- [ ] **Step 1: 创建 TimeSlider.vue**

```vue
<template>
  <div class="time-slider">
    <input
      type="range"
      :min="minYear"
      :max="maxYear"
      :value="modelValue"
      @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))"
      class="slider"
    />
    <div class="year-display">{{ modelValue }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: number
  minYear: number
  maxYear: number
}>()

defineEmits<{
  'update:modelValue': [value: number]
}>()
</script>

<style scoped>
.time-slider {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.slider {
  flex: 1;
  height: 10px;
  -webkit-appearance: none;
  appearance: none;
  background: #444;
  border-radius: 5px;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fbbf24;
  cursor: pointer;
}

.year-display {
  font-size: 18px;
  font-weight: bold;
  color: #fbbf24;
  min-width: 60px;
  text-align: center;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/components/TimeSlider.vue
git commit -m "feat: 添加时间滑块组件"
```

---

### Task 10: 控制面板组件

**Files:**
- Create: `src/observable/src/components/Controls.vue`

- [ ] **Step 1: 创建 Controls.vue**

```vue
<template>
  <div class="controls">
    <button @click="$emit('toggle-play')" class="play-btn">
      {{ isPlaying ? '⏸' : '▶' }}
    </button>
    
    <select :value="playbackSpeed" @change="$emit('update:playbackSpeed', Number(($event.target as HTMLSelectElement).value))">
      <option :value="0.5">0.5×</option>
      <option :value="1">1×</option>
      <option :value="2">2×</option>
      <option :value="4">4×</option>
    </select>
    
    <select :value="granularity" @change="$emit('update:granularity', ($event.target as HTMLSelectElement).value)">
      <option value="fine">8 细带</option>
      <option value="medium">3 粗带</option>
      <option value="hemisphere">半球</option>
    </select>
    
    <button @click="$emit('reset')" class="reset-btn">重置</button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isPlaying: boolean
  playbackSpeed: number
  granularity: string
}>()

defineEmits<{
  'toggle-play': []
  'update:playbackSpeed': [value: number]
  'update:granularity': [value: string]
  'reset': []
}>()
</script>

<style scoped>
.controls {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: #2a2a2a;
  border-radius: 8px;
}

.play-btn, .reset-btn {
  padding: 8px 16px;
  background: #444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.play-btn:hover, .reset-btn:hover {
  background: #555;
}

select {
  padding: 8px;
  background: #444;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/components/Controls.vue
git commit -m "feat: 添加控制面板组件"
```

---

### Task 11: 主应用组件

**Files:**
- Modify: `src/observable/src/App.vue`

- [ ] **Step 1: 更新 App.vue**

```vue
<template>
  <div id="app">
    <h1>全球气候演变三维探索</h1>
    <h2>CO₂、纬度与温度异常的交叉分析 (1880–2025)</h2>
    
    <div class="visualization-container">
      <div class="main-chart">
        <Scatter3D :data="combinedData" :currentYear="currentYear" />
      </div>
      
      <div class="side-charts">
        <Heatmap :data="combinedData" :currentYear="currentYear" />
        <CO2Chart :data="combinedData" :currentYear="currentYear" />
      </div>
    </div>
    
    <TimeSlider
      v-model="currentYear"
      :minYear="1979"
      :maxYear="2025"
    />
    
    <Controls
      :isPlaying="isPlaying"
      :playbackSpeed="playbackSpeed"
      :granularity="granularity"
      @toggle-play="togglePlay"
      @update:playbackSpeed="playbackSpeed = $event"
      @update:granularity="granularity = $event"
      @reset="reset"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Scatter3D from './components/Scatter3D.vue'
import Heatmap from './components/Heatmap.vue'
import CO2Chart from './components/CO2Chart.vue'
import TimeSlider from './components/TimeSlider.vue'
import Controls from './components/Controls.vue'
import { loadCombinedData } from './data/loader'
import type { CombinedData } from './data/types'

const combinedData = ref<CombinedData | null>(null)
const currentYear = ref(1979)
const isPlaying = ref(false)
const playbackSpeed = ref(1)
const granularity = ref('fine')
let animationInterval: number | null = null

onMounted(async () => {
  combinedData.value = await loadCombinedData()
})

function togglePlay() {
  isPlaying.value = !isPlaying.value
  
  if (isPlaying.value) {
    animationInterval = window.setInterval(() => {
      if (currentYear.value < 2025) {
        currentYear.value++
      } else {
        isPlaying.value = false
        if (animationInterval) {
          clearInterval(animationInterval)
        }
      }
    }, 200 / playbackSpeed.value)
  } else {
    if (animationInterval) {
      clearInterval(animationInterval)
    }
  }
}

function reset() {
  currentYear.value = 1979
  isPlaying.value = false
  playbackSpeed.value = 1
  granularity.value = 'fine'
  
  if (animationInterval) {
    clearInterval(animationInterval)
  }
}

onBeforeUnmount(() => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #e0e0e0;
  background: #1a1a1a;
  min-height: 100vh;
  padding: 20px;
}

h1 {
  margin-bottom: 5px;
}

h2 {
  margin-top: 0;
  color: #888;
  font-weight: normal;
}

.visualization-container {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.main-chart {
  flex: 2;
}

.side-charts {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/observable/src/App.vue
git commit -m "feat: 实现主应用组件"
```

---

### Task 12: GitHub Actions 部署工作流

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: 创建 deploy.yml**

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

- [ ] **Step 2: 提交**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: 添加 GitHub Actions 部署工作流"
```

---

### Task 13: 最终验证

- [ ] **Step 1: 运行开发服务器**

```bash
cd src/observable
npm run dev
```

Expected: 开发服务器启动，浏览器打开 http://localhost:5173 显示完整可视化

- [ ] **Step 2: 验证所有组件**

- 3D 散点图显示正常
- 热图显示正常
- CO₂ 时序图显示正常
- 时间滑块可拖动
- 播放/暂停功能正常
- 速度选择正常
- 粒度切换正常
- 重置功能正常

- [ ] **Step 3: 构建生产版本**

```bash
cd src/observable
npm run build
```

Expected: 构建成功，生成 `dist/` 目录

- [ ] **Step 4: 查看提交历史**

```bash
git log --oneline -10
```

Expected: 看到所有迁移相关的提交
