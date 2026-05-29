<template>
  <div id="app">
    <ClimateChart
      v-if="combinedData && tempData"
      :combinedData="combinedData"
      :tempData="tempData"
      :currentYear="currentYear"
      :isPlaying="isPlaying"
      :viewMode="viewMode"
      :animationSpeed="PLAY_SPEED"
      :hiddenBands="hiddenBands"
      @update:viewMode="viewMode = $event"
    />
    <Legend
      v-if="combinedData && tempData"
      :hiddenBands="hiddenBands"
      @toggle-band="toggleBand"
    />
    <div v-else class="loading">加载数据中...</div>

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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import ClimateChart from './components/ClimateChart.vue'
import Legend from './components/Legend.vue'
import ControlBar from './components/ControlBar.vue'
import { loadCombinedData, loadTemperatureData } from './data/loader'
import { BAND_8 } from './data/climate-data'
import type { CombinedData, TemperatureData, ViewMode } from './types'

const PLAY_SPEED = 500

const combinedData = ref<CombinedData | null>(null)
const tempData = ref<TemperatureData | null>(null)
const currentYear = ref(2025)
const isPlaying = ref(false)
const viewMode = ref<ViewMode>('3d')
const hiddenBands = ref<Set<string>>(new Set())
let animInterval: number | null = null

function toggleBand(key: string) {
  const next = new Set(hiddenBands.value)
  if (next.has(key)) {
    next.delete(key)
  } else {
    next.add(key)
  }
  hiddenBands.value = next
}

const stats = computed(() => {
  if (!combinedData.value) return null
  const item = combinedData.value.data.find(d => d.year === currentYear.value)
  if (!item) return null
  const arcticTemp = item.temperatures['64N-90N']
  return {
    co2: item.co2.toFixed(1),
    arcticTemp: (arcticTemp >= 0 ? '+' : '') + arcticTemp.toFixed(2),
  }
})

function setYear(year: number) {
  currentYear.value = Math.max(1979, Math.min(2025, year))
}

function togglePlay() {
  isPlaying.value = !isPlaying.value

  if (isPlaying.value) {
    if (currentYear.value >= 2025) setYear(1979)
    animInterval = window.setInterval(() => {
      if (currentYear.value < 2025) {
        currentYear.value++
      } else {
        isPlaying.value = false
        if (animInterval) clearInterval(animInterval)
      }
    }, PLAY_SPEED)
  } else {
    if (animInterval) {
      clearInterval(animInterval)
      animInterval = null
    }
  }
}

onMounted(async () => {
  const [combined, temp] = await Promise.all([
    loadCombinedData(),
    loadTemperatureData(),
  ])
  combinedData.value = combined
  tempData.value = temp
})

onBeforeUnmount(() => {
  if (animInterval) clearInterval(animInterval)
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'JetBrains Mono', monospace;
  background: #0f1419;
  color: #f2f5fa;
  min-height: 100vh;
  overflow: hidden;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 80px);
  color: #6b7a94;
  font-size: 14px;
}
</style>