import { ref } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";

import media from "./mediaNotification.js";

const current = ref({
  title: "Nothing played yet",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const next = ref({
  title: "The next song",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const prev = ref({
  title: "The previous song",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const queue = ref([
  {
    title: "Nothing played yet",
    artists: ["... blah blah blah"],
    _id: {
      $oid: "",
    },
  },
]);

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

const doThat = (songs, current) => {
  queue.value = songs;
  current.value = current;

  console.log(queue.value);
};

const readQueue = () => {
  const prev_queue = JSON.parse(localStorage.getItem("queue"));
  const last_played = JSON.parse(localStorage.getItem("current"));
  const next_ = JSON.parse(localStorage.getItem("next"));
  const prev_ = JSON.parse(localStorage.getItem("prev"));

  if (last_played) {
    current.value = last_played;
  }

  if (prev_queue) {
    queue.value = prev_queue;
  }

  if (next_) {
    next.value = next_;
  }

  if (prev_) {
    prev.value = prev_;
  }
};

watch(current, (new_current, old_current) => {
  media.showMediaNotif();

  new Promise((resolve) => {
    const index = queue.value.findIndex(
      (item) => item._id.$oid === new_current._id.$oid
    );

    if (index == queue.value.length - 1) {
      next.value = queue.value[0];
      prev.value = queue.value[queue.value.length - 2];
    } else if (index == 0) {
      next.value = queue.value[1];
    } else {
      next.value = queue.value[index + 1];
    }

    prev.value = old_current;
    resolve();
  }).then(() => {
    const elem = document.getElementsByClassName("currentInQueue")[0];

    if (elem) {
      elem.scrollIntoView({
        behavior: "smooth",
        block: "center",
        inline: "center",
      });
    }
  });
  
  localStorage.setItem("current", JSON.stringify(new_current));
  localStorage.setItem("prev", JSON.stringify(prev.value));
});

export default { putCommas, doThat, readQueue, current, queue, next, prev };
