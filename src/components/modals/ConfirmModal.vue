<template>
  <div class="confirm-modal">
    <div class="t-center" style="padding: 0 4rem">{{ text }}</div>
    <div class="buttons">
      <button class="cancel" @click="cancelAction">Cancel</button>
      <button class="confirm" @click="confirmAction">Delete</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text: string;
  confirmAction: () => void;
  cancelAction: () => void;
}>();
</script>

<style lang="scss">
.confirm-modal {
  .buttons {
    margin-top: 2rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .confirm {
    background: $red;
  }
}
</style>
