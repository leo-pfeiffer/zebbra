<template>
    <div class="flex">
        
        <div class="flex">
            <div class="text-xs py-2 px-2 border-b border-r border-zinc-300 min-w-[75px] max-w-[75px] text-right" v-for="index in 24" :key="index">{{index}}</div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
        }
    },
    props: {
    },
    methods: {},
}

</script>