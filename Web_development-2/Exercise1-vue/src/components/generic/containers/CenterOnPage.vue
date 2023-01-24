<script setup>
/**
 * Centers content on the page.
 */

const props = defineProps({
  class: String,
});

const classes = `${props.class} center-container`;
</script>

<template>
  <div :class="classes">
    <slot />
  </div>
</template>

<style>
.center-container {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 1rem;
  background: radial-gradient(#f1f0f5, #f1ebeb);
}
</style>
