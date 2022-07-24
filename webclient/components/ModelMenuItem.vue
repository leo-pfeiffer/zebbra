<script setup>

const user = useUserState();

</script>

<template>
    <div class="my-3 group flex first-letter: align-center rounded border border-zinc-300 p-3 hover:border-sky-500 hover:shadow-md hover:shadow-sky-50">
        <div>
            <span class="text-sm font-medium text-zinc-700">{{ modelName }}</span>
            <span class="ml-1.5 hidden group-hover:inline-block text-zinc-500 hover:text-zinc-700 z-50"><ModelListDropdown :modelId="modelId" :modelName="modelName"></ModelListDropdown></span>
        </div>
        <div class="flex-grow">

        </div>
        <div class="group-hover:inline-block hidden">
            <NuxtLink :to="`/${user.workspaces[0].name}/${modelId}/dashboard`"><span class="text-sm font-medium text-sky-600">--></span></NuxtLink>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        modelName:String,
        modelId:String
    },
}
</script>