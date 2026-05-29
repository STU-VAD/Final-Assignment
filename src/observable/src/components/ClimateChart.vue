<template>
  <div ref="chartRef" class="climate-chart"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import Plotly from 'plotly.js-dist'
import type { CombinedData, TemperatureData, ViewMode } from '../types'
import { BAND_8 } from '../data/climate-data'
import { useScatter3D } from '../composables/useScatter3D'
import { useHeatmap } from '../composables/useHeatmap'
import { useTimeSeries } from '../composables/useTimeSeries'

const props = defineProps<{
  combinedData: CombinedData | null
  tempData: TemperatureData | null
  currentYear: number
  isPlaying: boolean
  viewMode: ViewMode
  animationSpeed?: number
  hiddenBands: Set<string>
}>()

const emit = defineEmits<{
  'update:year': [year: number]
  'update:viewMode': [mode: ViewMode]
}>()

const animationDuration = computed(() => props.animationSpeed ?? 500)

const chartRef = ref<HTMLElement>()
const { buildCurrentYearTrace, buildHistoryTrail, buildTrendLines, buildSceneLayout, CAMERA_PRESETS } = useScatter3D()
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
  const trendLines = buildTrendLines(props.combinedData, props.currentYear)
  const heat = buildHeatmapTrace(props.tempData)
  const co2Line = buildCO2Line(props.combinedData)
  const co2Band = buildUncertaintyBand(props.combinedData)

  const currentArray = Array.isArray(current) ? current : [current]
  const trailArray = Array.isArray(trail) ? trail : [trail]

  return [...currentArray, ...trailArray, ...trendLines, heat, co2Band, co2Line]
}

function buildFrames() {
  if (!props.combinedData) return []

  return props.combinedData.years.map(year => {
    const current = buildCurrentYearTrace(props.combinedData!, year)
    const trail = buildHistoryTrail(props.combinedData!, year)
    const trendLines = buildTrendLines(props.combinedData!, year)

    const currentArray = Array.isArray(current) ? current : [current]
    const trailArray = Array.isArray(trail) ? trail : [trail]

    const frameData = [...currentArray, ...trailArray, ...trendLines]
    const traceIndices = Array.from({ length: frameData.length }, (_, i) => i)
    return {
      name: String(year),
      data: frameData,
      traces: traceIndices,
    }
  })
}

let initialized = false

function initChart() {
  if (!chartRef.value || !props.combinedData || !props.tempData) return

  const traces = buildTraces()
  const layout = buildLayout()
  const config = { responsive: true, displayModeBar: true }

  Plotly.newPlot(chartRef.value, traces, layout, config)

  ;(chartRef.value as any).on('plotly_doubleclick', () => {
    if (props.viewMode !== '3d') {
      emit('update:viewMode', '3d')
    }
  })

  const frames = buildFrames()
  Plotly.addFrames(chartRef.value, frames)

  initialized = true
}

function animateSilently(el: HTMLElement, frames: any, opts: any) {
  Plotly.animate(el, frames, opts).catch(() => {})
}

function updateChart() {
  if (!chartRef.value || !initialized || !props.combinedData || !props.tempData) return

  animateSilently(chartRef.value, [String(props.currentYear)], {
    frame: { duration: animationDuration.value, redraw: true },
    mode: 'immediate',
    fromcurrent: true,
  })
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

function syncVisibility() {
  if (!chartRef.value || !initialized) return

  for (let i = 0; i < BAND_8.length; i++) {
    const hidden = props.hiddenBands.has(BAND_8[i].key)
    Plotly.restyle(chartRef.value, { visible: !hidden }, [i, i + BAND_8.length, i + BAND_8.length * 2])
  }
}

watch(() => props.hiddenBands, () => syncVisibility(), { deep: true })

watch(() => props.currentYear, () => {
  if (props.isPlaying) return
  updateChart()
})

watch(() => props.isPlaying, (playing) => {
  if (!chartRef.value || !initialized) return

  if (playing) {
    animateSilently(chartRef.value, null, {
      frame: { duration: animationDuration.value, redraw: true },
      fromcurrent: true,
      mode: 'immediate',
    })
  } else {
    animateSilently(chartRef.value, [null], {
      frame: { duration: 0, redraw: false },
      mode: 'immediate',
    })
  }
})

watch(() => props.viewMode, (newMode, oldMode) => {
  if (newMode === oldMode) return
  switchCamera(newMode)
})

watch(() => [props.combinedData, props.tempData], () => {
  if (initialized && chartRef.value) {
    Plotly.purge(chartRef.value)
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