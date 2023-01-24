<script setup>
import { ref } from "vue";
import Input from "../generic/form/Input.vue";
import Button from "../generic/form/Button.vue";
import EmojiSelector from "./EmojiSelector/EmojiSelector.vue";

// Store the text input value
const text = ref("");

/**
 * Handle changes to the text input value
 * @param {String} newValue New text value
 */
const onChange = (newValue) => {
  text.value = newValue;
};

// Components emit events. Parent components listen to these events. Just like the DOM!
const emit = defineEmits(["send"]);

/**
 * Sends a text message.
 */
function send() {
  emit("send", text.value, "text");
  text.value = "";
}

/**
 * Sends an emoji message.
 */
function sendEmoji(name) {
  emit("send", name, "emoji");
}
</script>

<template>
  <div class="compose">
    <EmojiSelector @send="sendEmoji" />

    <div class="message-row">
      <Input
        :value="text"
        placeholder="Type a message"
        @change="onChange"
        @keydown.enter="send"
      />

      <Button icon="send" @click="send" />
    </div>
  </div>
</template>

<style scoped>
.message-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}
/* This targets a nested component with scoped styles*/
.compose:deep(.emoji-selector) {
  margin-bottom: 0.5rem;
}
</style>
