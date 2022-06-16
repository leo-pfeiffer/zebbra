//from: https://github.com/nuxt/framework/discussions/3801

import { FetchOptions } from "ohmyfetch";

export const useFetchAuth = (url: string, opts?: FetchOptions) => {
  const { token } = useProfile();

  const headers: HeadersInit = {
    ...(opts?.headers || {}),
    ...(token && { Authorization: `Bearer ${token.value}` }),
  };
  return $fetch(url, { ...opts, headers });
};