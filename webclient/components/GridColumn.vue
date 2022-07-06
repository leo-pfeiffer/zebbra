<template>
    <div class="flex">
        <div class="flex">
            <div class="text-xs py-2 px-2 border-t border-r border-zinc-300 min-w-[75px] max-w-[75px] h-full text-right" v-for="value in values">{{value}}</div>
            <!-- <div class="text-xs py-2 px-2 border-t border-r border-zinc-300 min-w-[75px] max-w-[75px] h-full text-right">{{assumption.timeSeries}}</div> -->
        </div>
    </div>
</template>

<script lang="ts">

export default {
    data() {
        return {
        }
    },
    props: {
        values: Object as () => string[],
    }
}
</script>