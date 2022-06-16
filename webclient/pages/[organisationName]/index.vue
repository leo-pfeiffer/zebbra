<script setup>
    definePageMeta({
        middleware: ["auth"]
    })
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <p>{{ $route.params.organisationName }} Workspace</p>
        </div>
    </NuxtLayout>
</template>