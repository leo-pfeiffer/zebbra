<script setup lang="ts">

definePageMeta({
  middleware: ["auth", "route-check"]
})

</script>

<template>
  <NuxtLayout name="navbar">
    <div class="h-full overflow-y-auto" v-if="!dataIsLoading">
      <LoadingSpinner v-if="showLoading" :text="'Reloading the model'"></LoadingSpinner>
      <div class="py-3 border-b bg-white px-3 border-zinc-300 top-0 min-h-[70px] max-h-[70px] sticky z-40">
        <SheetHeader :user="piniaUserStore" :modelMeta="piniaModelMetaStore" :sheetName="'Dashboard'" :workspaceName="piniaUserStore.workspaces[0].name"
          :modelName="piniaModelMetaStore.name">
        </SheetHeader>
      </div>
      <div class="border-b border-zinc-300 py-8 p-2 mb-6 mx-14 flex flex-wrap md:flex-nowrap">
        <div class="min-w-fit mr-6">
          <p class="uppercase font-medium text-xs text-zinc-500 mb-2">Starting month:<InfoToggle v-if="!userIsViewer" :position="'inline'" :text="'Change the starting month of your model here.'"></InfoToggle></p>
          <div class="flex">
            <form @submit.prevent="updateStartingMonth">
              <input :disabled="userIsViewer" type="month" class="border border-zinc-300 rounded py-1 px-2 mr-2 text-sm text-zinc-700"
                name="starting-month" placeholder="Starting month" v-model="newStartingMonth.value">
              <button v-if="!userIsViewer" type="submit"
                class=" bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">
                Set
              </button>
            </form>
          </div>
        </div>
        <div class="min-w-fit">
          <p class="uppercase font-medium text-xs text-zinc-500 mb-2">Starting balance:<InfoToggle v-if="!userIsViewer" :position="'inline'" :text="'Set a starting balance to calculate your cash runway.'"></InfoToggle></p>
          <div class="flex">
            <form @submit.prevent="updateStartingBalance">
            <input :disabled="userIsViewer" type="number" class="border border-zinc-300 rounded py-1 px-2 mr-2 text-sm text-zinc-700"
              name="starting-balance" placeholder="Starting balance" v-model="startingBalance.value">
            <button v-if="!userIsViewer" type="submit"
              class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-sm px-2.5 py-1 border border-zinc-300 rounded text-zinc-700">
              Set
            </button>
            </form>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-x-12 gap-y-8 p-3 px-16">
        <div class="border border-zinc-300 rounded-md shadow-sm bg-white">
          <div
            class="w-full py-2 px-3 uppercase text-sm rounded-t-md bg-zinc-100 text-zinc-500 font-medium border-b border-zinc-300">
            Profitability
          </div>
          <div class="p-4">
            <ClientOnly>
              <apexchart v-if="renderChart" width="100%" type="line" :options="profitChartOptions"
                :series="dashboardData.profit"></apexchart>
            </ClientOnly>
          </div>
        </div>


        <div class="border border-zinc-300 rounded-md shadow-sm bg-white">
          <div
            class="w-full py-2 px-3 uppercase text-sm rounded-t-md bg-zinc-100 text-zinc-500 font-medium border-b border-zinc-300">
            Liquidity
          </div>
          <div class="p-4">
            <ClientOnly>
              <apexchart v-if="renderChart" width="100%" type="bar" :options="cashBalanceOptions"
                :series="dashboardData.cashBalance"></apexchart>
            </ClientOnly>
          </div>
        </div>
      </div>

      <div class="px-16 mt-8">
        <div class="border border-zinc-300 rounded-md shadow-sm bg-white">
          <div
            class="w-full py-2 px-3 uppercase text-sm rounded-t-md bg-zinc-100 text-zinc-500 font-medium border-b border-zinc-300">
            Income vs. Expenses
          </div>
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-x-12 gap-y-6">
            <div class="p-4">
              <ClientOnly>
                <apexchart v-if="renderChart" width="100%" type="area" :options="revenuesOptions"
                  :series="dashboardData.revenues"></apexchart>
              </ClientOnly>
            </div>
            <div class="py-4 px-4">
              <ClientOnly>
                <apexchart v-if="renderChart" width="100%" type="area" :options="costsOptions"
                  :series="dashboardData.costs">
                </apexchart>
              </ClientOnly>
            </div>
          </div>
        </div>
      </div>

      <div class="px-16 my-8">
        <div class="border border-zinc-300 rounded-md shadow-sm bg-white">
          <div
            class="w-full py-2 px-3 uppercase text-sm rounded-t-md bg-zinc-100 text-zinc-500 font-medium border-b border-zinc-300">
            Payroll
          </div>
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-x-12 gap-y-6">
            <div class="p-4">
              <ClientOnly>
                <apexchart v-if="renderChart" width="100%" type="area" :options="payrollCostsOptions"
                  :series="dashboardData.payrollCosts"></apexchart>
              </ClientOnly>
            </div>
            <div class="p-4">
              <ClientOnly>
                <apexchart v-if="renderChart" width="100%" type="bar" :options="headcountOptions"
                  :series="dashboardData.headcount"></apexchart>
              </ClientOnly>
            </div>
          </div>
        </div>
      </div>
      <Teleport to="body">
        <div v-if="showRequiresReconnectModal" class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
          <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
            <div>
              <h3 class="text-zinc-900 font-medium text-sm mb-2"><i
                  class="bi bi-exclamation-triangle text-red-600 mr-1"></i>One of your integrations requires a
                reconnect!</h3>
            </div>
            <p class="text-zinc-500 text-xs mb-3">Please head to the integrations settings and reconnect it, so we can
              be sure that the values are up to date.</p>
            <div class="float-right">
              <NuxtLink :to="`/${piniaUserStore.workspaces[0].name}/settings/integrations`">
                <button
                  class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700">Go
                  to Integrations</button>
              </NuxtLink>
            </div>
          </div>
        </div>
        <div v-show="showRequiresReconnectModal" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50">
        </div>
      </Teleport>

    </div>
  </NuxtLayout>
</template>

<script lang="ts">

import { GetIntegrationProvidersResponse } from '~~/types/GetIntegrationProvidersResponse';
import { useFetchAuth } from '~~/methods/useFetchAuth';
import { useCalculateDashboardProfits } from "~/methods/useCalculateDashboardProfits";
import { mapState, mapWritableState, mapActions } from 'pinia';
import { useUserStore } from '~~/store/useUserStore';
import { useCostStore } from '~~/store/useCostStore';
import { useRevenueStore } from '~~/store/useRevenueStore';
import { usePayrollStore } from '~~/store/usePayrollStore';
import { useModelMetaStore } from '~~/store/useModelMetaStore';
import { useSheetUpdate } from '~~/methods/useSheetUpdate';

export default {
  data() {
    return {

      startingBalance: {
        value: null
      },
      newStartingMonth: {
        value: null
      },

      showRequiresReconnectModal: false,

      renderChart: false,

      profitChartOptions: {},
      cashBalanceOptions: {},
      revenuesOptions: {},
      costsOptions: {},
      payrollCostsOptions: {},
      headcountOptions: {},

      dashboardData: null,

      defaultStatusMessage: "Up to date.",
      statusMessage: "Up to date.",
      showLoading: false,
      dataIsLoading: true,
      userIsViewer: false
    }
  },
  computed: {
    ...mapState(useUserStore, ['piniaUserStore']),
    ...mapWritableState(useModelMetaStore, ['piniaModelMetaStore']),
    ...mapWritableState(useCostStore, ['piniaCostStore']),
    ...mapWritableState(useRevenueStore, ['piniaRevenueStore']),
    ...mapWritableState(usePayrollStore, ['piniaPayrollStore']),
  },
  methods: {
    ...mapActions(useModelMetaStore, ['updatePiniaModelMetaStore']),
    ...mapActions(useUserStore, ['updatePiniaUserStore']),
    ...mapActions(useCostStore, ['setPiniaCostStore']),
    ...mapActions(useRevenueStore, ['setPiniaRevenueStore']),
    ...mapActions(usePayrollStore, ['setPiniaPayrollStore']),

    async updateStartingBalance() {

      const data = await useFetchAuth(
        '/model/startingBalance', {
        method: 'POST',
        params: {
          model_id: this.$route.params.modelId,
          starting_balance: this.startingBalance.value
        }
      }).then(async (data) => {
        console.log(data)
      }).catch((error) => {
        console.log(error);
      });

      await this.refreshModelData()
      this.calculateData()

    },

    async updateStartingMonth() {

      const data = await useFetchAuth(
        '/model/startingMonth', {
        method: 'POST',
        params: {
          model_id: this.$route.params.modelId,
          starting_month: `${this.newStartingMonth.value}-01`
        }
      }).then(async (data) => {
        console.log(data)
      }).catch((error) => {
        console.log(error);
      });

      await this.refreshModelData()
      this.calculateData()

    },

    getProfitChartOptions(showZeroLine: boolean) {
      const opts = this.makeChartOptions('Net Income')
      opts.subtitle = {
        text: 'Total net income per month',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };

      opts.stroke = {
        width: 2,
        curve: 'straight'
      }

      opts.colors = ['#0ea5e9']

      if (showZeroLine) {
        opts.annotations = {
          yaxis: [
            {
              y: 0,
              borderColor: '#000000',
            }
          ]
        }
      }

      return opts;
    },

    getCashBalanceOptions(showZeroLine: boolean) {
      const opts = this.makeChartOptions('Cash Balance');
      opts.subtitle = {
        text: 'Total cash reserves per month (approximated)',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };
      opts.plotOptions = {
        bar: {
          borderRadius: 0,
          colors: {
            ranges: [{
              from: 0,
              to: Infinity,
              color: '#22c55e'
            }, {
              from: -Infinity,
              to: 0,
              color: '#ef4444'
            }],
          },
        }
      }

      if (showZeroLine) {
        opts.annotations = {
          yaxis: [
            {
              y: 0,
              borderColor: '#000000',
            }
          ]
        }
      }

      return opts
    },

    getRevenuesOptions() {
      const opts = this.makeChartOptions('Total Revenues')
      opts.subtitle = {
        text: 'Total revenues per month & product',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };
      opts.chart.stacked = true;
      opts.stroke = {
        width: 2,
        curve: 'straight'
      }
      return opts;
    },

    getCostsOptions() {
      const opts = this.makeChartOptions('Total Costs');
      opts.subtitle = {
        text: 'Total costs per month & category',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };
      opts.chart.stacked = true;
      opts.stroke = {
        width: 2,
        curve: 'straight'
      }
      return opts;
    },

    getPayrollCostsOptions() {
      const opts = this.makeChartOptions('Total Payroll Costs');
      opts.subtitle = {
        text: 'Total costs related to payroll per month and department',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };
      opts.chart.stacked = true;
      opts.stroke = {
        width: 2,
        curve: 'straight'
      }
      return opts;
    },

    getHeadcountOptions() {
      const opts = this.makeChartOptions('Headcount');
      opts.subtitle = {
        text: 'Total employee headcount per month',
        style: {
          fontFamily: 'Inter',
          color: '#71717a'
        }

      };
      opts.chart.stacked = true;
      return opts;
    },

    makeChartOptions(title) {
      return {
        chart: {
          toolbar: {
            show: true,
            tools: {
              download: true,
              selection: false,
              zoom: false,
              zoomin: false,
              zoomout: false,
              pan: false,
              reset: false,
              customIcons: []
            },
          },
          fontFamily: 'Inter'
        },
        colors: [
          '#22c55e', '#0ea5e9', '#f59e0b', '#ef4444',
          '#14b8a6', '#6366f1', '#f97316', '#ec4899',
          '#84cc16', '#06b6d4', '#f43f5e', '#a855f7'
        ],
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          type: 'datetime',
          labels: {
            style: {
              fontSize: '11px',
              colors: ['#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a', '#71717a']
            }
          },
        },
        yaxis: {
          labels: {
            style: {
              fontSize: '11px',
              colors: ['#71717a']
            },
            formatter: function (val) {
              return (val).toFixed(0);
            },
          },
          title: {
            text: title,
            style: {
              color: '#71717a',
              fontWeight: 500,
              fontFamily: 'Inter'
            }
          },
        },
        tooltip: {
          style: {
            fontFamily: 'Inter',
            fontSize: '11px',
            colors: ['#71717a']
          },
          x: {
            show: true,
            format: 'MMM \'yy',
          },
          y: {
            formatter: function (val) {
              return (val).toFixed(0)
            }
          }
        },
        legend: {
          position: 'top',
          horizontalAlign: 'left',
          offsetX: 0,
          offsetY: -14
        },
        title: {
          text: title,
          style: {
            color: '#334155',
            fontWeight: 500,
            fontSize: '18px'
          },
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
      }
    },

    async refreshModelData() {

      this.statusMessage = "Refreshing models..."
      this.showLoading = true;

      try {
        await this.updatePiniaModelMetaStore(this.$route.params.modelId);
      } catch (error) {
        console.log(error);
      }

      try {
        this.piniaRevenueStore = await useSheetUpdate().getRevenueSheet(this.$route.params.modelId);
      } catch (error) {
        console.log(error);
      }

      try {
        this.piniaCostStore = await useSheetUpdate().getCostSheet(this.$route.params.modelId);
      } catch (e) {
        console.log(e)
      }

      try {
        this.piniaPayrollStore = await useSheetUpdate().getPayroll(this.$route.params.modelId);
      } catch (e) {
        console.log(e)
      }

      this.statusMessage = this.defaultStatusMessage;
      this.showLoading = false;

    },
    calculateData() {

      this.statusMessage = "Processing data..."
      this.showLoading = true;

      if (!this.piniaModelMetaStore.starting_month) {
        return
      }
      // convert the string date to a date object
      
      const dateParts = this.piniaModelMetaStore.starting_month.split('-');
      const startingDate = new Date(Number(dateParts[0]), Number(dateParts[1]) - 1, Number(dateParts[2]));
    

      // calculate the dashboard data
      const newDashboardData = useCalculateDashboardProfits(
        this.piniaRevenueStore, this.piniaCostStore, this.piniaPayrollStore, startingDate, this.startingBalance.value
      );

      this.dashboardData = { ...newDashboardData };

      const showZeroLine = (arr) => {
        const countNegative = (arr) => arr.filter(x => x < 0).length;
        const countPositive = (arr) => arr.filter(x => x > 0).length;
        return (countPositive(arr)) > 0 && (countNegative(arr) > 0)
      }

      // determine if we need to show the zero line
      const zeroLineProfit = showZeroLine(this.dashboardData.profit[0].data.map(e => e[1]))
      const zeroLineCash = showZeroLine(this.dashboardData.cashBalance[0].data.map(e => e[1]))

      this.profitChartOptions = { ...this.getProfitChartOptions(zeroLineProfit) };
      this.cashBalanceOptions = { ...this.getCashBalanceOptions(zeroLineCash) };
      this.revenuesOptions = { ...this.getRevenuesOptions() };
      this.costsOptions = { ...this.getCostsOptions() };
      this.payrollCostsOptions = { ...this.getPayrollCostsOptions() };
      this.headcountOptions = { ...this.getHeadcountOptions() };

      this.statusMessage = this.defaultStatusMessage
      this.showLoading = false;
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

      this.userIsViewer = this.piniaModelMetaStore.viewers.includes(this.piniaUserStore._id);
      this.startingBalance.value = this.piniaModelMetaStore.starting_balance;
      this.newStartingMonth.value = this.piniaModelMetaStore.starting_month.slice(0, 7);

      this.dataIsLoading = false;

      this.calculateData();

    } catch (e) {
      console.log(e);
    }

    // fixes rendering issue in apexcharts if width is not set to a fixed pixel width
    // https://github.com/apexcharts/apexcharts.js/issues/1077#issuecomment-984386146
    setTimeout(() => { this.renderChart = true }, 50)

    let integrationsProviderResponse: GetIntegrationProvidersResponse[];;
    const getIntegrationsState = await useFetchAuth(
      '/integration/providers', {
      method: 'GET',
      params: {
        workspace_id: this.piniaUserStore.workspaces[0]._id
      }
    }
    ).then((data: GetIntegrationProvidersResponse[]) => {
      integrationsProviderResponse = data;
    }).catch((error) => {
      console.log(error);
    });

    this.showRequiresReconnectModal = integrationsProviderResponse[0].requires_reconnect || integrationsProviderResponse[1].requires_reconnect;
  }
}
</script>