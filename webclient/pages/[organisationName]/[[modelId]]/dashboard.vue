<script setup lang="ts">
definePageMeta({
  middleware: ["auth", "route-check"]
})

const user = useUserState();

</script>

<template>
    <NuxtLayout name="navbar">
      <div class="h-full">
        <div class="p-3 border-b border-zinc-300 top-0 min-h-[60px] max-h-[60px]">
          <h1 class="font-semibold text-xl inline-block align-middle">Dashboard</h1>
        </div>

        <div class="grid grid-cols-2 gap-4 p-3">
          <div class="border">
            <ClientOnly>
              <apexchart
                  width="100%"
                  type="line"
                  :options="profitChartOptions"
                  :series="series"
              ></apexchart>
            </ClientOnly>
          </div>
          <div class="border">02</div>
          <div class="border">03</div>
          <div class="border">04</div>
          <div class="border">05</div>
          <div class="border">06</div>
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

export default {
  data() {
    return {
      showRequiresReconnectModal: false,
      series: [{
        name: "Profits",
        data: [
            [+ new Date(2020, 1, 1), 100],
            [+ new Date(2020, 2, 1), 200],
            [+ new Date(2020, 3, 1), 300],
            [+ new Date(2020, 4, 1), 200],
            [+ new Date(2020, 5, 1), 300],
            [+ new Date(2020, 6, 1), 400],
            [+ new Date(2020, 7, 1), 300],
        ]
      }],
    }
  },
  computed: {
    profitChartOptions() {
      return this.makeLineChartOptions('Profits', 'Profits')
    }
  },
  methods: {
    makeLineChartOptions(title, yAxisTitle) {
      return {
        chart: {
          type: 'line',
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
          title: {
            text: yAxisTitle
          },
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

    var integrationsProviderResponse: GetIntegrationProvidersResponse[];
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

    if(integrationsProviderResponse[0].requires_reconnect || integrationsProviderResponse[1].requires_reconnect) {
      this.showRequiresReconnectModal = true;
    } else {
      this.showRequiresReconnectModal = false;
    }
  }
}
</script>