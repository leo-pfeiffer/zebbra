<template>

    <div class="sticky top-0 rounded-b min-w-fit z-50">
        <table class="text-left min-w-fit">
            <th class="font-medium border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-[10px] text-zinc-500">VARIABLE</th>
            <tr class="border bg-white border-zinc-300 shadow-md text-left" v-for="[key, value] in variableSearch" :key="key">
            <div class="min-w-fit flex align-middle justify-start py-2 px-2">
                <div>
                    <button class="text-left mr-1" @click="$emit('searchClick', key, searchTimeDiff)">
                        {{ value }}
                    </button>
                </div>
                <div class="flex align-middle py-auto ">
                    <select v-model="searchTimeDiff" class="bg-transparent font-medium italic text-zinc-500 rounded text-[10px] bg-zinc-100 mr-1">
                        <option selected>current</option>
                        <option>previous</option>
                        <option>T-2</option>
                        <option>T-12</option>
                    </select>
                </div>
            </div>
            </tr>
        </table>
    </div>

</template>

<script lang="ts">

export default {
    data() {
        return {
            searchTimeDiff: "current"
        }
    },
    props: {
        variableSearch: Map<string, string>
    }
}

</script>