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
