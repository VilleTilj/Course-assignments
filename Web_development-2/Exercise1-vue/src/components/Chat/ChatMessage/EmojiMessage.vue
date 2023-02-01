<script setup>
import useIcons from "../../../compositionFunctions/useIcons";
import useChatBubblePosition from "../useChatBubblePosition";

const props = defineProps({
  emoji: String,
  direction: {
    type: String,
    default: "right",
  },
});

const icons = useIcons();

const { cssVars } = useChatBubblePosition(props.direction);
</script>

<template>
  <img :src="icons[props.emoji]" :alt="props.emoji" :style="cssVars" />
</template>

<style scoped>
img {
  width: 48px;
  height: 48px;
  display: inline-block;
  position: relative;
  align-self: var(--align);
  margin: var(--margin);
}
</style>
