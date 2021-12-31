import { ref } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";

import media from "./mediaNotification.js";
import state from "./state.js";

const current = ref(state.current);

const next = ref({
  title: "The next song",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const prev = ref(state.prev);

const queue = ref(state.queue);

const search = ref("");

const putCommas = (artists) => {
  let result = [];

  artists.forEach((i, index, artists) => {
    if (index !== artists.length - 1) {
      result.push(i + ", ");
    } else {
      result.push(i);
    }
  });

  return result;
};

function updateNext(song_) {
  const index = state.queue.value.findIndex(
    (item) => item._id.$oid === song_._id.$oid
  );

  if (index == queue.value.length - 1) {
    next.value = queue.value[0];
    state.prev.value = queue.value[queue.value.length - 2];
  } else if (index == 0) {
    next.value = queue.value[1];
  } else {
    next.value = queue.value[index + 1];
  }
}

function updatePrev(song) {
  const index = state.queue.value.findIndex(
    (item) => item._id.$oid === song._id.$oid
  );

  if (index == 0) {
    prev.value = queue.value[queue.value.length - 1];
  } else if (index == queue.value.length - 1) {
    prev.value = queue.value[index - 1];
  } else {
    prev.value = queue.value[index - 1];
  }
}

const readQueue = () => {
  const prev_queue = JSON.parse(localStorage.getItem("queue"));
  const last_played = JSON.parse(localStorage.getItem("current"));

  if (last_played) {
    state.current.value = last_played;
  }

  if (prev_queue) {
    state.queue.value = prev_queue;
    
    updateNext(state.current.value);
    updatePrev(state.current.value);
  }
};

function focusCurrent() {
  const elem = document.getElementsByClassName("currentInQueue")[0];

  if (elem) {
    elem.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center",
    });
  }
}

setTimeout(() => {
  watch(current, (new_current) => {
    media.showMediaNotif();

    new Promise((resolve) => {
      updateNext(new_current);
      updatePrev(new_current);
      resolve();
    }).then(() => {
      focusCurrent();
    });

    localStorage.setItem("current", JSON.stringify(new_current));
  });
}, 1000);

window.addEventListener('keyup', (e) => {
  if (e.code) {
      console.log(e.code);
  }
});

export default {
  putCommas,
  readQueue,
  focusCurrent,
  current,
  queue,
  next,
  prev,
  search,
};
