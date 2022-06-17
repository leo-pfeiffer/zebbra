<script setup>
    definePageMeta({
        middleware: ["auth"]
    })
</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <p>Settings</p>
        </div>
    </NuxtLayout>
</template>