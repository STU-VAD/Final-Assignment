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
