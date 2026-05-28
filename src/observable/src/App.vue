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
