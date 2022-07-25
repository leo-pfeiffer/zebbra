<script setup lang="ts">
definePageMeta({
  middleware: ["auth", "route-check"]
})

const user = useUserState();

const chartOptions = {
  chart: {
    id: 'vuechart-example',
  },
  xaxis: {
    categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
  },
};
const series = [
  {
    name: 'series-1',
    data: [30, 40, 35, 50, 49, 60, 70, 91],
  },
];

</script>

<template>
    <NuxtLayout name="navbar">
        <div>
            <h1>Model ID: {{ $route.params.modelId }}</h1>
            <p>Dashboard</p>
        </div>
        <ClientOnly>
          <apexchart
              width="500"
              type="bar"
              :options="chartOptions"
              :series="series"
          ></apexchart>
        </ClientOnly>


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

        
    </NuxtLayout>
</template>

<script lang="ts">

import { GetIntegrationProvidersResponse } from '~~/types/GetIntegrationProvidersResponse';
import { useFetchAuth } from '~~/methods/useFetchAuth';

export default {
  data() {
    return {
      showRequiresReconnectModal: false,
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