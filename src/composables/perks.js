import { ref } from "@vue/reactivity";

const current = ref({
    title: "Nothing played yet",
    artists: ["... blah blah blah"],
});

const next = ref({
    title: "Next song shows here",
    artists: ["... blah blah blah"],
});

const queue = ref([
    {
        title: "Nothing played yet",
        artists: ["... blah blah blah"],
        _id: {
            $oid: ""
        }
    }
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
    const last_played =  JSON.parse(localStorage.getItem("current"));
    const next_ = JSON.parse(localStorage.getItem("next"));

    if (last_played){
        current.value = last_played;
    }

    if (prev_queue){
        queue.value = prev_queue;
    }

    if (next_){
        next.value = next_;
    }
}

export default { putCommas, doThat, readQueue, current, queue, next };
