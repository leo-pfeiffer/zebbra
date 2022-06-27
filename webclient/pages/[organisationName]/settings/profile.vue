<script setup>
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div class="container">
            <div class="mt-8 px-4 sm:px-[20%] lg:px-[25%]">
                <h1 class="text-2xl my-1 font-medium text-zinc-900">Profile</h1>
                <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage your account here</p>
                <div class="py-6">
                    <h2 class="text-xl text-zinc-900 mb-3">Personal Information</h2>
                    <form @submit.prevent="updateUserInformation">
                        <div class="mb-4">
                            <label class="block text-xs font-medium text-zinc-500" for="first-name">First Name</label>
                            <div class="mt-1">
                            <input required
                                class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                                id="first-name" type="text" :placeholder="user.firstName" v-model="user.firstName">
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="block text-xs font-medium text-zinc-500" for="last-name">Last Name</label>
                            <div class="mt-1">
                            <input required
                                class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                                id="last-name" type="text" :placeholder="user.lastName" v-model="user.lastName">
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="block text-xs font-medium text-zinc-500" for="email">Email</label>
                            <div class="mt-1">
                            <input required
                                class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                                id="email" type="email" :placeholder="user.email" v-model="user.email">
                            </div>
                        </div>
                        <button type="submit"
                        class="bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-sm font-medium px-2.5 py-1 
                        border border-sky-600 rounded text-neutral-100">
                        Update
                        </button>
                    </form>
                    <div v-show="showError" class="w-full flex justify-center">
                        <ErrorMessage :error-message="errorMessage"></ErrorMessage>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script>
export default {
  data() {
    return {
      user: {
        firstName: "Patrick",
        lastName: "Schnyder",
        email: "patrick@schnyder.ch"
      },
      showError: false, 
      errorMessage: "Somthing went wrong. Try again!"
    };
  },
  methods: {
    async updateUserInformation() {
      //todo make API call to update names etc and handle error
      console.log("update user info")
    }
  }
}
</script>