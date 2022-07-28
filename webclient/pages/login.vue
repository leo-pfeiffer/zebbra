<script setup lang="ts">

const config = useRuntimeConfig();

console.log("setup")
console.log(config);

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
          <div v-show="promptForOtp" class="mt-2">

            <label class="block text-xs font-medium text-zinc-500" for="login-otp">OTP for 2-Factor Authentication</label>
            <div class="mt-1">
              <input
                     class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                     id="login-otp" type="text" placeholder="OTP" v-model="form.otp">
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
import {OtpRequiredResponse} from "~/types/OtpRequiredResponse";

export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
        otp: ""
      },
      showError: false, 
      errorMessage: "Login failed. Try again!",
      promptForOtp: false,
    };
  },
  methods: {
    async checkOtp () {
      const data = await $fetch(
          `${this.$config.public.backendUrlBase}/user/requiresOtp`,{ method: 'GET',
            params: {username: this.form.username}
          }
      ).then((data:OtpRequiredResponse) => {

        if (data.message == "OTP required") {
          console.log("OTP required")
          this.promptForOtp = true;
        } else {
          console.log("OTP not required")
          this.performLogin();
        }
      }).catch((error) => {
        console.log(error);
        this.errorMessage = error.data.detail;
        this.showError = true;
      });
    },

    async login() {

      if (!this.promptForOtp) {
        await this.checkOtp();
      } else {
        await this.performLogin();
      }
    },

    async performLogin() {

      useToken().deleteTokenCookie();

      const loginBody = new FormData();
      loginBody.append("username", this.form.username);
      loginBody.append("password", this.form.password);

      if (this.promptForOtp) {
        loginBody.append("otp", this.form.otp);
      }

      const data = await $fetch(
        `${this.$config.public.backendUrlBase}/token`,{ method: 'POST',
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