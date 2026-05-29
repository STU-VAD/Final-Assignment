<template>
  <div class="legend-panel" :class="{ collapsed: isCollapsed }">
    <div class="legend-header" @click="toggleCollapse">
      <div class="legend-title">纬度带</div>
      <div class="collapse-icon">{{ isCollapsed ? '▶' : '▼' }}</div>
    </div>
    <div class="legend-content" v-show="!isCollapsed">
      <div class="legend-items">
        <div
          v-for="band in bands"
          :key="band.key"
          class="legend-item"
          :class="{ 'legend-item--hidden': hiddenBands.has(band.key) }"
          :title="band.label"
          @click="emit('toggle-band', band.key)"
        >
          <div
            class="legend-color"
            :style="{ backgroundColor: hiddenBands.has(band.key) ? '#3a4455' : band.color }"
          ></div>
          <span class="legend-label">{{ band.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { BAND_8 } from '../data/climate-data'

const props = defineProps<{
  hiddenBands: Set<string>
}>()

const emit = defineEmits<{
  'toggle-band': [key: string]
}>()

const bands = BAND_8
const isCollapsed = ref(false)

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.legend-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(15, 20, 25, 0.9);
  border: 1px solid #1a2540;
  border-radius: 8px;
  padding: 0;
  z-index: 100;
  min-width: 160px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.legend-panel.collapsed {
  min-width: 120px;
}

.legend-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.legend-header:hover {
  background: rgba(233, 69, 96, 0.1);
}

.legend-title {
  font-size: 12px;
  font-weight: 600;
  color: #f2f5fa;
}

.collapse-icon {
  font-size: 10px;
  color: #6b7a94;
  transition: transform 0.3s ease;
}

.legend-panel.collapsed .collapse-icon {
  transform: rotate(-90deg);
}

.legend-content {
  padding: 0 12px 12px 12px;
  max-height: 300px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.legend-panel.collapsed .legend-content {
  padding: 0 12px;
  max-height: 0;
  opacity: 0;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.legend-item:hover {
  background: rgba(233, 69, 96, 0.1);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  font-size: 10px;
  color: #6b7a94;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s, opacity 0.2s;
}

.legend-item--hidden .legend-label {
  color: #3a4455;
  opacity: 0.5;
  text-decoration: line-through;
}

.legend-item--hidden .legend-color {
  opacity: 0.4;
  transition: background-color 0.2s, opacity 0.2s;
}
</style>