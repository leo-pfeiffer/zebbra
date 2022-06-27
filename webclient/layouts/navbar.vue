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
        <div class="w-48 min-w-[12rem] bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div class="text-sm ml-0.5">
                <span class="px-2 py-1 rounded-md bg-green-500 text-neutral-50 shadow-sm">
                    {{ workspaceName[0] }}
                </span>
                <span class="ml-2 text-zinc-900">
                    {{ workspaceName }}
                </span>
            </div>
            <div class="text-xs my-4">
                <NuxtLink to="/tesla/settings/workspace"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                    <i class="bi bi-gear-fill text-zinc-400"></i><span
                            class="pl-2">Settings</span>
                </div></NuxtLink>
                <NuxtLink to="tesla/settings/integrations"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
                    <i class="bi bi-cloud-fill text-zinc-400"></i><span
                            class="pl-2">Integrations</span>
                </div></NuxtLink>
                <NuxtLink to="/docs"><div class="px-2 hover:bg-zinc-200 py-1.5 rounded text-zinc-500">
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
                    <div v-if="true" class="overflow-auto min-h-[55vh] max-h-[55vh]">
                        <div v-for="model in models">
                            <ModelDropdown :model=model></ModelDropdown>
                        </div>
                    </div>
                    <div v-else>
                        <p class="text-xs mt-2 text-zinc-500">Start by creating your first model.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="absolute bottom-0 left-0 bg-zinc-100 border-r border-zinc-300 w-48 flex justify-center px-3">
            <div class="flex justify-center w-full border-t border-zinc-300 py-3">
                <button @click="useLogout" class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">Logout</button>
            </div>
        </div>
        <div class="flex-grow overflow-y-scroll">
            <slot />
        </div>
    </div>
</template>