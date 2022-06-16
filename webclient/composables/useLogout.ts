import { useToken } from "./useToken";

export const useLogout = () => {

    useToken().deleteTokenCookie();

    navigateTo('/login');

}