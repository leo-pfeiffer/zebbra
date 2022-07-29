<template>
    <div>
        <Teleport to="body">
            <div class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
                <div
                    class="py-3 px-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50 inline-flex items-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg"
                        fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                    </svg>
                    <span class="text-xs font-medium text-zinc-900">{{text}}...</span>
                </div>
            </div>
        </Teleport>
    </div>
</template>

<script>
export default {

    props: {
        text: String
    },

}
</script>