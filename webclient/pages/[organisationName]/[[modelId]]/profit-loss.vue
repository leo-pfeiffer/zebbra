<script setup lang="ts">

definePageMeta({
    middleware: ["auth", "route-check"]
})

</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <LoadingSpinner v-if="dataIsLoading && !dataLoadingFailed" :text="'Loading'"></LoadingSpinner>
            <div class="h-full overflow-hidden" v-if="!dataIsLoading">
                <div class="py-3 border-b px-3 border-zinc-300 top-0 min-h-[70px] max-h-[70px]">
                    <SheetHeader :sheetName="'Profit & Loss'" :workspaceName="piniaUserStore.workspaces[0].name"
                        :modelName="piniaModelMetaStore.name"></SheetHeader>
                </div>
                <div class="ml-1 pl-2 flex top-0 bg-white pt-2 min-h-[50px] max-h-[50px]">
                    <div class="min-w-[300px] max-w-[300px]">
                    </div>
                    <div class="overflow-x-auto no-scrollbar z-10" id="dates"
                        @scroll="stickScroll('dates', 'table-right')">
                        <div class="border-zinc-300 flex">
                            <div class="first:border-l first:rounded-tl first:rounded-bl text-xs py-2 px-2 border-r border-y border-zinc-300 min-w-[75px] max-w-[75px] text-center uppercase bg-zinc-100 text-zinc-700"
                                v-for="date in dates">{{ date }}</div>
                        </div>
                    </div>
                </div>
                <div class="ml-1 pb-3 pl-2 mr-0 overflow-x-hidden min-h-[calc(100%-120px)] max-h-[calc(100%-120px)]">
                    <div class="flex">
                        <div>
                            <div
                                class="group flex text-xs text-zinc-500 rounded-tl py-2 px-3 min-w-[300px] max-w-[300px] bg-zinc-100 border-zinc-300 border-l border-t">
                                <span class="font-medium uppercase">
                                    Profit & Loss Statement
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-500 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-t border-l">
                                <span class="font-medium">
                                    Revenues
                                </span>
                            </div>
                            <div v-for="revenueStream in profitLoss.gross_income.revenue_streams"
                                class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-t border-l border-r">
                                <span class="pl-6">
                                    <li class="marker:text-zinc-500">{{ revenueStream.name }}</li>
                                </span>
                            </div>
                            <div
                                class="flex text-xs text-zinc-700 py-2 px-3 min-w-[300px] max-w-[300px] border-l border-y border-zinc-300 bg-zinc-50">
                                <span class="font-medium uppercase">
                                    {{ profitLoss.gross_income.total.name }}
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-500 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-l">
                                <span class="font-medium">
                                    Cost
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-t border-l border-r">
                                <span class="pl-5">
                                    <i class="bi bi-wallet-fill text-zinc-500 mr-2"></i>{{
                                            profitLoss.cost_of_goods_sold.name
                                    }}
                                </span>
                            </div>
                            <div
                                class="flex text-xs text-zinc-700 py-2 px-3 min-w-[300px] max-w-[300px] border-l border-y border-zinc-300 bg-zinc-50">
                                <span class="font-medium uppercase">
                                    {{ profitLoss.gross_margin.name }}
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-l border-r">
                                <span class="pl-5">
                                    <i class="bi bi-people-fill text-zinc-500 mr-2"></i>{{ profitLoss.payroll_cost.name
                                    }}
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[300px] max-w-[300px] border-zinc-300 border-t border-l border-r">
                                <span class="pl-5">
                                    <i class="bi bi-hammer text-zinc-500 mr-2"></i>{{ profitLoss.operating_cost.name }}
                                </span>
                            </div>
                            <div
                                class="flex text-xs text-zinc-700 py-2 px-3 min-w-[300px] max-w-[300px] border-l border-y border-zinc-300 bg-zinc-50">
                                <span class="font-medium uppercase">
                                    {{ profitLoss.operating_income.name }}
                                </span>
                            </div>
                            <div
                                class="group flex text-xs text-zinc-900 py-2 px-3 min-w-[300px]  max-w-[300px] border-zinc-300 border-l border-r">
                                <span class="pl-5">
                                    <i class="bi bi-layers-fill text-zinc-500 mr-2"></i>{{ profitLoss.other_cost.name }}
                                </span>
                            </div>
                            <div
                                class="flex text-xs text-zinc-900 rounded-bl py-2 px-3 min-w-[300px] max-w-[300px] bg-zinc-200 border-zinc-300 border-t-zinc-400 border-l border-b border-t-2">
                                <span class="font-medium uppercase">
                                    {{ profitLoss.net_income.name }}
                                </span>
                            </div>

                        </div>
                        <div id="table-right" class="overflow-x-auto" @scroll="stickScroll('table-right', 'dates')">
                            <div id="model-values" class="">
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 bg-zinc-100 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <!-- Revenues title -->
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <ClientOnly>
                                    <VariableRow v-for="revenueStream in profitLoss.gross_income.revenue_streams"
                                        :values="revenueStream.values" :round-to="2" :hierarchy="'low'"></VariableRow>
                                    <VariableRow :values="profitLoss.gross_income.total.values" :round-to="2"
                                        :hierarchy="'med'"></VariableRow>
                                </ClientOnly>
                                <!-- Costs title -->
                                <div class="flex">
                                    <div class="text-xs py-2 px-2 min-w-[75px] max-w-[75px] text-white/0 border-zinc-300 border-t"
                                        v-for="date in dates">X</div>
                                </div>
                                <ClientOnly>
                                    <VariableRow :values="profitLoss.cost_of_goods_sold.values" :round-to="2"
                                        :hierarchy="'low'"></VariableRow>
                                    <VariableRow :values="profitLoss.gross_margin.values" :round-to="2"
                                        :hierarchy="'med'"></VariableRow>
                                    <VariableRow :values="profitLoss.payroll_cost.values" :round-to="2"
                                        :hierarchy="'low'"></VariableRow>
                                    <VariableRow :values="profitLoss.operating_cost.values" :round-to="2"
                                        :hierarchy="'low'"></VariableRow>
                                    <VariableRow :values="profitLoss.operating_income.values" :round-to="2"
                                        :hierarchy="'med'"></VariableRow>
                                    <VariableRow :values="profitLoss.other_cost.values" :round-to="2"
                                        :hierarchy="'low'"></VariableRow>
                                    <VariableRow :values="profitLoss.net_income.values" :round-to="2"
                                        :hierarchy="'high'"></VariableRow>
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

import { mapState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useCostStore } from '~~/store/useCostStore';
import { useRevenueStore } from '~~/store/useRevenueStore';
import { usePayrollStore } from '~~/store/usePayrollStore';
import { useModelMetaStore } from '~~/store/useModelMetaStore';
import { useCalculateProfitLoss } from '~~/methods/useCalculateProfitLoss';
import { useDateArray } from '~~/methods/useDateArray';

export default {
    data() {
        return {
            errorMessages: [],
            dataIsLoading: true,
            dataLoadingFailed: false
        }
    },
    async mounted() {
        this.dataIsLoading = true;
        try {
            await this.updatePiniaUserStore();
            await this.updatePiniaModelMetaStore(this.$route.params.modelId);
            await this.setPiniaCostStore(this.$route.params.modelId);
            await this.setPiniaRevenueStore(this.$route.params.modelId);
            await this.setPiniaPayrollStore(this.$route.params.modelId);
            this.dataIsLoading = false;
        } catch (e) {
            this.errorMessages.push("Failed to load data. Please reload the page.");
            this.dataLoadingFailed = true;
            console.log(e);
        }

    },
    methods: {
        ...mapActions(useModelMetaStore, ['updatePiniaModelMetaStore']),
        ...mapActions(useUserStore, ['updatePiniaUserStore']),
        ...mapActions(useCostStore, ['setPiniaCostStore']),
        ...mapActions(useRevenueStore, ['setPiniaRevenueStore']),
        ...mapActions(usePayrollStore, ['setPiniaPayrollStore']),
        closeErrorMessage(index: number) {
            this.errorMessages.splice(index, 1)
        },
        stickScroll(idParent: string, idChild: string) {
            const scrollParent = document.querySelector(`#${idParent}`);
            const scrollChild = document.querySelector(`#${idChild}`);
            scrollChild.scrollLeft = scrollParent.scrollLeft;
        }

    },
    computed: {
        ...mapState(useUserStore, ['piniaUserStore']),
        ...mapState(useModelMetaStore, ['piniaModelMetaStore']),
        ...mapState(useCostStore, ['piniaCostStore']),
        ...mapState(useRevenueStore, ['piniaRevenueStore']),
        ...mapState(usePayrollStore, ['piniaPayrollStore']),
        dates() {

            if (this.piniaModelMetaStore.starting_month) {
                const date: string[] = this.piniaModelMetaStore.starting_month.split("-");
                return useDateArray(new Date(+date[0], +date[1] - 1))
            }
        },
        profitLoss() {
            return useCalculateProfitLoss(this.piniaRevenueStore, this.piniaCostStore, this.piniaPayrollStore);
        }
    }
}

</script>