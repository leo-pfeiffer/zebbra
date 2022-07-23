<script setup lang="ts">
import { Employee, Section, Variable } from '~~/types/Model';
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

console.log(modelMeta.value.starting_month)

const costState = useCostState();
costState.value = await useSheetUpdate().getCostSheet(route.params.modelId);

const payrollState = usePayrollState();
payrollState.value = await useSheetUpdate().getPayroll(route.params.modelId);

console.log(payrollState.value);

//todo: find better solution
const date: string[] = modelMeta.value.starting_month.split("-");
const dates = useState('dates', () => useDateArray(new Date(+date[0], +date[1] - 1)));

const assumptionValuesToDisplayState = useState<string[][]>('costAssumptionValues');
const variableValuesToDisplayState = useState<Map<number, string[][]>>('costVariableValues');
const endRowValuesToDisplayState = useState<string[][]>('costEndRowValues');

const possibleIntegrationValuesState = usePossibleIntegrationValuesState();
possibleIntegrationValuesState.value = await useGetPossibleIntegrationValues(route.params.modelId);

</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div class="p-3 border-b border-zinc-300 top-0 min-h-[60px] max-h-[60px]">
                <h1 class="font-semibold text-xl inline-block align-middle">Costs</h1>
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
                                @delete-variable="deleteAssumption" v-for="(assumption, index) in costState.assumptions"
                                :variable="assumption" :variableIndex="index"
                                :timeSeriesMap="useVariableTimeSeriesMap(costState.assumptions)"
                                :variableSearchMap="useVariableSearchMap(costState.assumptions)" :sectionIndex="0"
                                :isEndRow="false" :showIntegration="false">
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

                                <div
                                    class="group flex mt-6 text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    <span class="font-medium uppercase">
                                        Model
                                    </span>
                                </div>
                                <div>
                                    <SectionHeader :sectionName="'Payroll'" :changingEnabled="false"></SectionHeader>
                                    <EmployeeRowHeader v-for="(employee, index) in payrollState.employees"
                                        :employee="employee" :employeeIndex="index"
                                        @update-employee="updateEmployee"
                                        @delete-employee="deleteEmployee"></EmployeeRowHeader>
                                    <div
                                        class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                        <button @click="addEmployee()"
                                            class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-3"></i>Add Employee</button>
                                    </div>
                                    <div
                                        class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-l border-t border-r-2">
                                        <span class="font-medium">
                                            <li class="marker:text-white/0">Total Payroll</li>
                                        </span>
                                    </div>
                                </div>
                                <div v-for="(section, sectionIndex) in costState.sections" :key="sectionIndex">
                                    <SectionHeader :sectionName="section.name" :sectionIndex="sectionIndex"
                                        :changingEnabled="true" @change-section-name="updateSectionName"
                                        @delete-section="deleteSection"></SectionHeader>
                                    <VariableRowHeader @update-value="updateVariableValue"
                                        @update-settings="updateVariableSettings" @update-name="updateVariableName"
                                        @delete-variable="deleteVariable" @update-integration="updateIntegrationValue"
                                        v-for="(variable, index) in section.rows" :variable="variable"
                                        :variable-index="index"
                                        :timeSeriesMap="useVariableTimeSeriesMap(costState.assumptions.concat(section.rows))"
                                        :variableSearchMap="useVariableSearchMap(costState.assumptions.concat(section.rows))"
                                        :sectionIndex="sectionIndex" :isEndRow="false" :showIntegration="true"
                                        :possible-integration-values="possibleIntegrationValuesState">
                                    </VariableRowHeader>
                                    <div
                                        class="text-xs py-2 pl-10 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l">
                                        <button @click="addVariable(sectionIndex)"
                                            class="text-zinc-400 italic hover:text-zinc-500"><i
                                                class="bi bi-plus-lg mr-3"></i>Add Variable</button>
                                    </div>

                                    <VariableRowHeader @update-value="updateEndRowValue" :variable="section.end_row"
                                        :variable-index="0" :timeSeriesMap="useVariableTimeSeriesMap(section.rows)"
                                        :variableSearchMap="useVariableSearchMap(section.rows)"
                                        :sectionIndex="sectionIndex" :sectionName="section.name" :isEndRow="true">
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
                                <div
                                    class="group flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-50 border-zinc-300 border">
                                    <span class="font-medium uppercase">
                                        Total Costs
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
                            <VariableRow v-for="(assumptionValues, index) in assumptionValuesToDisplayState"
                                :values="assumptionValues" :round-to="costState.assumptions[index].decimal_places">
                            </VariableRow>
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
                            <!-- Payroll -->
                            <div class="flex">
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <div class="flex" v-for="payrollValues in payrollToDisplay">
                                <VariableRow :values="payrollValues" :round-to="2"></VariableRow>
                            </div>
                            <div class="flex">
                                <!-- add employee button empty -->
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <div class="flex">
                                <!-- <VariableRow v-for="index in payrollState.employees" :values="payrollState.payroll_values" :round-to="2"></VariableRow> -->
                                <VariableRow :values="totalPayrollToDisplay" :round-to="2"
                                :isFinalRow="false"></VariableRow>
                            </div>
                            <div v-for="(section, index) in costState.sections" :key="index">
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <VariableRow v-if="variableValuesToDisplayState"
                                    v-for="(variableValues, variableIndex) in variableValuesToDisplayState.get(index)"
                                    :values="variableValues"
                                    :round-to="costState.sections[index].rows[variableIndex].decimal_places">
                                </VariableRow>
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
                        <div id="total-cost-values" class="border-zinc-300">
                            <VariableRow v-if="endRowValuesToDisplayState" :values="totalCostsToDisplay" :round-to="2"
                                :isFinalRow="true"></VariableRow>
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
        payrollToDisplay() {
            var returnArray:string[][] = [];

            console.log(this.payrollState.employees.length)

            if(this.payrollState.employees) {
                for(let i = 0; i < this.payrollState.employees.length; i++) {
                    var valueArray:string[] = [];
                    
                    for(let j=0; j < 24; j++) {
                        //todo: handle starting month and end month
                        valueArray.push(this.payrollState.employees[i].monthly_salary.toString())
                    }
                    returnArray.push(valueArray);
                }
            } 
            console.log(returnArray);
            return returnArray;
        },
        totalPayrollToDisplay() {
            var returnArray: string[] = [];

            if (this.payrollState.payroll_values) {
                for (let i = 0; i < 24; i++) {
                    returnArray.push(this.payrollState.payroll_values[i].value);
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

            if (this.endRowValuesToDisplayState.length > 0) {

                //populate array with all calculation to perform
                var calcArray: string[] = [];

                for (let i = 0; i < 24; i++) {
                    calcArray.push("");
                }

                for (let i = 0; i < this.endRowValuesToDisplayState.length; i++) {
                    for (let j = 0; j < this.endRowValuesToDisplayState[i].length; j++) {
                        if (this.endRowValuesToDisplayState[i][j] != "–") {
                            calcArray[j] = calcArray[j] + "+" + this.endRowValuesToDisplayState[i][j];
                        }
                    }
                }

                for(let i = 0; i < calcArray.length; i++) {
                    calcArray[i] = calcArray[i] + "+" + this.totalPayrollToDisplay[i];
                }

                for (let i = 0; i < calcArray.length; i++) {
                    try {
                        returnArray.push(useMathParser(calcArray[i]).toString());
                    } catch (e) {
                        if (this.endRowValuesToDisplayState.length === 1) {
                            returnArray.push(this.endRowValuesToDisplayState[0][i]);
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
        closeErrorMessage(index: number) {
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

            this.costState.sections.push(emptySection);

            this.updateDisplayedValues();

            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the section again.");
                this.costState = await useSheetUpdate().getCostSheet(this.route.params.modelId)
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

            this.costState.assumptions.push(emptyAssumption);

            const assumptionValuesArrayState = useState<string[][]>('costAssumptionValues');
            var assumptionValuesArray: string[][];

            try {
                assumptionValuesArray = useFormulaParser().getSheetRowValues(this.costState.assumptions);
                let index = assumptionValuesArray.length - 1;
                assumptionValuesArrayState.value.push(assumptionValuesArray[index])
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.costState = await useSheetUpdate().getCostSheet(this.route.params.modelId)
            }

            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.costState = await useSheetUpdate().getCostSheet(this.route.params.modelId)
            }

        },
        async addEmployee() {

            console.log(this.modelMeta.starting_month)

            const emptyEmployee: Employee = {
                _id: null,
                name: "Joanna Doe",
                start_date: this.modelMeta.starting_month,
                end_date: null,
                title: "CEO",
                department: "Finance",
                monthly_salary: 0,
                from_integration: false,
            }

            this.payrollState.employees.push(emptyEmployee);

            try {
                await useSheetUpdate().updatePayroll(this.route.params.modelId, this.payrollState.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not add employee! Please try again.");
                this.payrollState = await useSheetUpdate().getPayroll(this.route.params.modelId);
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

            this.costState.sections[sectionIndex].rows.push(emptyVariable);
            this.updateDisplayedValues();

            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
            } catch (e) {
                console.log(e)
                this.errorMessages.push("Something went wrong! Please try adding the variable again.");
                this.costState = await useSheetUpdate().getCostSheet(this.route.params.modelId)
                this.updateDisplayedValues();
            }

        },
        async updateAssumptionValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.costState.assumptions[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.costState.assumptions[variableIndex].value = storageValue.toString();
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.costState.assumptions[variableIndex].var_type = "formula";
                } else {
                    this.costState.assumptions[variableIndex].var_type = "value";
                }

                try {
                    //update CostState
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(actualSheet.assumptions[variableIndex].value === this.costState.assumptions[variableIndex].value)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateEmployee(employeeIndex:number, newName:string, newSalary:number, newTitle:string, newDepartment:string, newStartDate:string, newEndDate:string) {

            this.payrollState.employees[employeeIndex].name = newName;
            this.payrollState.employees[employeeIndex].monthly_salary = newSalary;
            this.payrollState.employees[employeeIndex].title = newTitle;
            this.payrollState.employees[employeeIndex].department = newDepartment;
            this.payrollState.employees[employeeIndex].start_date = newStartDate;
            this.payrollState.employees[employeeIndex].end_date = newEndDate;

            try {
                this.payrollState = await useSheetUpdate().updatePayroll(this.route.params.modelId, this.payrollState.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not update employee! Please try again.");
                this.payrollState = await useSheetUpdate().getPayroll(this.route.params.modelId);
            }

        },
        async updateVariableValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);
                this.costState.sections[sectionIndex].rows[variableIndex].value = storageValue.toString();

                if (this.costState.sections[sectionIndex].rows[variableIndex].integration_name != null) {
                    this.costState.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                    this.costState.sections[sectionIndex].rows[variableIndex].time_series = true;
                } else if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.costState.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                    this.costState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                } else {
                    this.costState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                    this.costState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                }

                try {
                    //update CostState
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.costState.sections[0].rows[variableIndex].value)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateIntegrationValue(integrationSelected: string, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (integrationSelected != "None") {
                this.costState.sections[sectionIndex].rows[variableIndex].var_type = "integration";
                this.costState.sections[sectionIndex].rows[variableIndex].integration_name = integrationSelected;
                this.costState.sections[sectionIndex].rows[variableIndex].time_series = true;
            } else {
                var checkValue = this.costState.sections[sectionIndex].rows[variableIndex].value;
                if (checkValue.includes("+") || checkValue.includes("-") || checkValue.includes("*") || checkValue.includes("/") || checkValue.includes("-")) {
                    this.costState.sections[sectionIndex].rows[variableIndex].var_type = "formula";
                } else {
                    this.costState.sections[sectionIndex].rows[variableIndex].var_type = "value";
                }
                this.costState.sections[sectionIndex].rows[variableIndex].time_series = this.isTimeSeries(checkValue, timeSeriesMap);
                this.costState.sections[sectionIndex].rows[variableIndex].integration_name = null;
                this.costState.sections[sectionIndex].rows[variableIndex].integration_values = null;
            }

            try {
                //update CostState
                this.costState = await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                this.updateDisplayedValues();

            } catch (e) {
                console.log(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.sections[0].rows[variableIndex].integration_name === this.costState.sections[0].rows[variableIndex].integration_name) ||
                    !(actualSheet.sections[0].rows[variableIndex].var_type === this.costState.sections[0].rows[variableIndex].var_type)) {
                    this.costState = actualSheet;
                }
            }
        },
        async updateEndRowValue(humanReadableInputValue: string, variableId: string, variableSearchMap: Map<string, string>, timeSeriesMap: Map<string, boolean>, variableIndex: number, sectionIndex: number) {
            if (humanReadableInputValue.length > 0) {

                //Get humanReadableInputValue and create storage value

                const storageValue: string = useGetValueFromHumanReadable(humanReadableInputValue, variableId, variableSearchMap);

                this.costState.sections[sectionIndex].end_row.time_series = this.isTimeSeries(storageValue, timeSeriesMap);
                this.costState.sections[sectionIndex].end_row.value = storageValue.toString();

                //todo: handle integration
                if (storageValue.includes("+") || storageValue.includes("-") || storageValue.includes("*") || storageValue.includes("/") || storageValue.includes("-")) {
                    this.costState.sections[sectionIndex].end_row.var_type = "formula";
                } else {
                    this.costState.sections[sectionIndex].end_row.var_type = "value";
                }

                try {
                    //update CostState
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                    this.updateDisplayedValues();

                } catch (e) {
                    console.log(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(actualSheet.sections[0].rows[variableIndex].value === this.costState.sections[0].rows[variableIndex].value)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("You can't enter an empty value. Please try again.");
            }
        },
        async updateAssumptionName(newName: string, variableIndex: number, sectionIndex: number) {
            if (newName.length > 0 && !useFormulaParser().charIsNumerical(newName[0])) {
                this.costState.assumptions[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(this.costState.assumptions[variableIndex].name === actualSheet.assumptions[variableIndex].name)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("A variable name must be longer than 0 and can't start with a number.");
            }
        },
        async updateSectionName(sectionIndex: number, newName: string) {
            if (newName.length > 0) {
                this.costState.sections[sectionIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(this.costState.sections[sectionIndex].name === actualSheet.sections[sectionIndex].name)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("The section name must be at least one character.");
            }
        },
        async updateVariableName(newName: string, variableIndex: number, sectionIndex: number) {
            if (newName.length > 0 && !useFormulaParser().charIsNumerical(newName[0])) {
                this.costState.sections[sectionIndex].rows[variableIndex].name = newName;
                try {
                    await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                } catch (e) {
                    console.log(e);
                    this.errorMessages.push(e);
                    //retrieve actual stored sheet from DB
                    //if actual sheet and state match, if not update state to actual sheet
                    const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                    if (!(this.costState.sections[sectionIndex].rows[variableIndex].name === actualSheet.sections[sectionIndex].rows[variableIndex].name)) {
                        this.costState = actualSheet;
                    }
                }
            } else {
                this.errorMessages.push("A variable name must be longer than 0 and can't start with a number.");
            }
        },
        async updateAssumptionSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces: number, startingAtInput: number, sectionIndex: number) {

            this.costState.assumptions[variableIndex].val_type = valTypeInput;
            this.costState.assumptions[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null || value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.costState.assumptions[variableIndex].value_1 = undefined;
                this.costState.assumptions[variableIndex].first_value_diff = false;
            } else {
                this.costState.assumptions[variableIndex].first_value_diff = true;
            }

            this.costState.assumptions[variableIndex].decimal_places = decimalPlaces;
            this.costState.assumptions[variableIndex].starting_at = startingAtInput;

            try {
                //update CostState
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                this.updateDisplayedValues();
            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions[variableIndex].value === this.costState.assumptions[variableIndex].value)) {
                    this.costState = actualSheet;
                }
            }
        },
        async updateVariableSettings(variableIndex: number, value1Input: string, valTypeInput: string, decimalPlaces: number, startingAtInput: number, sectionIndex: number) {

            this.costState.sections[sectionIndex].rows[variableIndex].val_type = valTypeInput;
            this.costState.sections[sectionIndex].rows[variableIndex].value_1 = value1Input;

            var value1OnlySpaces: boolean;

            try {
                value1OnlySpaces = value1Input.trim().length === 0;
            } catch (e) {
                //if it returns an error it means value_1 is undefined
                value1OnlySpaces = false;
            }

            if (value1Input === null || value1Input === undefined || value1Input === "" || value1OnlySpaces) {
                this.costState.sections[sectionIndex].rows[variableIndex].value_1 = undefined;
                this.costState.sections[sectionIndex].rows[variableIndex].first_value_diff = false;
            } else {
                this.costState.sections[sectionIndex].rows[variableIndex].first_value_diff = true;
            }

            this.costState.sections[sectionIndex].rows[variableIndex].decimal_places = decimalPlaces;
            this.costState.sections[sectionIndex].rows[variableIndex].starting_at = startingAtInput;

            try {
                //update CostState
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                //Update sheet values valuesToDisplay
                this.updateDisplayedValues();

            } catch (e) {
                console.log(e);
                this.errorMessages.push(e);
                //retrieve actual stored sheet from DB
                //if actual sheet and state match, if not update state to actual sheet
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows[variableIndex].value === this.costState.sections[sectionIndex].rows[variableIndex].value)) {
                    this.costState = actualSheet;
                }
            }
        },
        async deleteAssumption(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.costState.assumptions.splice(variableIndex, 1);
            this.assumptionValuesToDisplayState.splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.assumptions.length === this.costState.assumptions.length)) {
                    this.costState = actualSheet;
                    this.updateDisplayedValues();
                }
            }
        },
        async deleteEmployee(employeeIndex:number) {

            this.payrollState.employees.splice(employeeIndex, 1);

            try {
                this.payrollState = await useSheetUpdate().updatePayroll(this.route.params.modelId, this.payrollState.employees);
            } catch (e) {
                console.log(e);
                this.errorMessages.push("Could not delete employee! Please try again.");
                this.payrollState = await useSheetUpdate().getPayroll(this.route.params.modelId);
            }

        },
        async deleteSection(sectionIndex: number) {
            //first directly change the state
            this.costState.sections.splice(sectionIndex, 1)
            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
                this.updateDisplayedValues();
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.costState.sections[sectionIndex].rows.length)) {
                    this.costState = actualSheet;
                    this.updateDisplayedValues();
                }
            }
        },
        async deleteVariable(variableIndex: number, sectionIndex: number) {
            //first directly change the state
            this.costState.sections[sectionIndex].rows.splice(variableIndex, 1);
            this.variableValuesToDisplayState.get(sectionIndex).splice(variableIndex, 1);

            //then update the backend
            try {
                await useSheetUpdate().updateCostSheet(this.route.params.modelId, this.costState);
            } catch (e) {
                console.log(e) //todo: throw error message
                this.errorMessages.push(e);
                const actualSheet = await useSheetUpdate().getCostSheet(this.route.params.modelId);
                if (!(actualSheet.sections[sectionIndex].rows.length === this.costState.sections[sectionIndex].rows.length)) {
                    this.costState = actualSheet;
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
                this.assumptionValuesToDisplayState = useFormulaParser().getSheetRowValues(this.costState.assumptions);

                //Update entire sheet
                var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
                var endRowValuesStorage: string[][] = [];
                for (let i = 0; i < this.costState.sections.length; i++) {
                    //variables
                    var sectionVariables: Variable[] = [...this.costState.sections[i].rows];
                    var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(this.costState.assumptions.concat(sectionVariables))
                    valuesOfAssumptionsAndVariables.splice(0, this.costState.assumptions.length);
                    variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                    //endrow
                    var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.costState.assumptions.concat(sectionVariables.concat(this.costState.sections[i].end_row)));
                    valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.costState.assumptions.length);
                    endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);

                };
                this.variableValuesToDisplayState = variablesValuesStorage;
                this.endRowValuesToDisplayState = endRowValuesStorage;

            } catch (e) {
                console.log(e);
                this.errorMessages.push(e)
            }
        }
    },
    mounted() {
        try {
            //return the display values for all the assumptions
            const costs = useCostState();

            var assumptionValuesArray: string[][] = useFormulaParser().getSheetRowValues(costs.value.assumptions);
            useState('costAssumptionValues', () => assumptionValuesArray);

            var variablesValuesStorage: Map<number, string[][]> = new Map<number, string[][]>();
            var endRowValuesStorage: string[][] = [];
            for (let i = 0; i < costs.value.sections.length; i++) {
                //variables
                var sectionVariables: Variable[] = [...costs.value.sections[i].rows];
                var valuesOfAssumptionsAndVariables: string[][] = useFormulaParser().getSheetRowValues(costs.value.assumptions.concat(sectionVariables))
                valuesOfAssumptionsAndVariables.splice(0, costs.value.assumptions.length);
                variablesValuesStorage.set(i, valuesOfAssumptionsAndVariables);
                //endrow
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(costs.value.assumptions.concat(sectionVariables.concat(costs.value.sections[i].end_row)));
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + costs.value.assumptions.length);
                endRowValuesStorage.push(valuesOfVariablesAndEndRow[0]);
            };

            useState<Map<number, string[][]>>('costVariableValues', () => variablesValuesStorage);
            useState<string[][]>('costEndRowValues', () => endRowValuesStorage);

        } catch (e) {
            console.log(e);
            this.errorMessages.push(e)
        }
    }
}

</script>