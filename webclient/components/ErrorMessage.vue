<script>
export default {
    data() {
        return {}
    },
    props: {
        errorMessage: String
    }
}

</script>

<template>

<div class="w-max static mt-5 py-2 px-3 border border-red-300 rounded shadow-sm shadow-red-100 text-xs text-red-500 text-center" ><i class="bi bi-exclamation-triangle-fill mr-2"></i>{{ errorMessage }} </div>

</template>