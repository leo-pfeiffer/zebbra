<script setup lang="ts">
import { Section, Variable } from '~~/types/Model';
import { useVariableSearchMap } from '~~/methods/useVariableSearchMap';
import { useVariableTimeSeriesMap } from '~~/methods/useVariableTimeSeriesMap';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { useGetPossibleIntegrationValues } from '~~/methods/useGetPossibleIntegrationValues';

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
const endRowValuesToDisplayState = useState<string[][]>('endRowValues');

const possibleIntegrationValuesState = usePossibleIntegrationValuesState();
possibleIntegrationValuesState.value = await useGetPossibleIntegrationValues(route.params.modelId);

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
                                    class="mt-12 text-xs text-zinc-500 font-medium uppercase rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    Assumptions
                                </div>
                            </div>
                            <VariableRowHeader @update-value="updateAssumptionValue"
                                @update-settings="updateAssumptionSettings" @update-name="updateAssumptionName"
                                @delete-variable="deleteAssumption"
                                v-for="(assumption, index) in revenueState.assumptions" :variable="assumption"
                                :variableIndex="index"
                                :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions)"
                                :variableSearchMap="useVariableSearchMap(revenueState.assumptions)" :sectionIndex="0"
                                :isEndRow="false"
                                :showIntegration="false">
                            </VariableRowHeader>
                            <div class="">
                                <!-- add assumption button -->
                                <div
                                    class="text-xs rounded-bl py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-y border-l">
                                    <button @click="addAssumption" class="text-zinc-400 italic hover:text-zinc-500"><i
                                            class="bi bi-plus-lg mr-3"></i>Add Assumption</button>
                                </div>
                            </div>
                        </div>
                        <div id="model-headers">
                            <div>

                                <div class="group flex mt-6 text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    <span class="font-medium uppercase">
                                        Model
                                    </span>
                                </div>
                                <div v-for="(section, sectionIndex) in revenueState.sections" :key="sectionIndex">
                                    <SectionHeader :sectionName="section.name" :sectionIndex="sectionIndex"
                                    @change-section-name="updateSectionName"
                                    @delete-section="deleteSection"></SectionHeader>
                                    <VariableRowHeader @update-value="updateVariableValue"
                                        @update-settings="updateVariableSettings" @update-name="updateVariableName"
                                        @delete-variable="deleteVariable"
                                        @update-integration="updateIntegrationValue"
                                        v-for="(variable, index) in section.rows"
                                        :variable="variable" :variable-index="index"
                                        :timeSeriesMap="useVariableTimeSeriesMap(revenueState.assumptions.concat(section.rows))"
                                        :variableSearchMap="useVariableSearchMap(revenueState.assumptions.concat(section.rows))"
                                        :sectionIndex="sectionIndex" :isEndRow="false"
                                        :showIntegration="true"
                                        :possible-integration-values="possibleIntegrationValuesState"></VariableRowHeader>
                                    <div
                                        class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                        <button @click="addVariable(sectionIndex)"
                                            class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-3"></i>Add Variable</button>
                                    </div>

                                    <VariableRowHeader @update-value="updateEndRowValue"
                                        :variable="section.end_row" :variable-index="0"
                                        :timeSeriesMap="useVariableTimeSeriesMap(section.rows)"
                                        :variableSearchMap="useVariableSearchMap(section.rows)"
                                        :sectionIndex="sectionIndex"
                                        :sectionName="section.name"
                                        :isEndRow="true">
                                    </VariableRowHeader>
                                </div>
                                <div class="">
                                    <!-- add section button -->
                                    <div
                                        class="text-xs py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-y border-l">
                                        <button @click="addSection" class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-2"></i>Add Section</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div>
                                <div class="group flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-50 border-zinc-300 border">
                                    <span class="font-medium uppercase">
                                        Total Revenues
                                    </span>
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
                                <div class="flex">
                                    <!-- add variable button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <VariableRow v-if="endRowValuesToDisplayState"
                                        :values="endRowValuesToDisplayState[index]" :round-to="2"></VariableRow>
                            </div>
                            <div class="flex">
                                    <!-- add section button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-y"
                                        v-for="date in dates">X</div>
                                </div>
                        </div>
                        <div id="total-revenue-values" class="border-zinc-300">
                            <VariableRow v-if="endRowValuesToDisplayState" :values="totalRevenuesToDisplay" :round-to="2" :isFinalRow="true"></VariableRow>
                        </div>
                    </div>
                </div>
            </div>
            <SheetErrorMessages v-if="(errorMessages.length > 0)" :errorMessages="errorMessages" @close="closeErrorMessage"></SheetErrorMessages>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">

import { useFormulaParser } from '~~/methods/useFormulaParser';
import { useGetValueFromHumanReadable } from '~~/methods/useGetValueFromHumanReadable';
import { useMathParser } from '~~/methods/useMathParser';
import { useFetchAuth } from '~~/methods/useFetchAuth';
export default {
    data() {
        return {
            errorMessages: []
        }
    },
    computed: {
        totalRevenuesToDisplay() {
            var returnArray:string[] = [];

            if(this.endRowValuesToDisplayState.length > 0) {

                //populate array with all calculation to perform
                var calcArray:string[] = [];
                
                for(let i=0; i < 24; i++) {
                    calcArray.push("");
                }

                for(let i=0; i < this.endRowValuesToDisplayState.length; i++) {
                    for(let j=0; j < this.endRowValuesToDisplayState[i].length; j++) {
                        if(this.endRowValuesToDisplayState[i][j] != "–") {
                            calcArray[j] = calcArray[j] + "+" + this.endRowValuesToDisplayState[i][j];
                        }
                    }
                }

                for(let i=0; i < calcArray.length; i++) {
                    try {
                        returnArray.push(useMathParser(calcArray[i]).toString());
                    } catch(e) {
                        if(this.endRowValuesToDisplayState.length === 1) {
                            returnArray.push(this.endRowValuesToDisplayState[0][i]);
                        } else {
                            returnArray.push("#REF!");
                        }
                    }
                }

                return returnArray;

            } else {
                for(let i=0; i < 24; i++) {
                    returnArray.push("–")
                }
                return returnArray;
            }
        }

    },
    methods: {
        closeErrorMessage(index:number){
            this.errorMessages.splice(index, 1)
        },
        async addSection() {

            const emptyVariable: Variable = {

                _id: undefined,
                name: "",
                val_type: "number",
                editable: true,
                decimal_places: 0,
                var_type: "value",
                time_series: false,
                starting_at: 0,
                first_value_diff: false,
                value: "0",
                value_1: undefined,
                integration_name: undefined,
                integration_values: undefined

            }

            const emptyEndRow: Variable = {

                _id: undefined,
                name: "",
                val_type: "number",
                editable: true,
                decimal_places: 0,
                var_type: "value",
                time_series: true,
                starting_at: 0,
                first_value_diff: false,
                value: "0",
                value_1: undefined,
                integration_name: undefined,
                integration_values: undefined

            }

            const emptySection: Section = {
                name: "New Section",
                rows: [emptyVariable],
                end_row: emptyEndRow
            }

            this.revenueState.sections.push(emptySection);

            this.updateDisplayedValues();

            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the section again.");
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
                this.updateDisplayedValues();
            }

        },
        async addAssumption() {
            const emptyAssumption: Variable = {

                _id: undefined,
                name: "",
                val_type: "number",
                editable: true,
                decimal_places: 0,
                var_type: "value",
                time_series: false,
                starting_at: 0,
                first_value_diff: false,
                value: "0",
                value_1: undefined,
                integration_name: undefined,
                integration_values: undefined

            }

            this.revenueState.assumptions.push(emptyAssumption);

            const assumptionValuesArrayState = useState<string[][]>('assumptionValues');
            var assumptionValuesArray: string[][];

            try {
                assumptionValuesArray = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);
                let index = assumptionValuesArray.length - 1;
                assumptionValuesArrayState.value.push(assumptionValuesArray[index])
            } catch(e){
                console.log(e);
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
            } 

            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
            }

        },
        async addVariable(sectionIndex: number) {
            const emptyVariable: Variable = {

                _id: undefined,
                name: "",
                val_type: "number",
                editable: true,
                decimal_places: 0,
                var_type: "value",
                time_series: false,
                starting_at: 0,
                first_value_diff: false,
                value: "0",
                value_1: undefined,
                integration_name: undefined,
                integration_values: undefined

            }

            this.revenueState.sections[sectionIndex].rows.push(emptyVariable);
            this.updateDisplayedValues();

            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
                this.updateDisplayedValues();
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
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(actualSheet.assumptions[variableIndex].value === this.revenue.assumptions[variableIndex].value)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateVariableValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

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
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.revenueState.sections[0].rows[variableIndex].value)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateIntegrationValue(integrationSelected: string, variableIndex: number, sectionIndex: number) {
            if(integrationSelected != "None") {
                this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_name = integrationSelected;
            } else {
                //todo: check if formula or value
                this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_name = undefined;
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_values = undefined;
            }

            try {
                //update RevenueState
                this.revenueState = await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                this.updateDisplayedValues();

            } catch (e) {
                console.log(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[0].rows[variableIndex].integration_name === this.revenueState.sections[0].rows[variableIndex].integration_name) ||
                    !(actualSheet.sections[0].rows[variableIndex].var_type === this.revenueState.sections[0].rows[variableIndex].var_type)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async updateEndRowValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.revenueState.sections[sectionIndex].end_row.time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.revenueState.sections[sectionIndex].end_row.value = storageValue.toString();
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.revenueState.sections[sectionIndex].end_row.var_type = "formula";
                } else {
                    this.revenueState.sections[sectionIndex].end_row.var_type = "value";
                }

                try {
                    //update RevenueState
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.revenueState.sections[0].rows[variableIndex].value)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateAssumptionName(newName: string, variableIndex: number, sectionIndex: number) {
            if (newName.length > 0 && !useFormulaParser().charIsNumerical(newName[0])) {
                this.revenueState.assumptions[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenueState.assumptions[variableIndex].name === actualSheet.assumptions[variableIndex].name)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("A variable name must be longer than 0 and can't start with a number.");
            }
        },
        async updateSectionName(sectionIndex: number, newName: string) {
            if (newName.length > 0) {
                this.revenueState.sections[sectionIndex].name = newName;
                try {
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenueState.sections[sectionIndex].name === actualSheet.sections[sectionIndex].name)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("The section name must be at least one character.");
            }
        },
        async updateVariableName(newName: string, variableIndex: number, sectionIndex: number) {
            if (newName.length > 0 && !useFormulaParser().charIsNumerical(newName[0])) {
                this.revenueState.sections[sectionIndex].rows[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(this.revenueState.sections[sectionIndex].rows[variableIndex].name === actualSheet.sections[sectionIndex].rows[variableIndex].name)) {
                        this.revenueState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("A variable name must be longer than 0 and can't start with a number.");
            }
        },
        async updateAssumptionSettings(variableIndex: number, value1Input: string, valTypeInput: string, startingAtInput: number, sectionIndex: number) {

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
                this.updateDisplayedValues();
            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(this.actualSheet.assumptions[variableIndex].value === this.revenueState.assumptions[variableIndex].value)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async updateVariableSettings(variableIndex: number, value1Input: string, valTypeInput: string, startingAtInput: number, sectionIndex: number) {
            
            this.revenueState.sections[sectionIndex].rows[variableIndex].val_type = valTypeInput;
            this.revenueState.sections[sectionIndex].rows[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.revenueState.sections[sectionIndex].rows[variableIndex].value_1 = undefined;
                this.revenueState.sections[sectionIndex].rows[variableIndex].first_value_diff = false;
            } else {
                this.revenueState.sections[sectionIndex].rows[variableIndex].first_value_diff = true;
            }
            this.revenueState.sections[sectionIndex].rows[variableIndex].starting_at = startingAtInput;

            try {
                //update RevenueState
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                //Update sheet values valuesToDisplay
                this.updateDisplayedValues();

            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows[variableIndex].value === this.revenueState.sections[sectionIndex].rows[variableIndex].value)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async deleteAssumption(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.revenueState.assumptions.splice(variableIndex, 1);
            this.assumptionValuesToDisplayState.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions.length === this.revenueState.assumptions.length)) {
                    this.revenueState = actualSheet;
                    this.updateDisplayedValues();
                }
            }
        },
        async deleteSection(sectionIndex: number) {
            //first directly change the state
            this.revenueState.sections.splice(sectionIndex, 1)
            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
                this.updateDisplayedValues();
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.revenueState.sections[sectionIndex].rows.length)) {
                    this.revenueState = actualSheet;
                    this.updateDisplayedValues();
                }
            }
        },
        async deleteVariable(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.revenueState.sections[sectionIndex].rows.splice(variableIndex, 1);
            this.variableValuesToDisplayState.get(sectionIndex).splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.revenueState.sections[sectionIndex].rows.length)) {
                    this.revenueState = actualSheet;
                    this.updateDisplayedValues();
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
        },
        updateDisplayedValues() {
            
            //assumptions
            try {
                this.assumptionValuesToDisplayState = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);

                //Update entire sheet
                var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
                var endRowValuesStorage: string[][] = [];
                for (let i = 0; i < this.revenueState.sections.length; i++) {
                    //variables
                    var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                    var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables))
                    valuesOfAssumptionsAndVariables.splice(0, this.revenueState.assumptions.length);
                    variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                    //endrow
                    var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables.concat(this.revenueState.sections[i].end_row)));
                    valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.revenueState.assumptions.length);
                    endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);

                };
                this.variableValuesToDisplayState = variablesValuesStorage;
                this.endRowValuesToDisplayState = endRowValuesStorage;

            } catch(e) {
                console.log(e);
                this.errorMessages.push(e)
            }
        }
    },
    mounted() {
        try {
            //return the display values for all the assumptions
            const revenues = useRevenueState();
            
            var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions);
            useState('assumptionValues', () => assumptionValuesArray);
            
            var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
            var endRowValuesStorage: string[][] = [];
            for (let i = 0; i < revenues.value.sections.length; i++) {
                //variables
                var sectionVariables: Variable[] = [...revenues.value.sections[i].rows];
                var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions.concat(sectionVariables))
                valuesOfAssumptionsAndVariables.splice(0, revenues.value.assumptions.length);
                variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                //endrow
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(revenues.value.assumptions.concat(sectionVariables.concat(revenues.value.sections[i].end_row)));
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + revenues.value.assumptions.length);
                endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);
            };

            useState<Map<number, string[][]>>('variableValues', () => variablesValuesStorage);
            useState<string[][]>('endRowValues', () => endRowValuesStorage);

        } catch(e) {
            console.log(e);
            this.errorMessages.push(e)
        }
    }
}

</script>