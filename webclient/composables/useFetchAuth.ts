//adapted from: https://github.com/nuxt/framework/discussions/3801

import { FetchOptions } from "ohmyfetch";
import { useLogout } from "./useLogout";
import { GetTokenExpiredResponse } from "~~/types/GetTokenExpiredResponse";

export const useFetchAuth = (url: string, opts?: FetchOptions) => {

  const token = useToken().getToken();

  const headers: HeadersInit = {
    ...(opts?.headers || {}),
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const logoutIfTokenIsExpired = $fetch('http://localhost:8000/token/expired', {
    method: 'GET', headers
  }).then((data:GetTokenExpiredResponse) => {
    console.log("Checking AuthToken");
    if (data.expired) {
      useToken().deleteTokenCookie();
      navigateTo('/login');
      console.log("Logged out because AuthToken was expired. Please login again.");
      return false;
    }
    console.log("AuthToken up to date.");
  }).catch((error) => {
    console.log(error);
    useToken().deleteTokenCookie();
    navigateTo('/login');
    return false;
  }
  )

  return $fetch(url, { ...opts, headers });
};