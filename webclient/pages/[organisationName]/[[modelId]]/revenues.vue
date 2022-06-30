<script setup>
definePageMeta({
  middleware: ["auth", "route-check"]
})
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <h1>Model ID: {{ $route.params.modelId }}</h1>
            <p>Revenues</p>
        </div>
    </NuxtLayout>
</template>