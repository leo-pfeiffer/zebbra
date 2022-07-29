import { defineStore } from 'pinia'
import { IntegrationValueInfo } from "~~/types/IntegrationValueInfo";
import { useGetPossibleIntegrationValues } from '~~/methods/useGetPossibleIntegrationValues';

export const usePossibleIntegrationsStore = defineStore('possibleIntegrationsStore', {
  state: () => ({
    piniaPossibleIntegrationsStore: [] as IntegrationValueInfo[],
  }),
  actions: {
    async setPossibleIntegrationsStore(modelId: string) {
      try {
        this.piniaPossibleIntegrationsStore = await useGetPossibleIntegrationValues(modelId);
      } catch (e) {
        throw e
      }
    },
  }
})