<script setup lang="ts">

definePageMeta({
  middleware: ["auth", "route-check"]
})

const model = useDummyModelState();

/* const route = useRoute()
const user = useUserState();

const model = useModelState();
model.value = await updateModelState(route.params.modelId); */

const dates = useState('dates', () => useDateArray(model.value.meta.starting_month));

</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <div class="mt-3 ml-1 py-3 pl-2 mr-0 overflow-x-hidden">
                <div class="flex">
                    <div class="">
                        <div class="flex mb-4">
                            <div class="text-xs text-center font-mono italic py-2 px-2 border-b border border-zinc-300 min-w-[50px] max-w-[50px]">fx</div>
                            <div class="text-xs border-y border-r border-zinc-300 min-w-[325px] max-w-[325px] text-right"><form class="w-full h-full"><input type="text" class="font-mono w-full h-full px-2"></form></div>
                        </div>
                        <ColumnHeader v-for="assumption, index in model.sheets[0].assumptions" :assumption="assumption" :key="index" :assumptionIndex="index"></ColumnHeader>
                    </div>
                    <div class="overflow-x-auto">
                        <div class="flex mb-4">
                            <div class="text-xs py-2 px-2 border-y border-r border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700" v-for="date in dates">{{date}}</div>
                        </div>
                        <GridColumn v-for="assumption in model.sheets[0].assumptions" :assumption="assumption"></GridColumn>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">
export default {
    data() {
        return {
            
        }
    },
    props: {
    },
    methods: {}
}

</script>