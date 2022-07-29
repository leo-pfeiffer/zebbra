import { defineStore } from 'pinia'
import { GetIntegrationProvidersResponse } from '~~/types/GetIntegrationProvidersResponse';
import { useFetchAuth } from '~~/methods/useFetchAuth';

export const useIntegrationStore = defineStore('integrationStore', {
  state: () => ({
    piniaXeroStore: {} as GetIntegrationProvidersResponse,
    piniaGustoStore: {} as GetIntegrationProvidersResponse
  }),
  actions: {
    async updatePiniaIntegrationStore(workspaceId:string) {

      await useFetchAuth(
          '/integration/providers', {
          method: 'GET',
          params: {
              workspace_id: workspaceId
          }
      }
      ).then((data: GetIntegrationProvidersResponse[]) => {
        this.piniaXeroStore = data[0];
        this.piniaGustoStore = data[1];
      }).catch((error) => {
          console.log(error);
      });
    },
  }
})