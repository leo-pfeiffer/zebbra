<script setup>
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div class="container">
            <div class="mt-8 px-4 sm:px-[20%] lg:px-[25%]">
                <h1 class="text-2xl my-1 font-medium text-zinc-900">Members</h1>
                <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage the members within your workspace</p>
                <div class="py-6">
                    
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script>
export default {
  data() {
    return {
      members: {
        name: "Tesla",
      }
    };
  },
  methods: {
    async updateWorkspaceName() {
      //todo make API call to update name and handle error
      console.log("update workspace name")
    }
  }
}
</script>