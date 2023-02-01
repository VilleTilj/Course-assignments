<script setup>
// Displays a timestamp in human-readable form
const props = defineProps({
  date: Date,
});

const time = props.date?.toLocaleTimeString("fi-FI", {
  hour: "2-digit",
  minute: "2-digit",
});
</script>

<template>
  <!-- v-show displays the element if the condition evaluates to true -->
  <span v-show="time" class="timestamp">{{ time }}</span>
</template>

<style scoped>
.timestamp {
  font-size: 0.8em;
  opacity: 0.6;
}
</style>
