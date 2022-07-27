<script setup lang="ts">

import { useSheetUpdate } from '~~/methods/useSheetUpdate';

definePageMeta({
  middleware: ["auth", "route-check"]
})

const route = useRoute()

const user = useUserState();

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
  console.log(e)
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
      <div class="h-full overflow-y-auto">
        <div class="py-3 border-b bg-white px-3 border-zinc-300 top-0 min-h-[70px] max-h-[70px] sticky z-40">
            <SheetHeader :sheetName="'Dashboard'" :workspaceName="user.workspaces[0].name" :modelName="modelMeta.name"></SheetHeader>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 p-3">
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="line"
                  :options="profitChartOptions"
                  :series="profitsSeries"
              ></apexchart>
            </ClientOnly>
          </div>
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="bar"
                  :options="cashBalanceOptions"
                  :series="cashBalanceSeries"
              ></apexchart>
            </ClientOnly>
          </div>
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="area"
                  :options="revenuesOptions"
                  :series="revenuesSeries"
              ></apexchart>
            </ClientOnly>
          </div>
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="area"
                  :options="costsOptions"
                  :series="costsSeries"
              ></apexchart>
            </ClientOnly>
          </div>
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="bar"
                  :options="payrollCostsOptions"
                  :series="payrollCostsSeries"
              ></apexchart>
            </ClientOnly>
          </div>
          <div>
            <ClientOnly>
              <apexchart
                  v-if="renderChart"
                  width="100%"
                  type="bar"
                  :options="headcountOptions"
                  :series="headcountSeries"
              ></apexchart>
            </ClientOnly>
          </div>
        </div>


        <Teleport to="body">
          <div v-if="showRequiresReconnectModal" class="absolute left-0 top-1/3 w-full flex justify-center align-middle">
            <div class="p-6 border h-max shadow-lg bg-white border-zinc-300 rounded z-50">
              <div>
                <h3 class="text-zinc-900 font-medium text-sm mb-2"><i class="bi bi-exclamation-triangle text-red-600 mr-1"></i>One of your integrations requires a reconnect!</h3>
              </div>
              <p class="text-zinc-500 text-xs mb-3">Please head to the integrations settings and reconnect it, so we can be sure that the values are up to date.</p>
              <div class="float-right">
                <NuxtLink :to="`/${user.workspaces[0].name}/settings/integrations`">
                  <button
                      class="bg-zinc-50 hover:bg-zinc-100 drop-shadow-sm shadow-inner shadow-zinc-50 font-medium text-xs px-2 py-1 border border-zinc-300 rounded text-zinc-700"
                  >Go to Integrations</button>
                </NuxtLink>
              </div>
            </div>
          </div>
          <div v-show="showRequiresReconnectModal" class="fixed top-0 left-0 w-[100vw] h-[100vh] z-0 bg-zinc-100/50"></div>
        </Teleport>

      </div>
    </NuxtLayout>
</template>

<script lang="ts">

import { GetIntegrationProvidersResponse } from '~~/types/GetIntegrationProvidersResponse';
import { useFetchAuth } from '~~/methods/useFetchAuth';
import {useCalculateDashboardProfits} from "~/methods/useCalculateDashboardProfits";

export default {
  data() {
    return {
      showRequiresReconnectModal: false,

      renderChart: false,

      profitChartOptions: {},
      cashBalanceOptions: {},
      revenuesOptions: {},
      costsOptions: {},
      payrollCostsOptions: {},
      headcountOptions: {},

      dashboardData: null,
    }
  },
  computed: {
    profitsSeries() {
      return this.dashboardData.profit;
    },
    cashBalanceSeries() {
      return this.dashboardData.cashBalance;
    },
    revenuesSeries() {
      return this.dashboardData.revenues;
    },
    costsSeries() {
      return this.dashboardData.costs;
    },
    payrollCostsSeries() {
      return this.dashboardData.payrollCosts;
    },
    headcountSeries() {
      return this.dashboardData.headcount;
    },
  },
  methods: {
    getProfitChartOptions() {
      return this.makeChartOptions('Profits', 'Profits')
    },
    getCashBalanceOptions() {
      const opts = this.makeChartOptions('Cash Balance', 'Cash Balance')
      opts.plotOptions = {
        bar: {
          colors: {
            ranges: [{
              from: -100,
              to: -46,
              color: '#F15B46'
            }, {
              from: -45,
              to: 0,
              color: '#FEB019'
            }]
          },
          columnWidth: '80%',
        }
      }
      return opts
    },
    getRevenuesOptions() {
      const opts = this.makeChartOptions('Revenues', 'Revenues')
      opts.chart.stacked = true;
      opts.chart.stackType = undefined;
      return opts;
    },
    getCostsOptions() {
      const opts = this.makeChartOptions('Costs', 'Costs')
      opts.chart.stacked = true;
      opts.chart.stackType = undefined;
      return opts;
    },
    getPayrollCostsOptions() {
      const opts = this.makeChartOptions('Payroll Costs', 'Payroll Costs')
      opts.chart.stacked = true;
      opts.chart.stackType = undefined;
      return opts;
    },
    getHeadcountOptions() {
      const opts = this.makeChartOptions('Headcount', 'Headcount')
      opts.chart.stacked = true;
      opts.chart.stackType = undefined;
      return opts;
    },
    makeChartOptions(title, yAxisTitle) {
      return {
        chart: {
          stackType: '100%',
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
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          width: 2,
          curve: 'straight'
        },
        xaxis: {
          categories: [],
          type: 'datetime',
        },
        yaxis: {
          labels: {
            formatter: function (val) {
              return (val).toFixed(0);
            },
          },
          title: {text: yAxisTitle},
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return (val).toFixed(0)
            }
          }
        },
        legend: {
          position: 'top',
          horizontalAlign: 'left',
          offsetX: 0
        },
        theme: {
          palette: 'palette10',
        },
        title: {text: title},
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
      }
    }
  },
  async mounted() {

    // convert the string date to a date object
    const dateParts = this.modelMeta.starting_month.split('-');
    const startingDate = new Date(Number(dateParts[0]), Number(dateParts[1]) - 1, Number(dateParts[2]));


    // calculate the dashboard data
    this.dashboardData = useCalculateDashboardProfits(
        this.revenueState, this.costState, this.payrollState, startingDate, 5000
    );

    this.profitChartOptions = {...this.getProfitChartOptions()};
    this.cashBalanceOptions = {...this.getCashBalanceOptions()};
    this.revenuesOptions = {...this.getRevenuesOptions()};
    this.costsOptions = {...this.getCostsOptions()};
    this.payrollCostsOptions = {...this.getPayrollCostsOptions()};
    this.headcountOptions = {...this.getHeadcountOptions()};

    // fixes rendering issue in apexcharts if width is not set to a fixed pixel width
    // https://github.com/apexcharts/apexcharts.js/issues/1077#issuecomment-984386146
    setTimeout(() => { this.renderChart = true }, 50)

    let integrationsProviderResponse: GetIntegrationProvidersResponse[];
    const getIntegrationsState = await useFetchAuth(
        '/integration/providers', {
        method: 'GET',
        params: {
            workspace_id: this.user.workspaces[0]._id
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