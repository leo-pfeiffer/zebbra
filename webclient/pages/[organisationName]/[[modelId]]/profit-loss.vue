<script setup lang="ts">

import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { useCalculateProfitLoss } from '~~/methods/useCalculateProfitLoss';

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

</script>

<template>
    <NuxtLayout name="navbar">
        <div class="h-full">
            <div class="p-3 border-b border-zinc-300 top-0 min-h-[60px] max-h-[60px]">
                <h1 class="font-semibold text-xl inline-block align-middle">Profit & Loss</h1>
            </div>
            <div class="ml-1 py-3 pl-2 mr-0 overflow-x-hidden min-h-[calc(100%-60px)] max-h-[calc(100%-60px)]">
                <div class="flex">
                    <div>
                        <div
                            class="group flex mt-6 text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-100 border-zinc-300 border-l border-t">
                            <span class="font-medium uppercase">
                                Profit & Loss Statement
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="font-medium">
                                Revenues
                            </span>
                        </div>
                        <div v-for="revenueStream in profitLoss.gross_income.revenue_streams"
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="pl-6">
                                {{revenueStream.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r bg-zinc-100">
                            <span class="font-medium uppercase">
                                {{profitLoss.gross_income.total.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="font-medium">
                                Costs
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="pl-6">
                                {{profitLoss.cost_of_goods_sold.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r bg-zinc-100">
                            <span class="font-medium uppercase">
                                {{profitLoss.gross_margin.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="pl-6">
                                {{profitLoss.payroll_cost.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="pl-6">
                                {{profitLoss.operating_cost.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r bg-zinc-100">
                            <span class="font-medium uppercase">
                                {{profitLoss.operating_income.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[470px] max-w-[470px] border-zinc-300 border-t border-l border-r">
                            <span class="pl-6">
                                {{profitLoss.other_cost.name}}
                            </span>
                        </div>
                        <div
                            class="group flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[470px] max-w-[470px] bg-zinc-200 border-zinc-300 border border-y-2">
                            <span class="font-medium uppercase">
                                {{profitLoss.net_income.name}}
                            </span>
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
                            <!-- Revenues title -->
                            <div class="flex">
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                    v-for="date in dates">X</div>
                            </div>
                            <ClientOnly>
                                <VariableRow v-for="revenueStream in profitLoss.gross_income.revenue_streams" :values="revenueStream.values" :round-to="2" :isFinalRow="false"></VariableRow>
                                <VariableRow :values="profitLoss.gross_income.total.values" :round-to="2" :isFinalRow="true"></VariableRow>
                            </ClientOnly>
                            <!-- Costs title -->
                            <div class="flex">
                                <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300"
                                    v-for="date in dates">X</div>
                            </div>
                            <ClientOnly>
                                <VariableRow :values="profitLoss.cost_of_goods_sold.values" :round-to="2" :isFinalRow="false"></VariableRow>
                                <VariableRow :values="profitLoss.gross_margin.values" :round-to="2" :isFinalRow="true"></VariableRow>
                                <VariableRow :values="profitLoss.payroll_cost.values" :round-to="2" :isFinalRow="false"></VariableRow>
                                <VariableRow :values="profitLoss.operating_cost.values" :round-to="2" :isFinalRow="false"></VariableRow>
                                <VariableRow :values="profitLoss.operating_income.values" :round-to="2" :isFinalRow="true"></VariableRow>
                                <VariableRow :values="profitLoss.other_cost.values" :round-to="2" :isFinalRow="false"></VariableRow>
                                <VariableRow :values="profitLoss.net_income.values" :round-to="2" :isFinalRow="true"></VariableRow>
                            </ClientOnly>
                            
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
        dates() {
            const date: string[] = this.modelMeta.starting_month.split("-");
            return useDateArray(new Date(+date[0], +date[1] - 1))
        },
        profitLoss() {
            return useCalculateProfitLoss(this.revenueState, this.costState, this.payrollState);
        }
    }
}

</script>