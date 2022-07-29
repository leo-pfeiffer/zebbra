import { defineStore } from 'pinia'
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { Sheet } from '~~/types/Model';

export const useRevenueStore = defineStore('revenueStore', {
  state: () => ({
    piniaRevenueStore: {} as Sheet,
  }),
  actions: {
    async setPiniaRevenueStore(modelId:string) {

      try {
        this.piniaRevenueStore = await useSheetUpdate().getRevenueSheet(modelId)
      } catch (e) {
        throw e
      }

    },
    async updatePiniaRevenueStore(modelId:string, revenuesIn:Sheet) {

      console.log("updatePiniaRevenueStore")

      try {
        this.piniaRevenueStore = await useSheetUpdate().updateRevenueSheet(modelId, revenuesIn)
      } catch (e) {
        throw e
      }

    },
  }
})