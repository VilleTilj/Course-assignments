<script setup>
import useIcons from "../../../compositionFunctions/useIcons";

const emit = defineEmits(["click"]);
const props = defineProps({
  icon: {
    type: String,
    default: null,
  },
  alt: {
    type: String,
    default: "",
  },
});

// Get the required icons
const icons = useIcons();

/**
 * Handles click events on this button
 * @param {Event} event
 */
function onClick(event) {
  emit("click", event);
}
</script>

<template>
  <button class="button shadow-1" @click="onClick">
    <img v-if="icon" :src="icons[icon]" :alt="alt" />
  </button>
</template>

<style lang="sass" scoped>
.button
  border: none
  box-sizing: inherit
  background-color: #fbfaf8
  border-radius: 99rem
  padding: 0.5rem
  cursor: pointer
  line-height: 0

  &:hover,
  &:focus-visible
    background-color: #fffefb

  &:focus-visible
    outline: 2px solid #C093AE

  img
    width: 24px
    height: 24px
</style>
