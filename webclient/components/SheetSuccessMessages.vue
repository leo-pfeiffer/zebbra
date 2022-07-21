<template>

    <div class="absolute min-h-fit bottom-6 right-6">
        <div v-for="message, index in successMessages" :key="index"
            class="block max-w-[400px] min-w-[200px] mt-2 py-2 px-3 border border-green-300 rounded shadow-sm shadow-red-200 hover:shadow-md text-xs text-green-500 bg-white">
            <div class="h-full w-full flex z-50">
                <div>{{ message }}</div>
                <div class="ml-2 flex-grow">
                    <button class="text-green-500 hover:text-green-700 float-right" @click="$emit('close', index)"><i
                            class="bi bi-x-lg"></i></button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    data() {
        return {}
    },
    props: {
        successMessages: Array
    }
}
</script>