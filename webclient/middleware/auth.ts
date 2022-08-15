import { useToken } from "~~/methods/useToken"

export default defineNuxtRouteMiddleware((to, from) => {

    const token = useToken().getToken();

    if(!token) {
        console.log("401 unauthorized");
        return navigateTo('/login');
    }

  })