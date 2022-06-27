<script setup>
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <h1>Model ID: {{ $route.params.model }}</h1>
            <p>Dashboard</p>
        </div>
    </NuxtLayout>
</template>