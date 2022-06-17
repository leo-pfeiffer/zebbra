<template>
  <div class="container flex justify-center mx-auto">
    <div class="w-1/2 md:w-1/4">
      <div>
        <h1 class="text-2xl mb-4 mt-16 text-zinc-900 font-semibold">Register</h1>
      </div>
      <div class="w-full">
        <form @submit.prevent="register">
          <div>
            <label class="block text-xs font-medium text-zinc-500" for="register-first-name">First Name</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="register-first-name" type="text" placeholder="Elon" v-model="form.first_name">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="register-last-name">Last Name</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="register-last-name" type="text" placeholder="Musk" v-model="form.last_name">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="register-email">Email</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="register-email" type="email" placeholder="elon@spacex.com" v-model="form.username">
            </div>
          </div>
          <div class="mt-2">
            <label class="block text-xs font-medium text-zinc-500" for="register-password">Password</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="register-password" type="password" placeholder="Password" v-model="form.password">
            </div>
          </div>
          <div class="my-3 border-t border-zinc-300"></div>
          <div class="">
            <label class="block text-xs font-medium text-zinc-500" for="register-workspace-name">Name Your Workspace</label>
            <div class="mt-1">
              <input required
                class="w-full border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                id="register-workspace-name" type="text" placeholder="Space X" v-model="workspaceInput">
            </div>
          </div>
          <div class="mt-3">
            <button type="submit"
              class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Register</button>
            <NuxtLink to="/login"><small class="ml-2 text-green-500 hover:text-green-700">or login here.</small>
            </NuxtLink>
          </div>
        </form>
        <div v-show="showError" class="w-full flex justify-center">
          <div class="w-max static mt-5 py-2 px-3 border border-red-300 rounded shadow-sm shadow-red-100 text-xs text-red-500 text-center" ><i class="bi bi-exclamation-triangle-fill mr-2"></i>{{ errorMessage }} </div>
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
        email: "",
        first_name: "",
        last_name: "",
        workspaces: [],
        password: ""
      },
      workspaceInput: "",
      showError: false,
      errorMessage: ""
    };
  },
  methods: {
    async register() {
      
      //add workspace and email to form
      this.form.workspaces.push(this.workspaceInput);
      this.form.email = this.form.username;

      const data = await $fetch(
        'http://localhost:8000/register', {
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


{
    "username": "pat.schnyder96@gmail.com",
    "password": "asdfasdf",
    "first_name": "Patrick",
    "last_name": "Schnyder",
    "workspaces": [
        "Patrick Schnyder"
    ]
}

{
  "username": "jdoe@example.com",
  "email": "jdoe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "workspaces": [
    "ACME Inc.",
    "Boring Co."
  ],
  "password": "secret"
}