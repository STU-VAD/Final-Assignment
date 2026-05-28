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
