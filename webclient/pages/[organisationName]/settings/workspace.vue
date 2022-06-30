<script setup>
definePageMeta({
  middleware: ["auth", "route-check"]
})
</script>

<template>
  <NuxtLayout name="settings-layout">
    <div class="container">
      <div class="mt-8 px-4 sm:px-[20%] lg:px-[25%]">
        <h1 class="text-2xl my-1 font-medium text-zinc-900">Workspace</h1>
        <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage the general workspace settings</p>
        <div class="py-6">
          <h2 class="text-xl text-zinc-900 mb-3">General</h2>
          <form @submit.prevent="updateWorkspaceName">
            <div class="mb-4">
              <label class="block text-xs font-medium text-zinc-500" for="workspace-name-update">Workspace Name</label>
              <div class="mt-1">
                <input required v-bind:disabled="!userIsWorkspaceAdmin"
                  class="w-64 border-zinc-300 border rounded text-sm focus:ring-sky-500 focus:border-sky-500 px-2.5 py-1 placeholder:text-zinc-400"
                  id="workspace-name-update" type="text" :placeholder="workspace.currentName"
                  v-model="workspace.currentName">
              </div>
            </div>
            <button v-show="userIsWorkspaceAdmin" type="submit" class="bg-sky-600  drop-shadow-sm
                        shadow-zinc-50 text-sm font-medium px-2.5 py-1 
                        border border-sky-600 rounded text-neutral-100">
              Update
            </button>
          </form>
          <div v-show="showError" class="w-full flex justify-center">
            <ErrorMessage :error-message="errorMessage"></ErrorMessage>
          </div>
          <div v-show="showSuccess" class="w-full flex justify-center">
            <SuccessMessage success-message="Workspace name successfully updated!"></SuccessMessage>
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
      workspace: {
        currentName: "",
        oldName: "",
      },
      showError: false,
      showSuccess: false,
      errorMessage: "Somthing went wrong. Try again!",
      userIsWorkspaceAdmin: false,
    };
  }, async beforeMount() {
    //check if user is admin
    this.userIsWorkspaceAdmin = await useIsWorkspaceAdmin();

    //get workspace name from userState
    const userState = useUserState();
    this.workspace.oldName = userState.value.workspaces[0];
    this.workspace.currentName = userState.value.workspaces[0];

  },
  methods: {
    async updateWorkspaceName() {

      //remove error messages so they don't stack up
      this.showError = false;
      this.showSuccess = false;

      const data = await useFetchAuth(
        'http://localhost:8000/workspace/rename', {
          method: 'POST',
        params: {
          old_name: this.workspace.oldName,
          new_name: this.workspace.currentName }
      }).then((data) => {
        console.log(data);
        this.workspace.oldName = data.name;
        this.showSuccess = true;

      }).catch((error) => {
        console.log(error);
        this.errorMessage = error.data.detail;
        this.showError = true;
      });
    }
  }
}
</script>