<template>
  <div class="control-bar">
    <button class="play-btn" @click="$emit('toggle-play')">
      {{ isPlaying ? '⏸ 暂停' : '▶ 播放' }}
    </button>

    <div class="mode-btns">
      <button
        v-for="m in modes"
        :key="m.id"
        class="mode-btn"
        :class="{ active: viewMode === m.id }"
        @click="$emit('update:viewMode', m.id)"
        :title="m.tip"
      >{{ m.label }}</button>
    </div>

    <div class="year-display">{{ currentYear }}</div>

    <div class="slider-wrap">
      <input
        type="range"
        :min="minYear"
        :max="maxYear"
        :value="currentYear"
        step="1"
        @input="$emit('update:year', Number(($event.target as HTMLInputElement).value))"
      />
    </div>

    <div class="stats" v-if="stats">
      <div class="stat">
        <div class="stat-val" style="color: #ffc048">{{ stats.co2 }}</div>
        <div class="stat-label">CO₂ ppm</div>
      </div>
      <div class="stat">
        <div class="stat-val" style="color: #e94560">{{ stats.arcticTemp }}</div>
        <div class="stat-label">北极 °C</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ViewMode } from '../types'

defineProps<{
  currentYear: number
  minYear: number
  maxYear: number
  isPlaying: boolean
  stats: { co2: string; arcticTemp: string } | null
  viewMode: ViewMode
}>()

defineEmits<{
  'toggle-play': []
  'update:year': [year: number]
  'update:viewMode': [mode: ViewMode]
}>()

const modes: { id: ViewMode; label: string; tip: string }[] = [
  { id: '3d',    label: '3D',      tip: '三维全景' },
  { id: 'faceA', label: 'CO₂×T',   tip: 'CO₂ × 温度异常' },
  { id: 'faceB', label: 'Lat×T',   tip: '纬度 × 温度异常' },
  { id: 'faceC', label: 'CO₂×Lat', tip: 'CO₂ × 纬度' },
]
</script>

<style scoped>
.control-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 24px;
  background: #0f1419;
  border-top: 1px solid #1a2540;
}

.play-btn {
  padding: 6px 16px;
  background: transparent;
  color: #e94560;
  border: 1px solid #e94560;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  font-size: 13px;
  transition: all 0.2s;
  white-space: nowrap;
}
.play-btn:hover {
  background: #e94560;
  color: #fff;
}

.year-display {
  font-size: 36px;
  font-weight: 200;
  color: #e94560;
  min-width: 90px;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.slider-wrap {
  flex: 1;
}
.slider-wrap input[type="range"] {
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
  background: #1a2540;
  border-radius: 2px;
  outline: none;
}
.slider-wrap input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: #e94560;
  border-radius: 50%;
  cursor: grab;
  box-shadow: 0 0 8px rgba(233, 69, 96, 0.4);
}

.stats {
  display: flex;
  gap: 20px;
}
.stat {
  text-align: center;
}
.stat-val {
  font-size: 20px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  line-height: 1;
}
.stat-label {
  font-size: 8px;
  color: #6b7a94;
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 2px;
}
.mode-btns {
  display: flex;
  gap: 4px;
}
.mode-btn {
  padding: 4px 8px;
  background: transparent;
  color: #6b7a94;
  border: 1px solid #1a2540;
  border-radius: 3px;
  cursor: pointer;
  font-family: inherit;
  font-size: 10px;
  transition: all 0.2s;
  white-space: nowrap;
}
.mode-btn:hover {
  border-color: #e94560;
  color: #e94560;
}
.mode-btn.active {
  background: #e94560;
  border-color: #e94560;
  color: #fff;
}
</style>
