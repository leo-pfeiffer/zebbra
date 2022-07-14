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
const date: string[] = modelMeta.value.starting_month.split("-");
const dates = useState('dates', () => useDateArray(new Date(+date[0], +date[1] - 1)));

const assumptionValuesToDisplayState = useState<string[][]>('assumptionValues');

const variableValuesToDisplayState = useState<Map<number, string[][]>>('variableValues');

</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div class="p-3 border-b border-zinc-300 top-0 min-h-[60px] max-h-[60px]">
                <h1 class="font-semibold text-xl inline-block align-middle">Revenues</h1>
            </div>
            <div class="ml-1 py-3 pl-2 mr-0 overflow-x-hidden min-h-[calc(100%-60px)] max-h-[calc(100%-60px)]">
                <div class="flex">
                    <div>
                        <div id="assumptions-headers">
                            <div>
                                <!-- assumption header -->
                                <div
                                    class="mt-12 text-xs text-zinc-500 font-medium uppercase rounded-tl py-2 px-3 min-w-[400px] max-w-[400px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    Assumptions
                                </div>
                            </div>
                            <VariableRowHeader @update-value="updateAssumptionValue"
                                @update-settings="updateAssumptionSettings" @update-name="updateAssumptionName"
                                @delete-variable="deleteAssumption"
                                v-for="(assumption, index) in revenueState.assumptions" :variable="assumption"
                                :variableIndex="index"
                                :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions)"
                                :variableSearchMap="useVariableSearchMap(revenueState.assumptions)" :sectionIndex="0">
                            </VariableRowHeader>
                            <div class="">
                                <!-- add assumption button -->
                                <div
                                    class="text-xs rounded-bl py-2 px-3 min-w-[400px] max-w-[400px] border-zinc-300 border-y border-l">
                                    <button @click="addAssumption" class="text-zinc-500 hover:text-zinc-700 pl-2"><i
                                            class="bi bi-plus-lg mr-1"></i>Add Assumption</button>
                                </div>
                            </div>
                        </div>
                        <div id="model-headers">
                            <div>

                                <div
                                    class="mt-6 text-xs text-zinc-500 font-medium uppercase rounded-tl py-2 px-3 min-w-[400px] max-w-[400px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    Model
                                </div>
                                <div v-for="(section, sectionIndex) in revenueState.sections" :key="sectionIndex">
                                    <div
                                        class="text-xs text-zinc-700 py-2 px-3 min-w-[400px] max-w-[400px] border-zinc-300 border-l border-t">
                                        {{ section.name }}</div>
                                    <VariableRowHeader @update-value="updateVariableValue"
                                        v-for="(variable, index) in section.rows" :variable="variable"
                                        :variable-index="index"
                                        :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions.concat(section.rows))"
                                        :variableSearchMap="useVariableSearchMap(revenueState.assumptions.concat(section.rows))"
                                        :sectionIndex="sectionIndex"></VariableRowHeader>

                                    <VariableRowHeader :variable="section.end_row" :variable-index="0"
                                        :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions.concat(section.rows))"
                                        :variableSearchMap="useVariableSearchMap(revenueState.assumptions.concat(section.rows))">
                                    </VariableRowHeader>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="relative overflow-x-auto">
                        <div id="dates" class="border-zinc-300 flex mb-4 absolute">
                            <div class="first:border-l first:rounded-tl first:rounded-bl text-xs py-2 px-2 border-r border-y border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700"
                                v-for="date in dates">{{ date }}</div>
                        </div>
                        <div id="assumption-values">
                            <div class="flex mt-12">
                                <!-- assumption header empty -->
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <VariableRow v-for="assumptionValues in assumptionValuesToDisplayState"
                                :values="assumptionValues" :round-to="2"></VariableRow>
                            <div class="flex">
                                <!-- add assumption button empty -->
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-y"
                                    v-for="date in dates">X</div>
                            </div>
                        </div>
                        <div id="model-values">
                            <div class="flex mt-6">

                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <div v-for="(section, index) in revenueState.sections" :key="index">
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <VariableRow v-if="variableValuesToDisplayState"
                                    v-for="variableValues in variableValuesToDisplayState.get(index)"
                                    :values="variableValues" :round-to="2"></VariableRow>
                            </div>
                        </div>
                    </div>
                </div>
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
        async addAssumption() {
            const emptyAssumption: Variable = {

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
            } catch (e) {
                console.log(e)
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
            }

        },
        async updateAssumptionValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

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

                    //Update entire sheet
                    var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
                    for (let i = 0; i < this.revenueState.sections.length; i++) {
                        var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                        var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables))
                        valuesOfAssumptionsAndVariables.splice(0, this.revenueState.assumptions.length);
                        variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                    };
                    this.variableValuesToDisplayState = variablesValuesStorage;

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
        async updateVariableValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                for (let [key, value] of timeSeriesMap) {
                    console.log(key + " : " + value)
                }
                console.log(variableIndex);
                console.log(sectionIndex)

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                console.log("storage: " + storageValue)

                this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.revenueState.sections[sectionIndex].rows[variableIndex].value = storageValue.toString();
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                } else {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                }

                try {
                    //update RevenueState
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                    //Update sheet values valuesToDisplay
                    var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
                    for (let i = 0; i < this.revenueState.sections.length; i++) {
                        var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                        var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables))
                        valuesOfAssumptionsAndVariables.splice(0, this.revenueState.assumptions.length);
                        variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                    };
                    this.variableValuesToDisplayState = variablesValuesStorage;
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenue.sections[0].rows[variableIndex].value === this.revenue.sections[0].rows[variableIndex].value)) {
                        this.revenue.value = actualSheet;
                    }
                }
            } else {
                //todo:throw error
            }
        },
        async updateAssumptionName(newName: string, variableIndex: number) {
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
        async updateAssumptionSettings(variableIndex: number, value1Input: string, valTypeInput: string, startingAtInput: number) {

            this.revenueState.assumptions[variableIndex].val_type = valTypeInput;
            this.revenueState.assumptions[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === undefined || value1Input === "" || value1OnlySpaces) {
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
        async deleteAssumption(variableIndex: number) {
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
        isTimeSeries(value: string, timeSeriesMap: Map<string, boolean>) {

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

        var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
        for (let i = 0; i < revenues.value.sections.length; i++) {
            var sectionVariables: Variable[] = [...revenues.value.sections[i].rows];
            var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions.concat(sectionVariables))
            valuesOfAssumptionsAndVariables.splice(0, revenues.value.assumptions.length);
            variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
        };
        useState<Map<number, string[][]>>('variableValues', () => variablesValuesStorage);
    }
}

</script>