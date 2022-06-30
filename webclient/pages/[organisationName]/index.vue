<script setup>
    definePageMeta({
        middleware: ["auth", "route-check"]
    })
    const user = useUserState();
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <p>{{ user.workspaces[0] }} Workspace</p>
        </div>
    </NuxtLayout>
</template>