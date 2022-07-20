//adapted from: https://github.com/nuxt/framework/discussions/3801

import { useBackendBaseUrl } from "./useBackendBaseUrl";

import { useToken } from "./useToken";

import { FetchOptions } from "ohmyfetch";
import { GetTokenExpiredResponse } from "~~/types/GetTokenExpiredResponse";

export const useFetchAuth = async (url: string, opts?: FetchOptions) => {

  const backendBaseUrl = useBackendBaseUrl();

  const token = useToken().getToken();

  const headers: HeadersInit = {
    ...(opts?.headers || {}),
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  //todo:update
  const logoutIfTokenIsExpired = await $fetch(`${backendBaseUrl}/token/expired`, {
    method: 'GET', headers
  }).then((data:GetTokenExpiredResponse) => {
    if (data.expired) {
      useToken().deleteTokenCookie();
      navigateTo('/login');
      console.log("Logged out because AuthToken was expired. Please login again.");
      return false;
    }
  }).catch((error) => {
    console.log(error);
    useToken().deleteTokenCookie();
    navigateTo('/login');
    return false;
  }
  )

  return $fetch(backendBaseUrl + url, { ...opts, headers });
};