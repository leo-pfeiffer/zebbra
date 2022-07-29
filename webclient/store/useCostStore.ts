import { defineStore } from 'pinia'
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { Sheet } from '~~/types/Model';

export const useCostStore = defineStore('costStore', {
  state: () => ({
    piniaCostStore: {} as Sheet,
  }),
  actions: {
    async setPiniaCostStore(modelId:string) {

      try {
        this.piniaCostStore = await useSheetUpdate().getCostSheet(modelId)
      } catch (e) {
        throw e
      }

    },
    async updatePiniaCostStore(modelId:string, costsIn:Sheet) {

      try {
        this.piniaCostStore = await useSheetUpdate().updateCostSheet(modelId, costsIn)
      } catch (e) {
        throw e
      }

    },
  }
})