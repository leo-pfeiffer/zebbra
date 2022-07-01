import { useToken } from "~~/composables/useToken"

export default defineNuxtRouteMiddleware((to, from) => {

    const token = useToken().getToken();

    if(!token) {
        console.log("401 unauthorized");
        return navigateTo('/login');
        //todo: add error message in modal that you have to be logged in
    }

    //todo: check if params org name is equal to workspace name in store

  })