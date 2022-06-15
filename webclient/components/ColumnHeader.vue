<template>
    <div class="flex">
        <div class="text-xs py-2 pl-6 pr-2 border-y border-x border-zinc-300 min-w-[250px] max-w-[250px]">{{ name }}</div>
        <div v-if="selected" class="text-xs border-y border-r border-zinc-300 min-w-[125px] max-w-[125px] text-right"><input class="w-full h-full px-1.5 font-mono font-sm" type=text></div>
        <div @dblclick="selectInput" v-else class="text-xs py-2 px-2 border-y border-r-2 border-zinc-300 min-w-[125px] max-w-[125px] text-right">{{ value }}</div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            selected: false
        }
    },
    props: {
        name: String,
        value: String
    },
    methods: {
        selectInput() {
            if(!selected) {
                selected = true;
            }
        }
    },
}

</script>