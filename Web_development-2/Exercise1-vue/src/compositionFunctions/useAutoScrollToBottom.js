import { onMounted } from "vue";

// Observe changes to a container. When changes happen, scroll to the bottom of that container.
function useAutoScrollToBottom(ref) {
  function observeHeight() {
    const mutationObserver = new MutationObserver(() => {
      ref.value.scrollTop = ref.value.scrollHeight;
    });
    mutationObserver.observe(ref.value, { childList: true });
  }

  onMounted(() => {
    observeHeight();
  });
}

export default useAutoScrollToBottom;
