<template>
  <div class="controls">
    <button @click="$emit('toggle-play')" class="play-btn">
      {{ isPlaying ? '⏸' : '▶' }}
    </button>

    <select :value="playbackSpeed" @change="$emit('update:playbackSpeed', Number(($event.target as HTMLSelectElement).value))">
      <option :value="0.5">0.5×</option>
      <option :value="1">1×</option>
      <option :value="2">2×</option>
      <option :value="4">4×</option>
    </select>

    <select :value="granularity" @change="$emit('update:granularity', ($event.target as HTMLSelectElement).value)">
      <option value="fine">8 细带</option>
      <option value="medium">3 粗带</option>
      <option value="hemisphere">半球</option>
    </select>

    <button @click="$emit('reset')" class="reset-btn">重置</button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isPlaying: boolean
  playbackSpeed: number
  granularity: string
}>()

defineEmits<{
  'toggle-play': []
  'update:playbackSpeed': [value: number]
  'update:granularity': [value: string]
  'reset': []
}>()
</script>

<style scoped>
.controls {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: #2a2a2a;
  border-radius: 8px;
}

.play-btn, .reset-btn {
  padding: 8px 16px;
  background: #444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.play-btn:hover, .reset-btn:hover {
  background: #555;
}

select {
  padding: 8px;
  background: #444;
  color: white;
  border: none;
  border-radius: 4px;
}
</style>
