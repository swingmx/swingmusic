const url = "http://127.0.0.1:9876/get/queue";

const getQueue = async (type, id) => {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      type: type,
      id: id,
    }),
  });

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  return data.songs;
};

export default getQueue;
