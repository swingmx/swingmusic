import { FetchProps } from "../../interfaces";
import axios, { AxiosError, AxiosResponse } from "axios";

export default async (args: FetchProps) => {
  let data: any = null;
  let error: string = null;
  let status: number = null;

  function getAxios() {
    if (args.get) {
      return axios.get(args.url, args.props);
    }

    if (args.put) {
      return axios.put(args.url, args.props, args.headers);
    }

    return axios.post(args.url, args.props);
  }

  await getAxios()
    .then((res: AxiosResponse) => {
      data = res.data;
      status = res.status;
    })
    .catch((err: AxiosError) => {
      error = err.message as string;
      status = err.response.status as number;
    });

  return { data, error, status };
};
