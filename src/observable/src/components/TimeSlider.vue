<template>
  <div class="time-slider">
    <input
      type="range"
      :min="minYear"
      :max="maxYear"
      :value="modelValue"
      @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))"
      class="slider"
    />
    <div class="year-display">{{ modelValue }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: number
  minYear: number
  maxYear: number
}>()

defineEmits<{
  'update:modelValue': [value: number]
}>()
</script>

<style scoped>
.time-slider {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.slider {
  flex: 1;
  height: 10px;
  -webkit-appearance: none;
  appearance: none;
  background: #444;
  border-radius: 5px;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fbbf24;
  cursor: pointer;
}

.year-display {
  font-size: 18px;
  font-weight: bold;
  color: #fbbf24;
  min-width: 60px;
  text-align: center;
}
</style>
