import { defineStore } from 'pinia'
import { useSheetUpdate } from '~~/methods/useSheetUpdate';
import { Payroll } from '~~/types/Model';

export const usePayrollStore = defineStore('payrollStore', {
  state: () => ({
    piniaPayrollStore: {} as Payroll,
  }),
  actions: {
    async setPiniaPayrollStore(modelId:string) {

      try {
        this.piniaPayrollStore = await useSheetUpdate().getPayroll(modelId);
      } catch (e) {
        throw e
      }

    },
  }
})