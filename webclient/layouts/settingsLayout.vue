<script>
export default {
    data() {
        
    }
}
</script>

<template>
    <div class="w-screen h-screen flex">
        <div class="w-48 bg-zinc-100 px-3 py-4 border-r border-zinc-300 overflow-hidden">
            <div class="text-sm flex align-middle">
                <NuxtLink to="/tesla"><div class="text-zinc-400 py-1 px-1.5 hover:bg-zinc-200 hover:text-zinc-500 rounded-md hover:shadow-sm">
                    <i class="bi bi-arrow-up-left"></i>
                </div></NuxtLink>
                <div class="ml-1.5 text-zinc-900 font-medium text-lg">Settings</div>
            </div>
            <div class="text-xs pl-2 mt-8">
                <div class="text-zinc-500 text-semibold"><i class="bi bi-house-door-fill mr-2"></i>Workspace</div>
                <div class="mt-1.5">
                    <NuxtLink to="/settings/workspace"><div class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">General</div></NuxtLink>
                    <NuxtLink to="/settings/workspace/members"><div class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">Members</div></NuxtLink>
                    <NuxtLink to="/settings/workspace/integrations"><div class="text-xs text-zinc-700 py-1 pl-5 hover:bg-zinc-200 rounded">Integrations</div></NuxtLink>
                </div>
            </div>
            <div class="text-xs pl-2 mt-6">
                <div class="text-zinc-500 text-semibold"><i class="bi bi-person-fill mr-2"></i>Profile</div>
            </div>
        </div>
        <div class="flex-grow">
            <slot />
        </div>
    </div>
</template>