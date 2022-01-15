let base_uri = "http://127.0.0.1:9876";

const getAlbumTracks = async (name, artist) => {
  const res = await fetch(
    base_uri +
      "/albums/" +
      encodeURIComponent(name.replaceAll("/", "|")) +
      "::" +
      encodeURIComponent(artist.replaceAll("/", "|"))
  );

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();

  return data;
};

const getAlbumArtists = async (name, artist) => {
  const res = await fetch(
    base_uri +
      "/album/" +
      encodeURIComponent(name.replaceAll("/", "|")) +
      "/" +
      encodeURIComponent(artist.replaceAll("/", "|")) +
      "/artists"
  );

  if (!res.ok) {
    const message = `An error has occured: ${res.status}`;
    throw new Error(message);
  }

  const data = await res.json();
  return data.artists;
};

export default {
  getAlbumTracks,
  getAlbumArtists,
};
