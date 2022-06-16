export const useToken = () => {

    const name = "authToken";

    const setTokenCookie = (token: string) => {
        const date = new Date();

        // Set it expire in 7 days
        date.setTime(date.getTime() + (7 * 24 * 60 * 60 * 1000));

        // Set it
        document.cookie = name+"="+token+"; expires="+date.toUTCString()+"; path=/";
    }

    const getToken = () => {

        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        
        if (parts.length == 2) {
            return parts.pop().split(";").shift();
        }

    }

    const deleteTokenCookie = () => {

        const date = new Date();

        // Set it expire in -1 days
        date.setTime(date.getTime() + (-1 * 24 * 60 * 60 * 1000));

        // Set it
        document.cookie = name+"=; expires="+date.toUTCString()+"; path=/";
        
    }

    return { setTokenCookie, getToken, deleteTokenCookie }

}