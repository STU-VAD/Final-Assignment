import type { CameraPreset, CombinedData, ViewMode } from '../types'
import { BAND_8, TEMP_COLORSCALE, TEMP_MIN, TEMP_MAX, CO2_MIN, CO2_MAX } from '../data/climate-data'

export const CAMERA_PRESETS: Record<ViewMode, CameraPreset> = {
  '3d': { eye: { x: 1.5, y: -1.5, z: 0.8 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceA': { eye: { x: 0, y: -2.5, z: 0 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceB': { eye: { x: 2.5, y: 0, z: 0 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceC': { eye: { x: 0, y: -0.01, z: 2.5 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 1, z: 0 } },
}

export function useScatter3D() {
  function buildCurrentYearTrace(data: CombinedData, year: number) {
    const item = data.data.find(d => d.year === year)
    if (!item) return emptyTrace(year)

    const traces: any[] = []

    for (const band of BAND_8) {
      const temp = item.temperatures[band.key]
      if (temp === undefined) continue

      traces.push({
        type: 'scatter3d' as const,
        scene: 'scene',
        mode: 'markers',
        name: String(year),
        showlegend: false,
        x: [item.co2],
        y: [band.yPos],
        z: [temp],
        customdata: [[year, band.key, band.label]],
        hovertemplate: '%{customdata[2]}<br>年份 %{customdata[0]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
        marker: {
          size: 9,
          opacity: 0.95,
          color: band.color,
          line: {
            width: 2,
            color: '#ffffff',
          },
        },
      })
    }

    return traces.length > 0 ? traces : emptyTrace(year)
  }

  function buildHistoryTrail(data: CombinedData, currentYear: number) {
    const traces: any[] = []

    for (const band of BAND_8) {
      const x: number[] = []
      const y: number[] = []
      const z: number[] = []
      const customdata: [number, string, string][] = []

      for (const item of data.data) {
        if (item.year > currentYear) break
        const temp = item.temperatures[band.key]
        if (temp === undefined) continue
        x.push(item.co2)
        y.push(band.yPos)
        z.push(temp)
        customdata.push([item.year, band.key, band.label])
      }

      if (x.length === 0) continue

      traces.push({
        type: 'scatter3d' as const,
        scene: 'scene',
        mode: 'markers',
        name: '历史轨迹',
        showlegend: false,
        x, y, z,
        customdata,
        hovertemplate: '%{customdata[2]}<br>年份 %{customdata[0]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
        marker: {
          size: 4,
          opacity: 0.35,
          color: band.color,
        },
      })
    }

    return traces.length > 0 ? traces : {
      type: 'scatter3d' as const,
      scene: 'scene',
      mode: 'markers',
      name: '历史轨迹',
      showlegend: false,
      x: [], y: [], z: [],
      customdata: [],
      hovertemplate: '',
      marker: { size: 4, opacity: 0.35, color: [] },
    }
  }

  function buildTrendLines(data: CombinedData, currentYear: number) {
    const traces: any[] = []

    for (const band of BAND_8) {
      const x: number[] = []
      const y: number[] = []
      const z: number[] = []
      const years: number[] = []

      for (const item of data.data) {
        if (item.year > currentYear) break
        const temp = item.temperatures[band.key]
        if (temp === undefined) continue
        x.push(item.co2)
        y.push(band.yPos)
        z.push(temp)
        years.push(item.year)
      }

      if (x.length < 2) continue

      traces.push({
        type: 'scatter3d' as const,
        scene: 'scene',
        mode: 'lines',
        name: `${band.key} 趋势`,
        showlegend: false,
        x, y, z,
        customdata: years.map(year => [year, band.key, band.label]),
        hovertemplate: '%{customdata[2]}<br>年份 %{customdata[0]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
        line: {
          width: 2,
          color: band.color,
          opacity: 0.7,
        },
      })
    }

    return traces
  }

  function emptyTrace(year: number) {
    return {
      type: 'scatter3d' as const,
      scene: 'scene',
      mode: 'markers',
      name: String(year),
      showlegend: false,
      x: [] as number[], y: [] as number[], z: [] as number[],
      customdata: [],
      hovertemplate: '',
      marker: { size: 7, opacity: 0.9, color: [] },
    }
  }

  function buildSceneLayout() {
    return {
      bgcolor: 'rgb(17,17,17)',
      camera: { eye: { x: 1.5, y: -1.5, z: 0.8 } },
      xaxis: {
        title: { text: 'CO₂ (ppm)' },
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        zerolinecolor: '#C8D4E3',
        range: [CO2_MIN, CO2_MAX],
        clipfase: false,
      },
      yaxis: {
        title: { text: '纬度' },
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        zerolinecolor: '#C8D4E3',
        clipfase: false,
      },
      zaxis: {
        title: { text: '温度异常 (°C)' },
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        zerolinecolor: '#C8D4E3',
        range: [TEMP_MIN, TEMP_MAX],
        clipfase: false,
      },
      domain: { x: [0, 0.62], y: [0.32, 1.0] },
    }
  }

  return { buildCurrentYearTrace, buildHistoryTrail, buildTrendLines, buildSceneLayout, CAMERA_PRESETS }
}