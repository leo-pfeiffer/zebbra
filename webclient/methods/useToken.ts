export const useToken = () => {
    
    const name = "authToken";
    const date = new Date();
    date.setTime(date.getTime() + (7 * 24 * 60 * 60 * 1000));

    const authCookie = useCookie(name, {expires:date});

    const setTokenCookie = (token: string) => {
        authCookie.value = token;
    }

    const getToken = () => {
        return authCookie.value;
    }

    const deleteTokenCookie = () => {
        authCookie.value = undefined;
    }

    return { setTokenCookie, getToken, deleteTokenCookie }

}