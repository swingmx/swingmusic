import { paths } from "@/config";
import { Folder, Track } from "@/interfaces";
import useAxios from "./useAxios";

export default async function (path: string) {
  interface FolderData {
    tracks: Track[];
    folders: Folder[];
  }

  const { data, error } = await useAxios({
    url: paths.api.folder,
    props: {
      folder: path,
    },
  });

  if (error) {
    console.error(error);
  }

  if (data) {
    return data as FolderData;
  }

  return <FolderData>{
    tracks: [],
    folders: [],
  };
}
