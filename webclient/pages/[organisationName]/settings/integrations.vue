<script setup>
definePageMeta({
  middleware: ["auth", "route-check"]
})
</script>

<template>
    <NuxtLayout name="settings-layout">
        <div>
            <p>Integrations</p>
        </div>
    </NuxtLayout>
</template>