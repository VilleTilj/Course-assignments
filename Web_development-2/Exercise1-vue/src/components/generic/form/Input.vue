<script setup>
// A generic input component
import { computed } from "vue";

const props = defineProps({
  label: {
    type: String,
    default: null,
  },
  placeholder: {
    type: String,
    default: "",
  },
  value: {
    type: String,
    default: "",
  },
  // How long can the input be before a character count is shown?
  showCharCountAt: {
    type: Number,
    default: 20,
  },
});
const emit = defineEmits(["change"]);

// The 'computed' function allows variables that are derived from other variables to stay up to date.
const charCount = computed(() => props.value.length);

// The 'computed' function can also be used to change the setter and getter of a variable.
// Here we create a variable that is passed to the native 'input' element via 'v-model'
const internalValue = computed({
  get: () => props.value,
  // Every time the input value changes we emit a 'change' event to this component's parent
  set: (newValue) => emit("change", newValue),
});
</script>

<template>
  <label class="label">
    {{ label }}

    <input v-model="internalValue" :placeholder="placeholder" />

    <span v-show="charCount > showCharCountAt" class="char-count">{{
      charCount
    }}</span>
  </label>
</template>

<style lang="sass" scoped>
.label
  width: 100%
  position: relative

  input
    color: #281822
    width: inherit

    padding: 0.5rem 5ch 0.5rem 1rem
    border-radius: 7px
    background-color: #fbfaf8
    box-shadow: 1.1px 1.1px 2px rgba(0, 0, 0, 0.028), 3.8px 3.8px 4px rgba(0, 0, 0, 0.042), 0 3px 6px inset rgba(0,0,0,0.17)
    cursor: text

    &:focus-visible
      outline: 2px solid #C093AE

  .char-count
    position: absolute
    right: 1rem
    top: 0.5rem
    padding: inherit
    text-align: right
    opacity: 0.4
</style>
