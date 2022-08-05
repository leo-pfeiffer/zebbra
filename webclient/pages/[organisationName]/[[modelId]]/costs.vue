<script setup lang="ts">
definePageMeta({
    middleware: ["auth", "route-check"]
})
</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <LoadingSpinner v-if="costDataLoading && !costDataLoadingFailed" :text="'Loading'"></LoadingSpinner>
            <div class="h-full" v-if="!costDataLoading">
                <div
                    class="py-3 border-b px-3 border-zinc-300 top-0 min-h-[70px] max-h-[70px]">
                    <SheetHeader :user="piniaUserStore" :modelMeta="piniaModelMetaStore" :sheetName="'Costs'" :workspaceName="piniaUserStore.workspaces[0].name"
                        :modelName="piniaModelMetaStore.name"></SheetHeader>
                </div>
                <div class="ml-1 pl-2 flex top-0 bg-white pt-2 min-h-[50px] max-h-[50px]">
                    <div class="min-w-[319px] max-w-[319px]">
                    </div>
                    <div class="min-w-[150px] max-w-[150px] z-10">
                        <div class="relative border border-r-2 rounded-bl rounded-tl border-zinc-300 text-xs uppercase bg-zinc-100 text-zinc-700 text-center p-2">
                            Values
                            <InfoToggle :position="'absolute'" :text="'Double click on the cell to define the value.'"></InfoToggle>
                            </div>
                    </div>
                    <div class="overflow-x-auto no-scrollbar" id="dates"
                        @scroll="stickScroll('dates', 'table-right')">
                        <div class="border-zinc-300 flex">
                            <div class="first:border-l first:border-l-zinc-100 text-xs py-2 px-2 border-r border-y border-zinc-300 min-w-[90px] max-w-[90px] text-center uppercase bg-zinc-100 text-zinc-700"
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
                                        Assumptions<InfoToggle :position="'inline'" :text="'Assumptions defined here can be accessed in the model below.'"></InfoToggle>
                                    </div>
                                </div>
                                <VariableRowHeader @update-value="updateAssumptionValue"
                                    @update-settings="updateAssumptionSettings" @update-name="updateAssumptionName"
                                    @delete-variable="deleteAssumption"
                                    v-for="(assumption, index) in piniaCostStore.assumptions" :variable="assumption"
                                    :variableIndex="index"
                                    :timeSeriesMap="useVariableTimeSeriesMap(piniaCostStore.assumptions)"
                                    :variableSearchMap="useVariableSearchMap(piniaCostStore.assumptions)"
                                    :sectionIndex="0" :isEndRow="false" :showIntegration="false"
                                    :userIsViewer="userIsViewer">
                                </VariableRowHeader>
                                <div class="">
                                    <!-- add assumption button -->
                                    <div
                                        class="text-xs rounded-bl py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-y border-l">
                                        <button :disabled="userIsViewer" @click="addAssumption"
                                            class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-3"></i>Add Assumption</button>
                                    </div>
                                </div>
                            </div>
                            <div id="model-headers">
                                <div>

                                    <div
                                        class="group flex mt-6 text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                                        <span class="font-medium uppercase max-w-fit">
                                            Model<InfoToggle :position="'inline'" :text="'The output of the cost model will automatically be added to the P&L.'"></InfoToggle>
                                        </span>
                                    </div>
                                    <div>
                                        <SectionHeader :sectionName="'Payroll'" :changingEnabled="false"
                                            :userIsViewer="userIsViewer"></SectionHeader>
                                        <EmployeeRowHeader v-for="(employee, index) in piniaPayrollStore.employees"
                                            :employee="employee" :employeeIndex="index"
                                            @update-employee="updateEmployee" @delete-employee="deleteEmployee"
                                            :userIsViewer="userIsViewer">
                                        </EmployeeRowHeader>
                                        <div
                                            class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                            <button :disabled="userIsViewer" @click="addEmployee()"
                                                class="text-zinc-400 italic hover:text-zinc-500"><i
                                                    class="bi bi-plus-lg mr-3"></i>Add Employee</button>
                                        </div>
                                        <div
                                            class="flex text-xs text-zinc-700 bg-zinc-50 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-l border-t">
                                            <span class="font-medium">
                                                <li class="marker:text-white/0">Total Payroll<InfoToggle :position="'list'" :text="'The output of the cost model will automatically be added to the P&L.'"></InfoToggle></li>
                                            </span>
                                        </div>
                                    </div>
                                    <div v-for="(section, sectionIndex) in piniaCostStore.sections" :key="sectionIndex">
                                        <SectionHeader :sectionName="section.name" :sectionIndex="sectionIndex"
                                            :changingEnabled="false" @change-section-name="updateSectionName"
                                            @delete-section="deleteSection" :userIsViewer="userIsViewer">
                                        </SectionHeader>
                                        <VariableRowHeader @update-value="updateVariableValue"
                                            @update-settings="updateVariableSettings" @update-name="updateVariableName"
                                            @delete-variable="deleteVariable"
                                            @update-integration="updateIntegrationValue"
                                            v-for="(variable, index) in section.rows" :variable="variable"
                                            :variable-index="index"
                                            :timeSeriesMap="useVariableTimeSeriesMap(piniaCostStore.assumptions.concat(section.rows))"
                                            :variableSearchMap="useVariableSearchMap(piniaCostStore.assumptions.concat(section.rows))"
                                            :sectionIndex="sectionIndex" :isEndRow="false" :showIntegration="true"
                                            :possible-integration-values="piniaPossibleIntegrationsStore"
                                            :userIsViewer="userIsViewer">
                                        </VariableRowHeader>
                                        <div
                                            class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                            <button :disabled="userIsViewer" @click="addVariable(sectionIndex)"
                                                class="text-zinc-400 italic hover:text-zinc-500"><i
                                                    class="bi bi-plus-lg mr-3"></i>Add Variable</button>
                                        </div>

                                        <VariableRowHeader @update-value="updateEndRowValue" :variable="section.end_row"
                                            :variable-index="0" :timeSeriesMap="useVariableTimeSeriesMap(section.rows)"
                                            :variableSearchMap="useVariableSearchMap(section.rows)"
                                            :sectionIndex="sectionIndex" :sectionName="section.name" :isEndRow="true"
                                            :hierarchy="'med'" :userIsViewer="userIsViewer">
                                        </VariableRowHeader>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <div
                                        class="group flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-200 border-zinc-300 border-t-zinc-400 border-l border-b border-t-2">
                                        <span class="font-medium uppercase">
                                            Total Costs
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="overflow-x-auto" id="table-right" @scroll="stickScroll('table-right', 'dates')">
                            <div id="assumption-values">
                                <div class="flex">
                                    <!-- assumption header empty -->
                                    <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <ClientOnly>
                                    <VariableRow v-for="(assumptionValues, index) in computedAssumptionValuesToDisplay"
                                        :values="assumptionValues"
                                        :round-to="piniaCostStore.assumptions[index].decimal_places" :hierarchy="'low'">
                                    </VariableRow>
                                </ClientOnly>
                                <div class="flex">
                                    <!-- add assumption button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 border-zinc-300 border-y"
                                        v-for="date in dates">X</div>
                                </div>
                            </div>
                            <div id="model-values">
                                <div class="flex mt-6">
                                    <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <!-- Payroll -->
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <div class="flex" v-for="payrollValues in payrollToDisplay">
                                    <ClientOnly>
                                        <VariableRow :values="payrollValues" :round-to="2" :hierarchy="'low'">
                                        </VariableRow>
                                    </ClientOnly>
                                </div>
                                <div class="flex">
                                    <!-- add employee button empty -->
                                    <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <div class="flex">
                                    <ClientOnly>
                                        <VariableRow :values="totalPayrollToDisplay" :round-to="2" :isFinalRow="false"
                                            :hierarchy="'med'"></VariableRow>
                                    </ClientOnly>
                                </div>
                                <div v-for="(section, index) in piniaCostStore.sections" :key="index">
                                    <div class="flex">
                                        <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 border-zinc-300 border-t"
                                            v-for="date in dates">X</div>
                                    </div>
                                    <ClientOnly>
                                        <VariableRow v-if="computedVariableValuesToDisplay"
                                            v-for="(variableValues, variableIndex) in computedVariableValuesToDisplay.get(index)"
                                            :values="variableValues"
                                            :round-to="piniaCostStore.sections[index].rows[variableIndex].decimal_places"
                                            :hierarchy="'low'">
                                        </VariableRow>
                                    </ClientOnly>
                                    <div class="flex">
                                        <!-- add variable button empty -->
                                        <div class="text-xs py-2 px-2 min-w-[90px] max-w-[90px] text-white/0 border-zinc-300 border-t"
                                            v-for="date in dates">X</div>
                                    </div>
                                    <ClientOnly>
                                        <VariableRow v-if="computedEndRowValuesToDisplay"
                                            :values="computedEndRowValuesToDisplay[index]" :round-to="2"
                                            :hierarchy="'med'">
                                        </VariableRow>
                                    </ClientOnly>
                                </div>
                            </div>
                            <div id="total-cost-values" class="border-zinc-300">
                                <ClientOnly>
                                    <VariableRow v-if="computedEndRowValuesToDisplay" :values="totalCostsToDisplay"
                                        :round-to="2" :isFinalRow="true" :hierarchy="'high'"></VariableRow>
                                </ClientOnly>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <SheetErrorMessages v-if="(errorMessages.length > 0)" :errorMessages="errorMessages"
                    @close="closeErrorMessage"></SheetErrorMessages>
        </div>
    </NuxtLayout>
</template>

<script lang="ts">
import { Employee, Section, Variable } from '~~/types/Model';
import { useVariableSearchMap } from '~~/methods/useVariableSearchMap';
import { useVariableTimeSeriesMap } from '~~/methods/useVariableTimeSeriesMap';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { useFormulaParser } from '~~/methods/useFormulaParser';
import { useGetValueFromHumanReadable } from '~~/methods/useGetValueFromHumanReadable';
import { useMathParser } from '~~/methods/useMathParser';
import { mapWritableState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useCostStore } from '~~/store/useCostStore';
import { usePayrollStore } from '~~/store/usePayrollStore';
import { useModelMetaStore } from '~~/store/useModelMetaStore';
import { usePossibleIntegrationsStore } from '~~/store/usePossibleIntegrationsStore';
import { useDateArray } from '~~/methods/useDateArray';


export default {
    data() {
        return {
            costDataLoading: true,
            costDataLoadingFailed: false,
            errorMessages: [],
            userIsViewer: false
        }
    },
    async mounted() {

        this.costDataLoading = true;
        try {
            await this.updatePiniaUserStore();
            await this.updatePiniaModelMetaStore(this.$route.params.modelId);
            await this.setPiniaCostStore(this.$route.params.modelId);
            await this.setPiniaPayrollStore(this.$route.params.modelId);
            await this.setPossibleIntegrationsStore(this.$route.params.modelId);
            this.userIsViewer = this.piniaModelMetaStore.viewers.includes(this.piniaUserStore._id);
            this.costDataLoading = false;
        } catch (e) {
            this.errorMessages.push("Failed to load data. Please reload the page.");
            this.costDataLoadingFailed = true;
            console.log(e)
        }

    },
    computed: {
        ...mapWritableState(useUserStore, ['piniaUserStore']),
        ...mapWritableState(useModelMetaStore, ['piniaModelMetaStore']),
        ...mapWritableState(useCostStore, ['piniaCostStore']),
        ...mapWritableState(usePayrollStore, ['piniaPayrollStore']),
        ...mapWritableState(usePossibleIntegrationsStore, ['piniaPossibleIntegrationsStore']),
        dates() {
            if (this.piniaModelMetaStore.starting_month) {
                const date: string[] = this.piniaModelMetaStore.starting_month.split("-");
                return useDateArray(new Date(+date[0], +date[1] - 1))
            }
        },
        computedAssumptionValuesToDisplay() {
            var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(this.piniaCostStore.assumptions);
            return assumptionValuesArray;
        },
        computedVariableValuesToDisplay() {
            var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
            for (let i = 0; i < this.piniaCostStore.sections.length; i++) {
                var sectionVariables: Variable[] = [...this.piniaCostStore.sections[i].rows];
                var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.piniaCostStore.assumptions.concat(sectionVariables))
                valuesOfAssumptionsAndVariables.splice(0, this.piniaCostStore.assumptions.length);
                variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
            };

            return variablesValuesStorage;
        },
        computedEndRowValuesToDisplay() {

            var endRowValuesStorage: string[][] = [];
            for (let i = 0; i < this.piniaCostStore.sections.length; i++) {
                var sectionVariables: Variable[] = [...this.piniaCostStore.sections[i].rows];
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.piniaCostStore.assumptions.concat(sectionVariables.concat(this.piniaCostStore.sections[i].end_row)));
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.piniaCostStore.assumptions.length);
                endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);
            };

            return endRowValuesStorage;

        },
        payrollToDisplay() {
            var returnArray: string[][] = [];

            const modelStartDate = new Date(this.piniaModelMetaStore.starting_month);

            if (this.piniaPayrollStore.employees) {
                for (let i = 0; i < this.piniaPayrollStore.employees.length; i++) {
                    var valueArray: string[] = [];

                    var startDateDiff: number;
                    var endDateDiff: number;

                    const employeeStartDate = new Date(this.piniaPayrollStore.employees[i].start_date);

                    startDateDiff = this.getMonthDiff(modelStartDate, employeeStartDate);

                    var employeeEndDate: Date;
                    if (this.piniaPayrollStore.employees[i].end_date != null) {
                        employeeEndDate = new Date(this.piniaPayrollStore.employees[i].end_date);
                        endDateDiff = this.getMonthDiff(modelStartDate, employeeEndDate);
                    } else {
                        endDateDiff = 24;
                    }

                    for (let j = 0; j < 24; j++) {
                        if (j >= startDateDiff && j <= endDateDiff) {
                            valueArray.push(this.piniaPayrollStore.employees[i].monthly_salary.toString())
                        } else {
                            valueArray.push("–");
                        }
                    }
                    returnArray.push(valueArray);
                }
            }
            return returnArray;
        },
        totalPayrollToDisplay() {
            var returnArray: string[] = [];

            if (this.piniaPayrollStore.payroll_values && this.piniaPayrollStore.payroll_values.length >= 24) {
                for (let i = 0; i < 24; i++) {
                    returnArray.push(this.piniaPayrollStore.payroll_values[i].value);
                }
            } else if (this.piniaPayrollStore.payroll_values && this.piniaPayrollStore.payroll_values.length > 0) {

                for (let i = 0; i < 24; i++) {
                    if (i < this.piniaPayrollStore.payroll_values.length) {
                        returnArray.push(this.piniaPayrollStore.payroll_values[i].value);
                    } else {
                        returnArray.push("–")
                    }
                }

            } else {
                for (let i = 0; i < 24; i++) {
                    returnArray.push("0");
                }
            }
            return returnArray;
        },
        totalCostsToDisplay() {
            var returnArray: string[] = [];

            if (this.computedEndRowValuesToDisplay.length > 0) {

                //populate array with all calculation to perform
                var calcArray: string[] = [];

                for (let i = 0; i < 24; i++) {
                    calcArray.push("");
                }

                for (let i = 0; i < this.computedEndRowValuesToDisplay.length; i++) {
                    for (let j = 0; j < this.computedEndRowValuesToDisplay[i].length; j++) {
                        if (this.computedEndRowValuesToDisplay[i][j] != "–") {
                            calcArray[j] = calcArray[j] + "+" + this.computedEndRowValuesToDisplay[i][j];
                        }
                    }
                }

                for (let i = 0; i < calcArray.length; i++) {
                    calcArray[i] = calcArray[i] + "+" + this.totalPayrollToDisplay[i];
                }

                for (let i = 0; i < calcArray.length; i++) {
                    try {
                        returnArray.push(useMathParser(calcArray[i]).toString());
                    } catch (e) {
                        if (this.computedEndRowValuesToDisplay.length === 1) {
                            returnArray.push(this.computedEndRowValuesToDisplay[0][i]);
                        } else {
                            returnArray.push("#REF!");
                        }
                    }
                }

                return returnArray;

            } else {
                for (let i = 0; i < 24; i++) {
                    returnArray.push("–")
                }
                return returnArray;
            }
        }

    },
    methods: {
        ...mapActions(useModelMetaStore, ['updatePiniaModelMetaStore']),
        ...mapActions(useUserStore, ['updatePiniaUserStore']),
        ...mapActions(useCostStore, ['setPiniaCostStore']),
        ...mapActions(usePayrollStore, ['setPiniaPayrollStore']),
        ...mapActions(usePossibleIntegrationsStore, ['setPossibleIntegrationsStore']),
        closeErrorMessage(index: number) {
            this.errorMessages.splice(index, 1)
        },
        stickScroll(idParent: string, idChild: string) {
            const scrollParent = document.querySelector(`#${idParent}`);
            const scrollChild = document.querySelector(`#${idChild}`);
            scrollChild.scrollLeft = scrollParent.scrollLeft;
        },
        getMonthDiff(startDate: Date, endDate: Date) {
            return endDate.getMonth() - startDate.getMonth() + (12 * (endDate.getFullYear() - startDate.getFullYear()))
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

            this.piniaCostStore.sections.push(emptySection);

            try {
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the section again.");
                this.piniaCostStore = await useSheetUpdate().getCostSheet(this.$route.params.modelId)
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

            this.piniaCostStore.assumptions.push(emptyAssumption);

            try {
                this.piniaCostStore = await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.piniaCostStore = await useSheetUpdate().getCostSheet(this.$route.params.modelId)
            }

            try {
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.piniaCostStore = await useSheetUpdate().getCostSheet(this.$route.params.modelId)
            }

        },
        async addEmployee() {

            console.log(this.piniaModelMetaStore.starting_month)

            const emptyEmployee: Employee = {
                _id: null,
                name: "Joanna Doe",
                start_date: this.piniaModelMetaStore.starting_month,
                end_date: null,
                title: "CEO",
                department: "Finance",
                monthly_salary: 0,
                from_integration: false,
            }

            this.piniaPayrollStore.employees.push(emptyEmployee);

            try {
                await useSheetUpdate().updatePayroll(this.$route.params.modelId, this.piniaPayrollStore.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not add employee! Please try again.");
                this.piniaPayrollStore = await useSheetUpdate().getPayroll(this.$route.params.modelId);
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

            this.piniaCostStore.sections[sectionIndex].rows.push(emptyVariable);

            try {
                this.piniaCostStore = await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.piniaCostStore = await useSheetUpdate().getCostSheet(this.$route.params.modelId)
            }

        },
        async updateAssumptionValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.piniaCostStore.assumptions[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.piniaCostStore.assumptions[variableIndex].value = storageValue.toString();
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.piniaCostStore.assumptions[variableIndex].var_type = "formula";
                } else {
                    this.piniaCostStore.assumptions[variableIndex].var_type = "value";
                }

                try {
                    //update piniaCostStore
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(actualSheet.assumptions[variableIndex].value === this.piniaCostStore.assumptions[variableIndex].value)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateEmployee(employeeIndex: number, newName: string, newSalary: number, newTitle: string, newDepartment: string, newStartDate: string, newEndDate: string) {

            this.piniaPayrollStore.employees[employeeIndex].name = newName;
            this.piniaPayrollStore.employees[employeeIndex].monthly_salary = newSalary;
            this.piniaPayrollStore.employees[employeeIndex].title = newTitle;
            this.piniaPayrollStore.employees[employeeIndex].department = newDepartment;
            this.piniaPayrollStore.employees[employeeIndex].start_date = newStartDate;
            if(newEndDate === "") {
                this.piniaPayrollStore.employees[employeeIndex].end_date = null;
            } else {
                this.piniaPayrollStore.employees[employeeIndex].end_date = newEndDate;
            }

            try {
                this.piniaPayrollStore = await useSheetUpdate().updatePayroll(this.$route.params.modelId, this.piniaPayrollStore.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not update employee! Please try again.");
                this.piniaPayrollStore = await useSheetUpdate().getPayroll(this.$route.params.modelId);
            }

        },
        async updateVariableValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].value = storageValue.toString();

                if (this.piniaCostStore.sections[sectionIndex].rows[variableIndex].integration_name != null) {
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].time_series = true;
                } else if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                } else {
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "value";
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                }

                try {
                    //update piniaCostStore
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.piniaCostStore.sections[0].rows[variableIndex].value)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateIntegrationValue(integrationSelected: string, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (integrationSelected != "None") {
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].integration_name = integrationSelected;
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].time_series = true;
            } else {
                var checkValue = this.piniaCostStore.sections[sectionIndex].rows[variableIndex].value;
                if (checkValue.includes("+") || checkValue.includes("-") || checkValue.includes("*") || checkValue.includes("/") || checkValue.includes("-")) {
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                } else {
                    this.piniaCostStore.sections[sectionIndex].rows[variableIndex].var_type = "value";
                }
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(checkValue, timeSeriesMap);
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].integration_name = null;
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].integration_values = null;
            }

            try {
                //update piniaCostStore
                this.piniaCostStore = await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.sections[0].rows[variableIndex].integration_name === this.piniaCostStore.sections[0].rows[variableIndex].integration_name) ||
                    !(actualSheet.sections[0].rows[variableIndex].var_type === this.piniaCostStore.sections[0].rows[variableIndex].var_type)) {
                    this.piniaCostStore = actualSheet;
                }
            }
        },
        async updateEndRowValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.piniaCostStore.sections[sectionIndex].end_row.time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.piniaCostStore.sections[sectionIndex].end_row.value = storageValue.toString();

                //todo: handle integration
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.piniaCostStore.sections[sectionIndex].end_row.var_type = "formula";
                } else {
                    this.piniaCostStore.sections[sectionIndex].end_row.var_type = "value";
                }

                try {
                    //update piniaCostStore
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.piniaCostStore.sections[0].rows[variableIndex].value)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateAssumptionName(newName: string, variableIndex: number, sectionIndex: number) {

            if(useFormulaParser().charIsNumerical(newName[0])) {
                this.errorMessages.push("A variable name cannot start with a number.")
                return
            }

            if(newName.length === 0) {
                this.errorMessages.push("Please enter a valid name.")
                return
            }

            if(newName.includes("[") || newName.includes("]")) {
                this.errorMessages.push("A variable name cannot include operators, brackets, hashtags, or dollar signs.")
                return
            }

            for(let i=0; i< newName.length; i++) {
                if(useFormulaParser().charIsOperator(newName[i]) || useFormulaParser().charIsRefToken(newName[i])) {
                    this.errorMessages.push("A variable name cannot include operators, brackets, hashtags, or dollar signs.")
                    return
                }
            }

            if (newName.length > 0) {
                this.piniaCostStore.assumptions[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(this.piniaCostStore.assumptions[variableIndex].name === actualSheet.assumptions[variableIndex].name)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("Please enter a valid name.");
            }
        },
        async updateSectionName(sectionIndex: number, newName: string) {
            if (newName.length > 0) {
                this.piniaCostStore.sections[sectionIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(this.piniaCostStore.sections[sectionIndex].name === actualSheet.sections[sectionIndex].name)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("The section name must be at least one character.");
            }
        },
        async updateVariableName(newName: string, variableIndex: number, sectionIndex: number) {

            if(useFormulaParser().charIsNumerical(newName[0])) {
                this.errorMessages.push("A variable name cannot start with a number.")
                return
            }

            if(newName.length === 0) {
                this.errorMessages.push("Please enter a valid name.")
                return
            }

            if(newName.includes("[") || newName.includes("]")) {
                this.errorMessages.push("A variable name cannot include operators, brackets, hashtags, or dollar signs.")
                return
            }

            for(let i=0; i< newName.length; i++) {
                if(useFormulaParser().charIsOperator(newName[i]) || useFormulaParser().charIsRefToken(newName[i])) {
                    this.errorMessages.push("A variable name cannot include operators, brackets, hashtags, or dollar signs.")
                    return
                }
            }

            if (newName.length > 0) {
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                    if (!(this.piniaCostStore.sections[sectionIndex].rows[variableIndex].name === actualSheet.sections[sectionIndex].rows[variableIndex].name)) {
                        this.piniaCostStore = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("Please enter a valid name.");
            }
        },
        async updateAssumptionSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces: number, startingAtInput: number, sectionIndex: number) {

            this.piniaCostStore.assumptions[variableIndex].val_type = valTypeInput;
            this.piniaCostStore.assumptions[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null || value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.piniaCostStore.assumptions[variableIndex].value_1 = undefined;
                this.piniaCostStore.assumptions[variableIndex].first_value_diff = false;
            } else {
                this.piniaCostStore.assumptions[variableIndex].first_value_diff = true;
            }

            this.piniaCostStore.assumptions[variableIndex].decimal_places = decimalPlaces;
            this.piniaCostStore.assumptions[variableIndex].starting_at = startingAtInput;

            try {
                //update piniaCostStore
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.assumptions[variableIndex].value === this.piniaCostStore.assumptions[variableIndex].value)) {
                    this.piniaCostStore = actualSheet;
                }
            }
        },
        async updateVariableSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces: number, startingAtInput: number, sectionIndex: number) {

            this.piniaCostStore.sections[sectionIndex].rows[variableIndex].val_type = valTypeInput;
            this.piniaCostStore.sections[sectionIndex].rows[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null || value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].value_1 = undefined;
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].first_value_diff = false;
            } else {
                this.piniaCostStore.sections[sectionIndex].rows[variableIndex].first_value_diff = true;
            }

            this.piniaCostStore.sections[sectionIndex].rows[variableIndex].decimal_places = decimalPlaces;
            this.piniaCostStore.sections[sectionIndex].rows[variableIndex].starting_at = startingAtInput;

            try {
                //update piniaCostStore
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows[variableIndex].value === this.piniaCostStore.sections[sectionIndex].rows[variableIndex].value)) {
                    this.piniaCostStore = actualSheet;
                }
            }
        },
        async deleteAssumption(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.piniaCostStore.assumptions.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.assumptions.length === this.piniaCostStore.assumptions.length)) {
                    this.piniaCostStore = actualSheet;
                }
            }
        },
        async deleteEmployee(employeeIndex: number) {

            this.piniaPayrollStore.employees.splice(employeeIndex, 1);

            try {
                this.piniaPayrollStore = await useSheetUpdate().updatePayroll(this.$route.params.modelId, this.piniaPayrollStore.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not delete employee! Please try again.");
                this.piniaPayrollStore = await useSheetUpdate().getPayroll(this.$route.params.modelId);
            }

        },
        async deleteSection(sectionIndex: number) {
            //first directly change the state
            this.piniaCostStore.sections.splice(sectionIndex, 1)
            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.piniaCostStore.sections[sectionIndex].rows.length)) {
                    this.piniaCostStore = actualSheet;
                }
            }
        },
        async deleteVariable(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.piniaCostStore.sections[sectionIndex].rows.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.$route.params.modelId, this.piniaCostStore);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.piniaCostStore.sections[sectionIndex].rows.length)) {
                    this.piniaCostStore = actualSheet;
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