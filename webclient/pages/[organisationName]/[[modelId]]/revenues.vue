<script setup lang="ts">
import { Section, Variable } from '~~/types/Model';
import { useVariableSearchMap } from '~~/methods/useVariableSearchMap';
import { useVariableTimeSeriesMap } from '~~/methods/useVariableTimeSeriesMap';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { useGetPossibleIntegrationValues } from '~~/methods/useGetPossibleIntegrationValues';

definePageMeta({
    middleware: ["auth", "route-check"]
})

const route = useRoute();

const revenueState = useRevenueState();

try{
    revenueState.value = await useSheetUpdate().getRevenueSheet(route.params.modelId);
} catch(error){
    console.log(error);
}

const possibleIntegrationValuesState = usePossibleIntegrationValuesState();

try{
    possibleIntegrationValuesState.value = await useGetPossibleIntegrationValues(route.params.modelId);
} catch(error){
    console.log(error);
}

</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div v-if="!userAndMetaDataLoading" class="py-3 border-b px-3 border-zinc-300 top-0 min-h-[70px] max-h-[70px]">
                <SheetHeader :sheetName="'Revenues'" :workspaceName="piniaUserStore.workspaces[0].name" :modelName="piniaModelMetaStore.name"></SheetHeader>
            </div>
            <div class="ml-1 pl-2 flex top-0 bg-white pt-2 min-h-[50px] max-h-[50px]">
                <div class="min-w-[470px] max-w-[470px]">
                </div>
                <div class="overflow-x-auto no-scrollbar z-10" id="dates" @scroll="stickScroll('dates', 'table-right')">
                    <div class="border-zinc-300 flex">
                        <div class="first:border-l first:rounded-tl first:rounded-bl text-xs py-2 px-2 border-r border-y border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700"
                            v-for="date in dates">{{ date }}</div>
                    </div>
                </div>
            </div>
            <div class="ml-1 pb-3 pl-2 mr-0 overflow-x-hidden min-h-[calc(100%-120px)] max-h-[calc(100%-120px)]">
                <div class="flex">
                    <div>
                        <div id="assumptions-headers">
                            <div>
                                <!-- assumption header -->
                                <div
                                    class="text-xs text-zinc-500 font-medium uppercase rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
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
                                :showIntegration="false"
                                :userIsViewer="userIsViewer">
                            </VariableRowHeader>
                            <div class="">
                                <!-- add assumption button -->
                                <div
                                    class="text-xs rounded-bl py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-y border-l">
                                    <button :disabled="userIsViewer" @click="addAssumption" class="text-zinc-400 italic hover:text-zinc-500"><i
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
                                    <SectionHeader :sectionName="section.name" :sectionIndex="sectionIndex" :changingEnabled="true" :userIsViewer="userIsViewer"
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
                                        :possible-integration-values="possibleIntegrationValuesState"
                                        :userIsViewer="userIsViewer"></VariableRowHeader>
                                    <div
                                        class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                        <button :disabled="userIsViewer" @click="addVariable(sectionIndex)"
                                            class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-3"></i>Add Variable</button>
                                    </div>

                                    <VariableRowHeader @update-value="updateEndRowValue"
                                        :variable="section.end_row" :variable-index="0"
                                        :timeSeriesMap="useVariableTimeSeriesMap(section.rows)"
                                        :variableSearchMap="useVariableSearchMap(section.rows)"
                                        :sectionIndex="sectionIndex"
                                        :sectionName="section.name"
                                        :isEndRow="true"
                                        :hierarchy="'med'"
                                        :userIsViewer="userIsViewer">
                                    </VariableRowHeader>
                                </div>
                                <div class="">
                                    <!-- add section button -->
                                    <div
                                        class="text-xs py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                        <button :disabled="userIsViewer" @click="addSection" class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-2"></i>Add Section</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div>
                                <div class="flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-200 border-zinc-300 border-t-zinc-400 border-l border-b border-t-2">
                                    <span class="font-medium uppercase">
                                        Total Revenues
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="overflow-x-auto" id="table-right" @scroll="stickScroll('table-right', 'dates')">
                        <div id="assumption-values">
                            <div class="flex">
                                <!-- assumption header empty -->
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <ClientOnly>
                                <VariableRow v-for="(assumptionValues, index) in computedAssumptionValuesToDisplay"
                                :values="assumptionValues" :round-to="revenueState.assumptions[index].decimal_places" :hierarchy="'low'"></VariableRow>
                            </ClientOnly>
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
                                <ClientOnly>
                                    <VariableRow v-if="computedVariableValuesToDisplay"
                                        v-for="(variableValues, variableIndex) in computedVariableValuesToDisplay.get(index)"
                                        :values="variableValues" :round-to="revenueState.sections[index].rows[variableIndex].decimal_places" :hierarchy="'low'"></VariableRow>
                                </ClientOnly>
                                <div class="flex">
                                    <!-- add variable button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <ClientOnly>
                                    <VariableRow v-if="computedEndRowValuesToDisplay"
                                        :values="computedEndRowValuesToDisplay[index]" :round-to="2" :hierarchy="'med'"></VariableRow>
                                </ClientOnly>
                            </div>
                            <div class="flex">
                                    <!-- add section button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                        </div>
                        <div id="total-revenue-values" class="border-zinc-300">
                            <ClientOnly>
                                <VariableRow v-if="computedEndRowValuesToDisplay" :values="totalRevenuesToDisplay" :round-to="2" :isFinalRow="true" :hierarchy="'high'"></VariableRow>
                            </ClientOnly>
                        </div>
                    </div>
                </div>
            </div>
            <SheetErrorMessages v-if="(errorMessages.length > 0)" :errorMessages="errorMessages" @close="closeErrorMessage"></SheetErrorMessages>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">

import { mapState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useModelMetaStore } from '~~/store/useModelMetaStore';


import { useFormulaParser } from '~~/methods/useFormulaParser';
import { useGetValueFromHumanReadable } from '~~/methods/useGetValueFromHumanReadable';
import { useMathParser } from '~~/methods/useMathParser';

export default {
    data() {
        return {
            userAndMetaDataLoading: true,
            errorMessages: [],
            userIsViewer: false
        }
    },
    async mounted() {
        this.userAndMetaDataLoading = true;
        try {
            await this.updatePiniaUserStore();
            await this.updatePiniaModelMetaStore(this.$route.params.modelId);
            this.userAndMetaDataLoading = false;
        } catch(e) {
            console.log(e) //todo: handle error
        }

        this.userIsViewer = this.piniaModelMetaStore.viewers.includes(this.piniaUserStore._id);

    },
    computed: {
        ...mapState(useUserStore, ['piniaUserStore']),
        ...mapState(useModelMetaStore, ['piniaModelMetaStore']),
        dates() {
            if(this.piniaModelMetaStore.starting_month) {
                const date: string[] = this.piniaModelMetaStore.starting_month.split("-");
                return useDateArray(new Date(+date[0], +date[1] - 1))
            }
        },
        computedAssumptionValuesToDisplay() {
            var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions);
            return assumptionValuesArray;
        },
        computedVariableValuesToDisplay() {
            var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
            for (let i = 0; i < this.revenueState.sections.length; i++) {
                //variables
                var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables))
                valuesOfAssumptionsAndVariables.splice(0, this.revenueState.assumptions.length);
                variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
            };

            return variablesValuesStorage;
        },
        computedEndRowValuesToDisplay() {
            var endRowValuesStorage: string[][] = [];
            for (let i = 0; i < this.revenueState.sections.length; i++) {
                var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                //endrow
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables.concat(this.revenueState.sections[i].end_row)));
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.revenueState.assumptions.length);
                endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);
            };
            return endRowValuesStorage;
        },
        totalRevenuesToDisplay() {
            var returnArray:string[] = [];

            if(this.computedEndRowValuesToDisplay.length > 0) {

                //populate array with all calculation to perform
                var calcArray:string[] = [];
                
                for(let i=0; i < 24; i++) {
                    calcArray.push("");
                }

                for(let i=0; i < this.computedEndRowValuesToDisplay.length; i++) {
                    for(let j=0; j < this.computedEndRowValuesToDisplay[i].length; j++) {
                        if(this.computedEndRowValuesToDisplay[i][j] != "–") {
                            calcArray[j] = calcArray[j] + "+" + this.computedEndRowValuesToDisplay[i][j];
                        }
                    }
                }

                for(let i=0; i < calcArray.length; i++) {
                    try {
                        returnArray.push(useMathParser(calcArray[i]).toString());
                    } catch(e) {
                        if(this.computedEndRowValuesToDisplay.length === 1) {
                            returnArray.push(this.computedEndRowValuesToDisplay[0][i]);
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
        ...mapActions(useModelMetaStore, ['updatePiniaModelMetaStore']),
        ...mapActions(useUserStore, ['updatePiniaUserStore']),
        closeErrorMessage(index:number){
            this.errorMessages.splice(index, 1)
        },
        stickScroll(idParent:string, idChild:string) {
            const scrollParent = document.querySelector(`#${idParent}`);
            const scrollChild = document.querySelector(`#${idChild}`);
            scrollChild.scrollLeft = scrollParent.scrollLeft;
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

            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the section again.");
                this.revenueState = await useSheetUpdate().getRevenueSheet(this.route.params.modelId)
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

            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
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

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                    if (!(actualSheet.assumptions[variableIndex].value === this.revenueState.assumptions[variableIndex].value)) {
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
                this.revenueState.sections[sectionIndex].rows[variableIndex].value = storageValue.toString();

                if(this.revenueState.sections[sectionIndex].rows[variableIndex].integration_name != null) {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                    this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = true;
                } else if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                    this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                } else {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                    this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                }

                try {
                    //update RevenueState
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
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
        async updateIntegrationValue(integrationSelected: string, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if(integrationSelected != "None") {
                this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_name = integrationSelected;
                this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = true;
            } else {
                var checkValue = this.revenueState.sections[sectionIndex].rows[variableIndex].value;
                if (checkValue.includes("+") || checkValue.includes("-") || checkValue.includes("*") || checkValue.includes("/") || checkValue.includes("-")) {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                } else {
                    this.revenueState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                }
                this.revenueState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(checkValue, timeSeriesMap);
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_name = null;
                this.revenueState.sections[sectionIndex].rows[variableIndex].integration_values = null;
            }

            try {
                //update RevenueState
                this.revenueState = await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
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

                //todo: handle integration
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.revenueState.sections[sectionIndex].end_row.var_type = "formula";
                } else {
                    this.revenueState.sections[sectionIndex].end_row.var_type = "value";
                }

                try {
                    //update RevenueState
                    await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
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
        async updateAssumptionSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces:number, startingAtInput: number, sectionIndex: number) {

            this.revenueState.assumptions[variableIndex].val_type = valTypeInput;
            this.revenueState.assumptions[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null ||value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.revenueState.assumptions[variableIndex].value_1 = undefined;
                this.revenueState.assumptions[variableIndex].first_value_diff = false;
            } else {
                this.revenueState.assumptions[variableIndex].first_value_diff = true;
            }

            this.revenueState.assumptions[variableIndex].decimal_places = decimalPlaces;
            this.revenueState.assumptions[variableIndex].starting_at = startingAtInput;

            try {
                //update RevenueState
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions[variableIndex].value === this.revenueState.assumptions[variableIndex].value)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async updateVariableSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces: number, startingAtInput: number, sectionIndex: number) {
            
            this.revenueState.sections[sectionIndex].rows[variableIndex].val_type = valTypeInput;
            this.revenueState.sections[sectionIndex].rows[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null || value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.revenueState.sections[sectionIndex].rows[variableIndex].value_1 = undefined;
                this.revenueState.sections[sectionIndex].rows[variableIndex].first_value_diff = false;
            } else {
                this.revenueState.sections[sectionIndex].rows[variableIndex].first_value_diff = true;
            }

            this.revenueState.sections[sectionIndex].rows[variableIndex].decimal_places = decimalPlaces;
            this.revenueState.sections[sectionIndex].rows[variableIndex].starting_at = startingAtInput;

            try {
                //update RevenueState
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
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

            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions.length === this.revenueState.assumptions.length)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async deleteSection(sectionIndex: number) {
            //first directly change the state
            this.revenueState.sections.splice(sectionIndex, 1)
            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.revenueState.sections[sectionIndex].rows.length)) {
                    this.revenueState = actualSheet;
                }
            }
        },
        async deleteVariable(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.revenueState.sections[sectionIndex].rows.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateRevenueSheet(this.route.params.modelId, this.revenueState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getRevenueSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.revenueState.sections[sectionIndex].rows.length)) {
                    this.revenueState = actualSheet;
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
    }
}

</script>