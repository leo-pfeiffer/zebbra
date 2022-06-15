<script>
export default {
  data() {
    return {
      workspaceName: "",
      models: []
    }
  },
  beforeMount() {
    console.log("beforemount")
    this.workspaceName = "Acme"
  }
}
</script>

<template>
    <div class="w-screen h-screen flex">
        <div class="w-48 bg-zinc-100 px-3 py-6">
            <div>
                <span class="px-2 py-1 rounded-md bg-green-500 text-neutral-50">
                    {{ this.workspaceName[0] }}
                </span>
                <span class="ml-2 text-zinc-900">
                    {{ this.workspaceName }}
                </span>
            </div>
            <div class="text-sm mt-4">
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/settings"><i class="bi bi-gear-fill text-zinc-400"></i><span class="pl-3.5 text-zinc-500 hover:text-zinc-600">Settings</span></NuxtLink>
                </div>
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/integrations"><i class="bi bi-cloud-fill text-zinc-400"></i><span class="pl-3.5 text-zinc-500 hover:text-zinc-600">Integrations</span></NuxtLink>
                </div>
                <div class="my-1.5 pl-1.5">
                    <NuxtLink to="/documentation"><i class="bi bi-file-earmark-code-fill text-zinc-400"></i><span class="pl-3.5 text-zinc-500 hover:text-zinc-600">Documentation</span></NuxtLink>
                </div>
            </div>
            <div class="my-6">

                <button class=""><i class="bi bi-plus-lg"></i>Create New Model</button>

            </div>
        </div>
        <div class="flex-grow">
            <slot />
        </div>
    </div>
</template>