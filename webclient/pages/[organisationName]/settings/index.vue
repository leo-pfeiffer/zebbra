<script setup>
    definePageMeta({
        middleware: ["auth"]
    })
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div>
            <p>Settings</p>
        </div>
    </NuxtLayout>
</template>