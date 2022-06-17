<script>
export default {
    data() {
        return {
            workspaceName: 'Tesla',
            models: [
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
        <div class="w-48 bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div class="text-sm ml-0.5">
                <span class="px-2 py-1 rounded-md bg-green-500 text-neutral-50 shadow-sm">
                    {{ workspaceName[0] }}
                </span>
                <span class="ml-2 text-zinc-900">
                    {{ workspaceName }}
                </span>
            </div>
            <div class="text-xs my-4">
                <NuxtLink to="/settings"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                    <i class="bi bi-gear-fill text-zinc-400"></i><span
                            class="pl-2">Settings</span>
                </div></NuxtLink>
                <NuxtLink to="/settings"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                    <i class="bi bi-cloud-fill text-zinc-400"></i><span
                            class="pl-2">Integrations</span>
                </div></NuxtLink>
                <NuxtLink to="/settings"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                    <i class="bi bi-file-earmark-code-fill text-zinc-400"></i><span
                            class="pl-2">Documentation</span>
                </div></NuxtLink>
            </div>
            <div class="my-4 flex justify-center w-full">

                <button
                    class=" bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs pl-2.5 pr-3 py-1 border border-zinc-300 rounded text-zinc-700"><i
                        class="bi bi-bar-chart-fill mr-1"></i>Create New Model</button>

            </div>
            <div class="pb-3">
                <div>
                    <span class="text-xs text-zinc-500">Your Models</span>
                    <div v-if="true" class="overflow-auto min-h-[50vh] max-h-[50vh]">
                        <div v-for="model in models">
                            <ModelDropdown :model=model></ModelDropdown>
                        </div>
                    </div>
                    <div v-else>
                        <p class="text-xs mt-2 text-zinc-500">Start by creating your first model.</p>
                    </div>
                </div>
            </div>
            <div class="w-full flex justify-center border-t py-3 border-zinc-300">
                <button @click="useLogout" class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Logout</button>
            </div>
        </div>
        <div class="flex-grow">
            <slot />
        </div>
    </div>
</template>