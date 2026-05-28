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
