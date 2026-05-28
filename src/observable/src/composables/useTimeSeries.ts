import type { CombinedData } from '../types'

export function useTimeSeries() {
  function buildCO2Line(data: CombinedData) {
    return {
      type: 'scatter' as const,
      mode: 'lines',
      name: 'CO₂ 年均',
      x: data.data.map(d => d.year),
      y: data.data.map(d => d.co2),
      line: { color: '#ffc048', width: 2 },
      xaxis: 'x2',
      yaxis: 'y2',
      hovertemplate: '年份 %{x}<br>CO₂ %{y:.2f} ppm<extra></extra>',
    }
  }

  function buildUncertaintyBand(data: CombinedData) {
    return {
      type: 'scatter' as const,
      mode: 'lines',
      name: '不确定性',
      showlegend: false,
      x: [...data.data.map(d => d.year), ...[...data.data].reverse().map(d => d.year)],
      y: [...data.data.map(d => d.co2 - d.co2Unc), ...[...data.data].reverse().map(d => d.co2 + d.co2Unc)],
      fill: 'toself',
      fillcolor: 'rgba(255,192,72,0.15)',
      line: { width: 0 },
      xaxis: 'x2',
      yaxis: 'y2',
      hoverinfo: 'skip',
    }
  }

  function buildTimeSeriesLayout() {
    return {
      xaxis2: {
        anchor: 'y2',
        domain: [0.0, 1.0],
        title: { text: '', font: { color: '#f2f5fa' } },
        tickfont: { color: '#f2f5fa', size: 9 },
        gridcolor: '#506784',
        linecolor: '#506784',
      },
      yaxis2: {
        anchor: 'x2',
        domain: [0.0, 0.28],
        title: { text: 'CO₂ (ppm)', font: { color: '#ffc048' } },
        tickfont: { color: '#f2f5fa', size: 9 },
        gridcolor: '#506784',
        linecolor: '#506784',
      },
    }
  }

  return { buildCO2Line, buildUncertaintyBand, buildTimeSeriesLayout }
}
