<script setup lang="ts">

definePageMeta({
  middleware: ["auth", "route-check"]
})

const user = useUserState();

</script>

<template>
    <NuxtLayout name="settings-layout">
        <div class="container">
            <div class="mt-8 px-2 sm:px-[20%] lg:px-[30%]">
                <button @click=""
                    class="float-right mt-4 bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"><i
                        class="bi bi-plus-lg mr-1"></i>Create New Model</button>
                <h1 class="text-2xl my-1 font-medium text-zinc-900">Your Models</h1>
                <p class="text-sm text-zinc-500 border-b border-zinc-300 pb-5">Manage all your models here
                </p>
                <div class="py-6 px-0.5">
                    <div v-if="user.models.length < 1" class="text-xs text-center text-zinc-500 p-3 rounded border border-zinc-300 bg-zinc-50">
                        <i class="bi bi-layers mr-1"></i>You don't have any models yet. Start with creating a new one.
                    </div>
                    <div v-else>
                        <ModelMenuItem v-for="model in user.models" :modelName="model.name" :modelId="model._id"></ModelMenuItem>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

