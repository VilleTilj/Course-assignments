<script setup>
// A chat bubble container
import useChatBubblePosition from "../useChatBubblePosition";

const props = defineProps({
  direction: {
    type: String,
    default: "right",
  },
});

// Import CSS variables from a 'hook'
const { cssVars } = useChatBubblePosition(props.direction);
</script>

<template>
  <div class="chat-bubble shadow-1" :style="cssVars">
    <slot />
  </div>
</template>

<style scoped lang="scss">
.chat-bubble {
  background-color: #fbfaf8;
  color: #281822;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  display: inline-block;
  position: relative;
  align-self: var(--align);
  margin: var(--margin);

  &::after {
    content: "";
    display: block;
    position: absolute;
    top: 0;
    left: var(--left);
    right: var(--right);
    height: 20px;
    width: 20px;
    background-color: inherit;
    clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 5%);
    border-radius: 0.25rem 0 0 0;
    transform: var(--transform);
  }
}
</style>
