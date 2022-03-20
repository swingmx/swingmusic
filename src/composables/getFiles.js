let base_uri = "http://127.0.0.1:9876/";

const getTracksAndDirs = async (path) => {
    let url;

    const encoded_path = encodeURIComponent(path.replaceAll("/", "|"));
    url = url = `${base_uri}/f/${encoded_path}`;

    const res = await fetch(url);

    if (!res.ok) {
        const message = `An error has occurred: ${res.status}`;
        throw new Error(message);
    }

    const data = await res.json();

    const songs = data.files;
    const folders = data.folders;

    return {songs, folders};
};

export default getTracksAndDirs;
