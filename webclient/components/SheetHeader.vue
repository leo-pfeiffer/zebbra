<template>
    <div class="relative">
        <span class="inline-block align-middle">
            <div class="">
                <h1 class="font-semibold text-xl inline-block align-middle text-zinc-900">{{sheetName}}</h1>
                <p class="text-xs text-zinc-500">{{ workspaceName }} / {{ modelName }}
                </p>
            </div>
        </span>
    </div>
</template>

<script>
    export default {
        props: {
            sheetName:String,
            workspaceName: String,
            modelName: String,
        },
        
    }
</script>