import { useToken } from "./useToken";

export const useLogout = (backendUrlBase:string) => {

    useFetchAuth(backendUrlBase + '/logout', { method: 'POST'});

    useToken().deleteTokenCookie();

    navigateTo('/login');

}