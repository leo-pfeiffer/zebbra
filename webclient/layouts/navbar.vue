<script>
export default {
    data() {
        return {
            workspaceName: 'Tesla',
            items: [
                { name: 'Model S', id: "1" },
                { name: 'Model 3', id: "2" },
                { name: 'Model X', id: "3" }
            ]
    }
}
}
</script>

<template>
    <div class="w-screen h-screen flex">
        <div class="min-w-[12rem] max-w-[12rem]  bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div>
                <span class="px-2 py-1 rounded-md bg-green-500 text-neutral-50 shadow-sm">
                    {{ workspaceName[0] }}
                </span>
                <span class="ml-2 text-zinc-900">
                    {{ workspaceName }}
                </span>
            </div>
            <div class="text-sm my-5">
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/settings"><i class="bi bi-gear-fill text-zinc-400"></i><span
                            class="pl-3.5 text-zinc-500 hover:text-zinc-600">Settings</span></NuxtLink>
                </div>
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/integrations"><i class="bi bi-cloud-fill text-zinc-400"></i><span
                            class="pl-3.5 text-zinc-500 hover:text-zinc-600">Integrations</span></NuxtLink>
                </div>
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/documentation"><i class="bi bi-file-earmark-code-fill text-zinc-400"></i><span
                            class="pl-3.5 text-zinc-500 hover:text-zinc-600">Documentation</span></NuxtLink>
                </div>
            </div>
            <div class="my-6 flex justify-center w-full">

                <button
                    class=" bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded-md text-zinc-700"><i
                        class="bi bi-plus-lg mr-1"></i>Create New Model</button>

            </div>
            <div class="pb-3">
                <div>
                    <span class="text-xs text-zinc-500">YOUR MODELS</span>
                    <div v-if="true" class="overflow-auto min-h-[50vh] max-h-[50vh]">
                        <div v-for="item in items">
                            <ModelDropdown :model=item></ModelDropdown>
                        </div>
                    </div>
                    <div v-else>
                        <p class="text-xs mt-2 text-zinc-500">Start by creating your first model.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-page">
            <slot />
        </div>
    </div>
</template>

<style>

.right-page {
    width: calc(100% - 12rem);
}



</style>