<script setup lang="ts">
import { Sheet, Variable } from '~~/types/Model';
import { useVariableSearchMap } from '~~/methods/useVariableSearchMap';
import { useVariableTimeSeriesMap } from '~~/methods/useVariableTimeSeriesMap';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';

definePageMeta({
    middleware: ["auth", "route-check"]
})

const route = useRoute()

const modelMeta = useModelMetaState();

modelMeta.value = await getModelMeta(route.params.modelId);

const revenueState = useRevenueState();
revenueState.value = await useSheetUpdate().getRevenueSheet(route.params.modelId);

//todo: find better solution
const date:string[] = modelMeta.value.starting_month.split("-");
const dates = useState('dates', () => useDateArray(new Date(+date[0], +date[1]-1)));

const assumptionValuesToDisplayState = useState<string[][]>('assumptionValues');


</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div class="mt-3 ml-1 py-3 pl-2 mr-0 h-full overflow-x-hidden">
                <div class="flex border-b border-zinc-300">
                    <div>
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
                        <VariableRowHeader @update-value="updateAssumptionValue" @update-settings="updateAssumptionSettings" @update-name="updateAssumptionName" @delete-variable="deleteAssumption" v-for="(assumption, index) in revenueState.assumptions" :variable="assumption" :variableIndex="index" :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions)" :variableSearchMap="useVariableSearchMap(revenueState.assumptions)"></VariableRowHeader>
                    </div>
                    <div class="overflow-x-auto">
                        <div class="flex mb-4">
                            <div class="text-xs py-2 px-2 border-y border-r border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700"
                                v-for="date in dates">{{ date }}</div>
                        </div>
                        <VariableRow v-for="assumptionValues in assumptionValuesToDisplayState" :values="assumptionValues" :round-to="2"></VariableRow>
                    </div>
                </div>
                <div class="mt-2"><button class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs pl-2.5 pr-3 py-1 border border-zinc-300 rounded text-zinc-700" @click="addAssumption">Add Assumption</button></div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">

import { useFormulaParser } from '~~/methods/useFormulaParser';
import { useGetValueFromHumanReadable } from '~~/methods/useGetValueFromHumanReadable';

export default {
    data() {
        return {
        }
    },
    methods: {
        async addAssumption(){
            const emptyAssumption:Variable = {

                _id: undefined,
                name: "",
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

            this.revenueState.assumptions.push(emptyAssumption);

            const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
            var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);
            let index = assumptionValuesArray.length - 1;
            assumptionValuesArrayState.value.push(assumptionValuesArray[index])

            //todo: proper error handling
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch(e) {
                console.log(e)
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
            }

        },
        async updateAssumptionValue(humanReadableInputValue:string, variableId:string, variableSearchMap:Map<string, string>, timeSeriesMap:Map<string, boolean>, variableIndex:number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue:string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.revenueState.assumptions[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.revenueState.assumptions[variableIndex].value = storageValue.toString();
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.revenueState.assumptions[variableIndex].var_type = "formula";
                } else {
                    this.revenueState.assumptions[variableIndex].var_type = "value";
                }

                try {
                    //update RevenueState
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                    //Update sheet values valuesToDisplay
                    this.assumptionValuesToDisplayState = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenue.assumptions[variableIndex].value === this.revenue.assumptions[variableIndex].value)) {
                        this.revenue.value = actualSheet;
                    }
                }
            } else {
                //todo:throw error
            }
        },
        async updateAssumptionName(newName:string, variableIndex:number) {
            //todo: proper error handling
            if (newName.length > 0) {
                const sheet = useRevenueState();
                sheet.value.assumptions[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenue.assumptions[variableIndex].value === this.revenue.assumptions[variableIndex].value)) {
                        this.revenue.value = actualSheet;
                    }
                }
            }
        },
        async updateAssumptionSettings(variableIndex:number, value1Input:string, valTypeInput:string, startingAtInput:number) {

            this.revenueState.assumptions[variableIndex].val_type = valTypeInput;
            this.revenueState.assumptions[variableIndex].value_1 = value1Input;

            var value1OnlySpaces:boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch(e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if(value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.revenueState.assumptions[variableIndex].value_1 = undefined;
                this.revenueState.assumptions[variableIndex].first_value_diff = false;
            } else {
                this.revenueState.assumptions[variableIndex].first_value_diff = true;
            }
            this.revenueState.assumptions[variableIndex].starting_at = startingAtInput;

            try {
                //update RevenueState
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                //Update sheet values valuesToDisplay
                this.assumptionValuesToDisplayState = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);
            } catch (e) {
                console.log(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(this.revenue.assumptions[variableIndex].value === this.revenue.assumptions[variableIndex].value)) {
                    this.revenue.value = actualSheet;
                }
            }
        },
        async deleteAssumption(variableIndex:number) {
            //first directly change the state
            this.revenueState.assumptions.splice(variableIndex, 1);
            this.assumptionValuesToDisplayState.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions.length === this.revenueState.assumptions.length)) {
                    this.revenueState = actualSheet;
                    var actualAssumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(actualSheet.assumptions);
                    let index = actualAssumptionValuesArray.length - 1;
                    this.assumptionValuesToDisplayState.push(actualAssumptionValuesArray[index])
                }
            }
        },
        isTimeSeries(value: string, timeSeriesMap:Map<string, boolean>) {
        
            if (value.includes("$")) {
                return true;
            } else if (value.includes("#") && !value.includes("$")) {

                //create an array with all the refs in a variable string
                var refsArray: string[] = [];

                for (let i = 0; i < value.length; i++) {
                    let char = value[i];
                    if (char === "#") {
                        var ref: string = ""; //empty string to store id (ie number after the #)
                        var counter = 1;
                        //only getting the numerical because only the ids are needed not the point in time (e.g. t-1)
                        while (useFormulaParser().charIsNumerical(value[i + counter]) && (value[i + counter] != undefined)) {
                            ref = ref + value[i + counter];
                            counter++;
                            if ((i + counter >= value.length)) {
                                break;
                            }
                        }
                        refsArray.push(ref);
                        i = i + counter - 1;
                    }
                }

                //for every ref check timeSeriesMap and return true if one is timeseries
                for (let i = 0; i < refsArray.length; i++) {
                    if (timeSeriesMap.get(refsArray[i])) {
                        return true;
                    }
                }
                return false;

            } else {
                return false;
            }
        }
    },
    mounted() {
        //return the display values for all the assumptions
        const revenues = useRevenueState();

        //todo not only assumptions but all variables
        var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions);
        useState('assumptionValues', () => assumptionValuesArray);

    }
}

</script>