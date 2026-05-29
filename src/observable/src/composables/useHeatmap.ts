import type { TemperatureData } from '../types'
import { BAND_8, TEMP_COLORSCALE, TEMP_MIN, TEMP_MAX } from '../data/climate-data'

export function useHeatmap() {
  function buildHeatmapTrace(tempData: TemperatureData) {
    const bandKeys = BAND_8.map(b => b.key)
    const bandLabels = BAND_8.map(b => b.label)

    const yearIndices: number[] = []
    const years: number[] = []
    tempData.years.forEach((y, i) => {
      if (y >= 1880) {
        yearIndices.push(i)
        years.push(y)
      }
    })

    const z: number[][] = bandKeys.map(bandKey => {
      const bandIdx = tempData.latitudeBands.indexOf(bandKey)
      if (bandIdx === -1) return years.map(() => 0)
      return yearIndices.map(i => tempData.anomalies[i]?.[bandIdx] ?? 0)
    })

    return {
      type: 'heatmap' as const,
      x: years,
      y: bandLabels,
      z,
      colorscale: TEMP_COLORSCALE,
      cmin: TEMP_MIN,
      cmax: TEMP_MAX,
      colorbar: {
        thickness: 10,
        title: { text: '温度异常 °C' },
        outlinewidth: 0,
        tickfont: { color: '#f2f5fa' },
        titlefont: { color: '#f2f5fa' },
      },
      hovertemplate: '年份 %{x}<br>纬度带 %{y}<br>温度异常 %{z:.2f} °C<extra></extra>',
      xaxis: 'x',
      yaxis: 'y',
    }
  }

  function buildHeatmapLayout() {
    return {
      xaxis: {
        anchor: 'y',
        domain: [0.65, 0.98],
        title: { text: '年份', font: { color: '#f2f5fa' } },
        tickfont: { color: '#f2f5fa', size: 8 },
        gridcolor: '#506784',
        linecolor: '#506784',
      },
      yaxis: {
        anchor: 'x',
        domain: [0.40, 0.98],
        title: { text: '纬度带', font: { color: '#f2f5fa' } },
        tickfont: { color: '#f2f5fa', size: 9 },
        gridcolor: '#506784',
        linecolor: '#506784',
      },
    }
  }

  return { buildHeatmapTrace, buildHeatmapLayout }
}
