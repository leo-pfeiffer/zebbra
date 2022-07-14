import { useFetchAuth } from "~~/methods/useFetchAuth";
import { useToken } from "./useToken";

export const useLogout = () => {

    useFetchAuth('/logout', { method: 'POST'});

    useToken().deleteTokenCookie();

    navigateTo('/login');

}