import { ref } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";

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

  if (last_played) {
    current.value = last_played;
  }

  if (prev_queue) {
    queue.value = prev_queue;
  }

  if (next_) {
    next.value = next_;
  }
};

watch(current, (new_current) => {
  localStorage.setItem("current", JSON.stringify(new_current));

  const index = queue.value.findIndex(
    (item) => item._id.$oid === new_current._id.$oid
  );

  if (index == queue.value.length - 1) {
    next.value = queue.value[0];
    prev.value = queue.value[queue.value.length - 2];
  } else if (index == 0) {
    next.value = queue.value[1];
    prev.value = queue.value[queue.value.length - 1];
  } else {
    next.value = queue.value[index + 1];
    prev.value = queue.value[index - 1];
  }
});

export default { putCommas, doThat, readQueue, current, queue, next, prev };
