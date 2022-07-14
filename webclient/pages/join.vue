<script setup>

const config = useRuntimeConfig();

</script>

<template>
  <div class="container flex justify-center mx-auto">
    <div class="w-1/2 md:w-1/4">
      <div>
        <h1 class="text-2xl mb-4 mt-16 text-zinc-900 font-semibold">Join Workspace</h1>
      </div>
      <div class="w-full">
        <form @submit.prevent="join">
          <div>
            <label class="block text-xs font-medium text-zinc-500" for="join-first-name">First Name</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="join-first-name" type="text" placeholder="Elon" v-model="form.first_name">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="join-last-name">Last Name</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="join-last-name" type="text" placeholder="Musk" v-model="form.last_name">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="join-email">Email</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="join-email" type="email" placeholder="elon@spacex.com" v-model="form.username">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="join-password">Password</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="join-password" type="password" placeholder="Password" v-model="form.password">
            </div>
          </div>
          <div class="my-3 border-t border-zinc-300"></div>
          <div class="">
            <label class="block text-xs font-medium text-zinc-500" for="join-invite-code">Invite Code</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="join-invite-code" type="text" placeholder="Your Invite Code" v-model="form.invite_code">
            </div>
          </div>
          <div class="mt-3">
            <button type="submit"
              class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Join</button>
            <small class="ml-2 text-zinc-400">
              <NuxtLink to="/login" class="text-green-500 hover:text-green-700">Login</NuxtLink>
              or
              <NuxtLink to="/register" class="text-green-500 hover:text-green-700">register</NuxtLink>.</small>
          </div>
        </form>
        <div v-show="showError" class="w-full flex justify-center">
          <ErrorMessage :error-message="errorMessage"></ErrorMessage>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        first_name: "",
        last_name: "",
        invite_code: "",
        password: ""
      },
      showError: false,
      errorMessage: "Registration failed. Try again!"  
    };
  },
  methods: {
    async join() {
      
      const data = await $fetch(
        `${this.config.public.backendUrlBase}/register`, {
          method: 'POST',
          body: this.form
        }
      ).then(() => {
        navigateTo({ path: '/login' })
      
      }).catch((error) => {
        this.errorMessage = error.data.detail;
        this.showError = true;
      });
    }
  }
}
</script>