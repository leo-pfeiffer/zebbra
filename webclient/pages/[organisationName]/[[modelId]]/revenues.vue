<script setup lang="ts">
import { Sheet, ModelMeta, Variable } from '~~/types/Model';

definePageMeta({
    middleware: ["auth", "route-check"]
})

const route = useRoute()
//const user = useUserState();

const modelMeta = useModelMetaState();

modelMeta.value = await getModelMeta(route.params.modelId);

const revenues = useRevenueState();
revenues.value = await getRevenueState(route.params.modelId);

//todo: find better solution
const date:string[] = modelMeta.value.starting_month.split("-");
const dates = useState('dates', () => useDateArray(new Date(+date[0], +date[1]-1)));

const assumptionValuesToDisplay = useState('assumptionValues');

</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <div class="mt-3 ml-1 py-3 pl-2 mr-0 overflow-x-hidden">
                <div class="flex border-b border-zinc-300">
                    <div class="">
                        <div class="flex mb-4">
                            <div
                                class="text-xs text-center font-mono italic py-2 px-2 border-b border border-zinc-300 min-w-[50px] max-w-[50px]">
                                fx</div>
                            <div
                                class="text-xs border-y border-r border-zinc-300 min-w-[325px] max-w-[325px] text-right">
                                <form class="w-full h-full"><input type="text" class="font-mono w-full h-full px-2">
                                </form>
                            </div>
                        </div>
                        <AssumptionRowHeader v-for="(assumption, index) in revenues.assumptions" :assumption="assumption" :assumptionIndex="index"></AssumptionRowHeader>
                    </div>
                    <div class="overflow-x-auto">
                        <div class="flex mb-4">
                            <div class="text-xs py-2 px-2 border-y border-r border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700"
                                v-for="date in dates">{{ date }}</div>
                        </div>
                        <AssumptionRow v-for="assumptionValues in assumptionValuesToDisplay" :values="assumptionValues"></AssumptionRow>
                    </div>
                </div>
                <div class="mt-2"><button class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs pl-2.5 pr-3 py-1 border border-zinc-300 rounded text-zinc-700" @click="addAssumption">Add Assumption</button></div>
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
    methods: {
        async addAssumption(){

            const emptyAssumption:Variable = {

                _id: undefined,
                name: "New Assumption",
                val_type: "number",
                editable: true,
                var_type: "value",
                time_series: false,
                starting_at: 0,
                first_value_diff: false,
                value: "0",
                value_1: undefined, 
                integration_values: undefined

            }

            const revenues = useRevenueState();
            revenues.value.assumptions.push(emptyAssumption);
            
            const route = useRoute();

            //todo: proper error handling
            try {
                await updateRevenueState(route.params.modelId, revenues.value);
            } catch(e) {
                console.log(e)
                revenues.value = await getRevenueState(route.params.modelId)
            }

        }
    },
    mounted() {

        //return the display values for all the assumptions
        //const model = useDummyModelState();
        const revenues = useRevenueState();

        //todo not only assumptions but all variables
        var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions);
        useState('assumptionValues', () => assumptionValuesArray);
    }
}

</script>