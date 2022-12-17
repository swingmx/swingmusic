<template>
  <div class="toasts" v-if="notifStore.notifs">
    <div
      class="new-notif rounded-sm"
      :class="notif.type"
      v-for="notif in notifStore.notifs"
    >
      <component :is="getSvg(notif.type)" class="notif-icon" />
      <div class="notif-text ellip">{{ notif.text }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotifStore, NotifType } from "../stores/notification";

import ErrorSvg from "../assets/icons/toast/error.svg";
import InfoSvg from "../assets/icons/toast/info.svg";
import SuccessSvg from "../assets/icons/toast/ok.svg";
import WorkingSvg from "../assets/icons/toast/working.svg";
import HeartSvg from "../assets/icons/heart.svg";

const notifStore = useNotifStore();

function getSvg(notif: NotifType) {
  switch (notif) {
    case NotifType.Error:
      return ErrorSvg;
    case NotifType.Info:
      return InfoSvg;
    case NotifType.Success:
      return SuccessSvg;
    case NotifType.Working:
      return WorkingSvg;
    case NotifType.Favorite:
      return HeartSvg;
  }
}
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
  gap: 1rem;
}

.new-notif {
  width: 20rem;
  height: 4rem;
  background-color: $gray;
  display: grid;
  place-items: center;
  box-shadow: 0px 0px 2rem rgba(0, 0, 0, 0.466);
  font-size: 0.85rem;
  padding: 1rem;

  grid-template-columns: 2rem 3fr;
  gap: $small;

  .notif-text {
    width: 100%;
  }
}

.new-notif.error {
  $bg: rgb(236, 31, 31);
  $bg1: rgba(236, 31, 31, 0.15);
  background-image: linear-gradient(275deg, $bg, $bg1 74%);
}

.new-notif.info, .new-notif.favorite {
  $bg: rgb(28, 102, 238);
  $bg1: rgba(31, 144, 236, 0.15);
  background-image: linear-gradient(275deg, $bg, $bg1 74%);
}

.new-notif.success {
  $bg: rgb(5, 167, 53);
  $bg1: rgba(5, 167, 54, 0.15);
  background-image: linear-gradient(275deg, $bg, $bg1 74%);
}

.new-notif.working {
  $bg: $gray4;
  $bg1: rgba(128, 128, 128, 0.151);
  background-image: linear-gradient(275deg, $bg, $bg1 74%);
}
</style>
