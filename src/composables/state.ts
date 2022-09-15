import { ref } from "@vue/reactivity";

const loading = ref(false);
const settings = {
  uri: "http://10.5.8.81:1970",
};

export default {
  loading,
  settings,
};
