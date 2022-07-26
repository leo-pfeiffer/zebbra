<script setup lang="ts">
import { Employee, Section, Variable } from '~~/types/Model';
import { useVariableSearchMap } from '~~/methods/useVariableSearchMap';
import { useVariableTimeSeriesMap } from '~~/methods/useVariableTimeSeriesMap';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { useGetPossibleIntegrationValues } from '~~/methods/useGetPossibleIntegrationValues';
import { ProfitLoss, Row } from '~~/types/ProfitLoss';
import { useFormulaParser } from '~~/methods/useFormulaParser';
import { useMathParser } from '~~/methods/useMathParser';

definePageMeta({
    middleware: ["auth", "route-check"]
})

const route = useRoute()

const userState = useUserState();

const modelMeta = useModelMetaState();
modelMeta.value = await getModelMeta(route.params.modelId);

const revenueState = useRevenueState();
try {
    revenueState.value = await useSheetUpdate().getRevenueSheet(route.params.modelId);
} catch (error) {
    console.log(error);
}

const costState = useCostState();
try {
    costState.value = await useSheetUpdate().getCostSheet(route.params.modelId);
} catch (e) {

}

const payrollState = usePayrollState();
try {
    payrollState.value = await useSheetUpdate().getPayroll(route.params.modelId);
} catch (e) {
    console.log(e)
}


//todo: find better solution
const date: string[] = modelMeta.value.starting_month.split("-");
const dates = useState('dates', () => useDateArray(new Date(+date[0], +date[1] - 1)));

</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div class="p-3 border-b border-zinc-300 top-0 min-h-[60px] max-h-[60px]">
                <h1 class="font-semibold text-xl inline-block align-middle">Profit & Loss Statement</h1>
            </div>
            <div class="ml-1 py-3 pl-2 mr-0 overflow-x-hidden min-h-[calc(100%-60px)] max-h-[calc(100%-60px)]">
                <ClientOnly>{{profitLoss}}</ClientOnly>
                <div class="flex">
                    <div>
                        <div id="model-headers">
                            <div>

                                <div
                                    class="group flex mt-6 text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                                    <span class="font-medium uppercase">
                                        Model
                                    </span>
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
                        <div id="model-values">
                            <div class="flex mt-6">
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <!-- Payroll -->
                            <div class="flex">
                                <!-- add section button empty -->
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-y"
                                    v-for="date in dates">X</div>
                            </div>
                        </div>
                        <div id="total-cost-values" class="border-zinc-300">
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

export default {
    data() {
        return {
            errorMessages: []
        }
    },
    methods: {
        closeErrorMessage(index: number) {
            this.errorMessages.splice(index, 1)
        },

    },
    computed: {
        profitLoss() {
            const emptyRow:Row = {
                name: "",
                values: []
            }
            
            var profitLoss: ProfitLoss = {
                gross_income: {
                    revenue_streams: [],
                    total: {...emptyRow}
                },
                cost_of_goods_sold: {...emptyRow},
                gross_margin: {...emptyRow},
                payroll_cost: {...emptyRow},
                operating_cost: {...emptyRow},
                operating_income: {...emptyRow},
                other_cost: {...emptyRow},
                net_income: {...emptyRow}
            }

            //pushing the endRowValues of each section into gross income
            for (let i = 0; i < this.revenueState.sections.length; i++) {
                var sectionVariables: Variable[] = [...this.revenueState.sections[i].rows];
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.revenueState.assumptions.concat(sectionVariables.concat(this.revenueState.sections[i].end_row)));
                
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.revenueState.assumptions.length);
                
                var rowStorage:Row = {
                    name: "",
                    values: []
                };
                rowStorage.name = this.revenueState.sections[i].name;
                rowStorage.values = valuesOfVariablesAndEndRow[0];
                profitLoss.gross_income.revenue_streams.push(rowStorage);
            };

            //calculating the total gross income
            var totalGrossIncome:string[] = [];
            for (let i=0; i < 24; i++) {
                var calcString:string = "";
                for(let j=0; j < profitLoss.gross_income.revenue_streams.length; j++) {
                    if(calcString.length === 0) {
                        calcString = calcString + profitLoss.gross_income.revenue_streams[j].values[i];
                    } else {
                        calcString = calcString + "+" + profitLoss.gross_income.revenue_streams[j].values[i];
                    }
                }

                var output:string;
                try {
                    output = useMathParser(calcString).toString();
                } catch(e) {
                    output = "#REF!"
                }
                totalGrossIncome.push(output);
            }
            profitLoss.gross_income.total.name = "Gross Income";
            profitLoss.gross_income.total.values = totalGrossIncome;

            //todo: getting the all the cost sections and storing them
            var costRowStorage: Row[] = [];
            for (let i = 0; i < this.costState.sections.length; i++) {
                var sectionVariables: Variable[] = [...this.costState.sections[i].rows];
                var valuesOfVariablesAndEndRow: string[][] = useFormulaParser().getSheetRowValues(this.costState.assumptions.concat(sectionVariables.concat(this.costState.sections[i].end_row)));
                
                valuesOfVariablesAndEndRow.splice(0, sectionVariables.length + this.costState.assumptions.length);
                
                var rowStorage:Row = {
                    name: "",
                    values: []
                };
                rowStorage.name = this.costState.sections[i].name;
                rowStorage.values = valuesOfVariablesAndEndRow[0];
                costRowStorage.push(rowStorage);
            };

            if(costRowStorage[0]) {
                profitLoss.cost_of_goods_sold = costRowStorage[0];
            }

            if(costRowStorage[1]) {
                profitLoss.operating_cost = costRowStorage[1];
            }

            if(costRowStorage[2]) {
                profitLoss.other_cost = costRowStorage[2];
            }
            
            //todo: calculating the gross margin

            var grossMargin:string[] = [];
            for (let i=0; i < 24; i++) {
                var calcString:string = profitLoss.gross_income.total.values[i] + "-" + profitLoss.cost_of_goods_sold.values[i];
                console.log(calcString)
                var output:string;
                try {
                    output = useMathParser(calcString).toString();
                } catch(e) {
                    output = "#REF!"
                }
                grossMargin.push(output);
            }
            profitLoss.gross_margin.name = "Gross Margin";
            profitLoss.gross_margin.values = grossMargin;

            //todo: getting the payroll costs

            var payrollCost:string[] = [];
            for(let i=0; i < this.payrollState.payroll_values.length; i++) {
                payrollCost.push(this.payrollState.payroll_values[i].value);
            }
            profitLoss.payroll_cost.name = "Payroll Cost";
            profitLoss.payroll_cost.values = payrollCost;

            //todo: calculating the operating income

            //todo: getting the other costs

            //todo: calculating the net income
            

            return profitLoss;
        }
    }
}

</script>