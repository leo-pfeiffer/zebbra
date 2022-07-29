import { defineStore } from 'pinia'
import { GetUserResponse } from '~~/types/GetUserResponse'
import { useFetchAuth } from '~~/methods/useFetchAuth';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    piniaUserStore: {} as GetUserResponse,
  }),
  actions: {
    async updatePiniaUserStore() {

      console.log("updatePiniaUserStore")

      await useFetchAuth(
        '/user', { method: 'GET' }
      ).then((data: GetUserResponse) => {
        this.piniaUserStore = data;
      }).catch((error) => {
        throw error
      });

    },
  }
})