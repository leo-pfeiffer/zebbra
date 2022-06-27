<script setup>
definePageMeta({
  middleware: ["auth"]
})
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div>
            <p>Profile Settings</p>
        </div>
    </NuxtLayout>
</template>