<template>
  <div class="toasts" v-if="notifStore.notifs">
    <div
      class="new-notif rounded"
      :class="[
        { 'notif-error': notif.type == NotifType.Error },
        {
          'notif-info': notif.type == NotifType.Info,
        },
      ]"
      v-for="notif in notifStore.notifs"
    >
      <div class="ellip">{{ notif.text }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotifStore, NotifType } from "../stores/notification";

const notifStore = useNotifStore();
</script>
<style lang="scss">
.toasts {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  translate: -50%;
  z-index: 100;
  display: flex;
  flex-direction: column-reverse;
  gap: $small;
}

.new-notif {
  width: 20rem;
  height: 3.5rem;
  bottom: 2rem;
  padding: $small;
  background: linear-gradient(to top right, #021b79, #0575e6);
  display: grid;
  place-items: center;
  align-items: center;
  box-shadow: 0px 0px 2rem rgb(0, 0, 0);

  .link {
    font-weight: bold;
    text-decoration: underline;
  }
}

.notif-error {
  background: linear-gradient(to top right, #cf0b25, #e60518);
}

.notif-info {
  background: linear-gradient(to top right, $gray4, $gray3);
}
</style>
