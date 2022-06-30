<script>
export default {
    data() {
        return {}
    },
    props: {
        successMessage: String
    }
}
</script>

<template>

    <div class="w-max static mt-5 py-2 px-3 border border-green-400 rounded shadow-sm shadow-green-100 text-xs text-green-600 text-center" ><i class="bi bi-check-square-fill mr-2"></i>{{ successMessage }}</div>

</template>