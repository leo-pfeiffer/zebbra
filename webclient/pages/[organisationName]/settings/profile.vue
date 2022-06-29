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
            <button type="submit" class="bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-sm font-medium px-2.5 py-1 
                        border border-sky-600 rounded text-neutral-100">
              Update
            </button>
          </form>
          <div v-show="showErrorPersonalInfo" class="w-full flex justify-center">
            <ErrorMessage :error-message="errorMessagePersonalInfo"></ErrorMessage>
          </div>
          <div v-show="showSuccessPersonalInfo" class="w-full flex justify-center">
            <SuccessMessage success-message="Personal Information successfully updated!"></SuccessMessage>
          </div>
        </div>
        <div class="py-6">
          <h2 class="text-xl text-zinc-900 mb-3">Change Password</h2>
          <form @submit.prevent="updatePassword">
            <div class="mb-4">
              <label class="block text-xs font-medium text-zinc-500" for="password">Password</label>
              <div class="mt-1">
                <input required
                  class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                  id="password" type="password" placeholder="Your new password" v-model="user.password">
              </div>
            </div>
            <button type="submit" class="bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-sm font-medium px-2.5 py-1 
                        border border-sky-600 rounded text-neutral-100">
              Change
            </button>
          </form>
          <div v-show="showErrorPassword" class="w-full flex justify-center">
            <ErrorMessage :error-message="errorMessagePassword"></ErrorMessage>
          </div>
          <div v-show="showSuccessPassword" class="w-full flex justify-center">
            <SuccessMessage success-message="Password successfully updated!"></SuccessMessage>
          </div>
        </div>
        <div class="py-6">
          <h2 class="text-xl text-zinc-900 mb-3">Delete Your Account</h2>
          <p class="text-sm text-zinc-500 my-3">With this action you permenantly delete your account. You will not be
            able to undo this. So be very careful here.</p>
          <button @click="toggleDeleteModal" class="bg-red-600  drop-shadow-sm
                        shadow-zinc-50 text-sm font-medium px-2.5 py-1 
                        border border-red-600 rounded text-neutral-100">
            Delete your account
          </button>
          <div v-show="showErrorDeleteAccount" class="w-full flex justify-center">
            <ErrorMessage :error-message="errorMessageDeleteAccount"></ErrorMessage>
          </div>
        </div>
        <div v-show="deleteModalOpen" class="absolute left-0 top-1/3 w-full h-full flex justify-center align-middle">
          <div class="p-3 border h-max shadow bg-white border-zinc-300 rounded">
            <p class="text-zinc-900 text-sm mb-3">Are you sure you want to delete your account?</p>
            <div class="float-right">
              <button
                class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                @click="toggleDeleteModal">Cancel</button>
              <button class="ml-2 bg-red-600  drop-shadow-sm
                          shadow-zinc-50 text-xs font-medium px-2 py-1 
                          border border-red-600 rounded text-neutral-100" @click="deleteAccount">Delete</button>
            </div>
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
        firstName: "",
        lastName: "",
        email: "",
        password: ""
      },
      showErrorPersonalInfo: false,
      showSuccessPersonalInfo: false,
      errorMessagePersonalInfo: "Somthing went wrong. Try again!",
      showErrorPassword: false,
      showSuccessPassword: false,
      errorMessagePassword: "Somthing went wrong. Try again!",
      showErrorDeleteAccount: false,
      errorMessageDeleteAccount: "Somthing went wrong. Try again!",
      deleteModalOpen: false
    };
  },
  async beforeMount() {
    //get user data and pre fill the form
    const data = await useFetchAuth(
        'http://localhost:8000/user',{ method: 'GET'}
        ).then((data) => {
          console.log(data);
          this.user.firstName = data.first_name;
          this.user.lastName = data.last_name;
          this.user.email = data.username;
          
        }).catch((error) => {
          console.log(error);
          });
  },
  methods: {
    async updateUserInformation() {

      //remove error messages so they don't stack up
      this.showErrorPersonalInfo = false;
      this.showSuccessPersonalInfo = false;

      const data = await useFetchAuth(
        'http://localhost:8000/user/update',{ method: 'POST', 
        params: {
          username: this.user.email,
          first_name: this.user.firstName,
          last_name: this.user.lastName
          }}
        ).then((data) => {
          this.user.firstName = data.first_name;
          this.user.lastName = data.last_name;
          this.user.email = data.username;

          this.showSuccessPersonalInfo = true;

        }).catch((error) => {
          console.log(error);
          this.errorMessagePersonalInfo = error.data.detail;
          this.showErrorPersonalInfo = true;
          });

    },
    async updatePassword() {
      
      //remove error messages so they don't stack up
      this.showErrorPassword = false;
      this.showSuccessPassword = false;

      const data = await useFetchAuth(
        'http://localhost:8000/user/update',{ method: 'POST', 
        params: {
          password: this.user.password
          }}
        ).then((data) => {
          console.log(data)
          //show success
          this.showSuccessPassword = true;
        }).catch((error) => {
          console.log(error);
          this.errorMessagePassword = error.data.detail;
          this.showErrorPassword = true;
          });
      
    },
    toggleDeleteModal() {
      if (this.deleteModalOpen === false) {
        this.deleteModalOpen = true;
      } else {
        this.deleteModalOpen = false;
      }

    },
    async deleteAccount() {

      const data = await useFetchAuth(
        'http://localhost:8000/user/delete',{ method: 'POST', 
        }).then((data) => {
          console.log(data)
          useLogout();
          //todo: success message
        }).catch((error) => {
          console.log(error);
          this.errorMessageDeleteAccount = error.data.detail;
          this.showErrorDeleteAccount = true;
          });
    }
  }
}
</script>