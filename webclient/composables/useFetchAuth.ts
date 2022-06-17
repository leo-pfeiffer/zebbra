//adapted from: https://github.com/nuxt/framework/discussions/3801

import { FetchOptions } from "ohmyfetch";

export const useFetchAuth = (url: string, opts?: FetchOptions) => {
  const token = useToken().getToken();

  const headers: HeadersInit = {
    ...(opts?.headers || {}),
    ...(token && { Authorization: `Bearer ${token}` }),
  };
  return $fetch(url, { ...opts, headers });
};