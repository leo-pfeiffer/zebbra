<script setup lang="ts">

const config = useRuntimeConfig();

</script>

<template>
  <div class="container flex justify-center mx-auto">
    <div class="w-1/2 md:w-1/4">
      <div>
        <h1 class="text-2xl mb-4 mt-16 text-zinc-900 font-semibold">Login</h1>
      </div>
      <div class="w-full">
        <form @submit.prevent="login">
          <div>
            <label class="block text-xs font-medium text-zinc-500" for="login-email">Email</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="login-email" type="email" placeholder="you@company.com" v-model="form.username">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="login-password">Password</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="login-password" type="password" placeholder="Password" v-model="form.password">
            </div>
          </div>
          <div class="mt-3">
            <button type="submit"
              class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Login</button>
            <small class="ml-2 text-zinc-400">
              <NuxtLink to="/register" class="text-green-500 hover:text-green-700">Register</NuxtLink>
              or
              <NuxtLink to="/join" class="text-green-500 hover:text-green-700">join a workspace</NuxtLink>.</small>
          </div>
        </form>
        <div v-show="showError" class="w-full flex justify-center">
          <ErrorMessage :error-message="errorMessage"></ErrorMessage>
        </div>
      </div>
    </div>
  </div>  
</template>

<script lang="ts">

import { useFetchAuth } from "~~/methods/useFetchAuth";
import { useToken } from "~~/methods/useToken";

import { PostTokenResponse } from "~~/types/PostTokenResponse";
import { GetUserResponse} from "~~/types/GetUserResponse";

export default {
  data() {
    return {
      form: {
        username: "",
        password: ""
      },
      showError: false, 
      errorMessage: "Login failed. Try again!"
    };
  },
  methods: {
    async login() {

      useToken().deleteTokenCookie();

      const loginBody = new FormData();
      loginBody.append("username", this.form.username);
      loginBody.append("password", this.form.password);

      const data = await $fetch(
        `${this.config.public.backendUrlBase}/token`,{ method: 'POST',
        body: loginBody }
        ).then((data:PostTokenResponse) => {
          
          useToken().setTokenCookie(data.access_token);

        }).catch((error) => {
          console.log(error);
          this.errorMessage = error.data.detail;
          this.showError = true;
          });

      const token:string = useToken().getToken();

      //if token is defined, get user information by updating user state and navigate to workspace
      if(token != undefined) {

        const getUserWorkspace = await useFetchAuth(
        '/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
          navigateTo({ path: "/"+`${data.workspaces[0].name}` });
        }).catch((error) => {
          console.log(error);
          });
      } else {
        this.showError = true;
      }
    }
  }
}
</script>