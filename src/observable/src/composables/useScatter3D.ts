import type { CameraPreset, CombinedData, ViewMode } from '../types'
import { BAND_8, TEMP_COLORSCALE, TEMP_MIN, TEMP_MAX, CO2_MIN, CO2_MAX } from '../data/climate-data'

export const CAMERA_PRESETS: Record<ViewMode, CameraPreset> = {
  '3d':    { eye: { x: 1.5, y: -1.5, z: 0.8 }, center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceA': { eye: { x: 0, y: -2.5, z: 0 },     center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceB': { eye: { x: 2.5, y: 0, z: 0 },      center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 0, z: 1 } },
  'faceC': { eye: { x: 0, y: -0.01, z: 2.5 },  center: { x: 0, y: 0, z: 0 }, up: { x: 0, y: 1, z: 0 } },
}

export function useScatter3D() {
  function buildCurrentYearTrace(data: CombinedData, year: number) {
    const item = data.data.find(d => d.year === year)
    if (!item) return emptyTrace(year)

    const x: number[] = []
    const y: number[] = []
    const z: number[] = []
    const customdata: [number, string][] = []
    const colors: number[] = []

    for (const band of BAND_8) {
      const temp = item.temperatures[band.key]
      if (temp === undefined) continue
      x.push(item.co2)
      y.push(band.yPos)
      z.push(temp)
      customdata.push([year, band.key])
      colors.push(temp)
    }

    return {
      type: 'scatter3d' as const,
      scene: 'scene',
      mode: 'markers',
      name: String(year),
      showlegend: false,
      x, y, z,
      customdata,
      hovertemplate: '年份 %{customdata[0]}<br>纬度带 %{customdata[1]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
      marker: {
        size: 7,
        opacity: 0.9,
        color: colors,
        cmin: TEMP_MIN,
        cmax: TEMP_MAX,
        colorscale: TEMP_COLORSCALE,
        showscale: false,
      },
    }
  }

  function buildHistoryTrail(data: CombinedData, currentYear: number) {
    const x: number[] = []
    const y: number[] = []
    const z: number[] = []
    const customdata: [number, string][] = []
    const colors: number[] = []

    for (const item of data.data) {
      for (const band of BAND_8) {
        const temp = item.temperatures[band.key]
        if (temp === undefined) continue
        x.push(item.co2)
        y.push(band.yPos)
        z.push(temp)
        customdata.push([item.year, band.key])
        colors.push(temp)
      }
    }

    return {
      type: 'scatter3d' as const,
      scene: 'scene',
      mode: 'markers',
      name: '历史轨迹',
      showlegend: false,
      x, y, z,
      customdata,
      hovertemplate: '年份 %{customdata[0]}<br>纬度带 %{customdata[1]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
      marker: {
        size: 4,
        opacity: 0.25,
        color: colors,
        cmin: TEMP_MIN,
        cmax: TEMP_MAX,
        colorscale: TEMP_COLORSCALE,
        showscale: false,
      },
    }
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
      hovertemplate: '年份 %{customdata[0]}<br>纬度带 %{customdata[1]}<br>CO₂ %{x:.2f} ppm<br>温度异常 %{z:.2f} °C<extra></extra>',
      marker: { size: 7, opacity: 0.9, color: [], cmin: TEMP_MIN, cmax: TEMP_MAX, colorscale: TEMP_COLORSCALE, showscale: false },
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
      },
      yaxis: {
        title: { text: '纬度' },
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        zerolinecolor: '#C8D4E3',
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
      },
      domain: { x: [0, 0.62], y: [0.32, 1.0] },
    }
  }

  return { buildCurrentYearTrace, buildHistoryTrail, buildSceneLayout, CAMERA_PRESETS }
}
