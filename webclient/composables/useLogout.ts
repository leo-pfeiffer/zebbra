import { useToken } from "./useToken";

export const useLogout = () => {

    useFetchAuth('http://localhost:8000/logout', { method: 'POST'});

    useToken().deleteTokenCookie();

    navigateTo('/login');

}