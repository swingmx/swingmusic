import { ref } from "@vue/reactivity";
import { reactive } from "vue";

const loading = ref(false);
const settings = reactive({
  uri: "http://127.0.0.1:9876",
});

export default {
  loading,
  settings,
};
