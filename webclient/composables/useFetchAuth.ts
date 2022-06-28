//adapted from: https://github.com/nuxt/framework/discussions/3801

import { FetchOptions } from "ohmyfetch";
import { useLogout } from "./useLogout";

export const useFetchAuth = (url: string, opts?: FetchOptions) => {

  
  type GetTokenExpiredResponse = {
    expired: Boolean;
  }


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
      useLogout();
      console.log("Logged out because AuthToken was expired. Please login again.");
      return false
    }
    console.log("AuthToken up to date.");
  }).catch((error) => {
    console.log(error);
    useLogout();
    return false;
  }
  )

  return $fetch(url, { ...opts, headers });
};