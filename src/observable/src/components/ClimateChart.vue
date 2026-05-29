<template>
  <div ref="chartRef" class="climate-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import Plotly from 'plotly.js-dist'
import type { CombinedData, TemperatureData, ViewMode } from '../types'
import { useScatter3D } from '../composables/useScatter3D'
import { useHeatmap } from '../composables/useHeatmap'
import { useTimeSeries } from '../composables/useTimeSeries'

const props = defineProps<{
  combinedData: CombinedData | null
  tempData: TemperatureData | null
  currentYear: number
  isPlaying: boolean
  viewMode: ViewMode
}>()

const emit = defineEmits<{
  'update:year': [year: number]
  'update:viewMode': [mode: ViewMode]
}>()

const chartRef = ref<HTMLElement>()
const { buildCurrentYearTrace, buildHistoryTrail, buildSceneLayout, CAMERA_PRESETS } = useScatter3D()
const { buildHeatmapTrace, buildHeatmapLayout } = useHeatmap()
const { buildCO2Line, buildUncertaintyBand, buildTimeSeriesLayout } = useTimeSeries()

function buildLayout() {
  const sceneLayout = buildSceneLayout()
  const heatmapLayout = buildHeatmapLayout()
  const tsLayout = buildTimeSeriesLayout()

  return {
    paper_bgcolor: '#0f1419',
    plot_bgcolor: '#0f1419',
    font: { color: '#f2f5fa', family: 'JetBrains Mono, monospace' },
    margin: { l: 40, r: 20, t: 20, b: 10 },
    showlegend: false,
    hovermode: 'closest',
    scene: sceneLayout,
    ...heatmapLayout,
    ...tsLayout,
  }
}

function buildTraces() {
  if (!props.combinedData || !props.tempData) return []

  const current = buildCurrentYearTrace(props.combinedData, props.currentYear)
  const trail = buildHistoryTrail(props.combinedData, props.currentYear)
  const heat = buildHeatmapTrace(props.tempData)
  const co2Line = buildCO2Line(props.combinedData)
  const co2Band = buildUncertaintyBand(props.combinedData)

  return [current, trail, heat, co2Band, co2Line]
}

function buildFrames() {
  if (!props.combinedData) return []

  return props.combinedData.years.map(year => {
    const current = buildCurrentYearTrace(props.combinedData!, year)
    const trail = buildHistoryTrail(props.combinedData!, year)
    return {
      name: String(year),
      data: [current, trail] as Partial<Plotly.PlotData>[],
      traces: [0, 1],
    }
  })
}

let initialized = false

function initChart() {
  if (!chartRef.value || !props.combinedData || !props.tempData) return

  const traces = buildTraces()
  const layout = buildLayout()
  const config = { responsive: true, displayModeBar: false }

  Plotly.newPlot(chartRef.value, traces, layout, config)

  chartRef.value.on('plotly_doubleclick', () => {
    if (props.viewMode !== '3d') {
      emit('update:viewMode', '3d')
    }
  })

  const frames = buildFrames()
  Plotly.addFrames(chartRef.value, frames)

  initialized = true
}

function updateChart() {
  if (!chartRef.value || !initialized || !props.combinedData || !props.tempData) return

  Plotly.animate(chartRef.value, [String(props.currentYear)], {
    frame: { duration: 200, redraw: true },
    mode: 'immediate',
    fromcurrent: true,
  }).catch(() => {})
}

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
    Plotly.relayout(chartRef.value, {
      'scene.camera': {
        eye: preset.eye,
        center: preset.center,
        up: preset.up,
        projection: { type: 'perspective' },
      },
    })
    modeTransitionTimer = window.setTimeout(() => {
      if (!chartRef.value) return
      Plotly.relayout(chartRef.value, {
        'scene.camera.projection.type': 'orthographic',
      })
    }, 450)
  } else {
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

watch(() => props.currentYear, () => {
  if (props.isPlaying) return
  updateChart()
})

watch(() => props.isPlaying, (playing) => {
  if (!chartRef.value || !initialized) return

  if (playing) {
    Plotly.animate(chartRef.value, null, {
      frame: { duration: 200, redraw: true },
      fromcurrent: true,
      mode: 'immediate',
    }).catch(() => {})
  } else {
    Plotly.animate(chartRef.value, [null], {
      frame: { duration: 0, redraw: false },
      mode: 'immediate',
    }).catch(() => {})
  }
})

watch(() => props.viewMode, (newMode, oldMode) => {
  if (newMode === oldMode) return
  switchCamera(newMode)
})

watch(() => [props.combinedData, props.tempData], () => {
  if (initialized) {
    Plotly.purge(chartRef.value!)
    initialized = false
  }
  initChart()
})

onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  if (chartRef.value && initialized) {
    Plotly.purge(chartRef.value)
  }
  if (modeTransitionTimer) clearTimeout(modeTransitionTimer)
})
</script>

<style scoped>
.climate-chart {
  width: 100%;
  height: calc(100vh - 80px);
}
</style>
