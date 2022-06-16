import { useToken } from "~~/composables/useToken"

export default defineNuxtRouteMiddleware((to, from) => {

    const token = useToken().getToken;

    console.log("auth");
    console.log(token);

    if(!token) {
        navigateTo("/login")
    }

    /* console.log("auth middleware");
    const { token } = useProfile();
    console.log(token) */

  })