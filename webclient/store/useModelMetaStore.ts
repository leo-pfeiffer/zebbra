import { defineStore } from 'pinia'
import { useFetchAuth } from '~~/methods/useFetchAuth';
import { ModelMeta } from '~~/types/Model';

export const useModelMetaStore = defineStore('modelMetaStore', {
  state: () => ({
    piniaModelMetaStore: {} as ModelMeta,
  }),
  actions: {
    async updatePiniaModelMetaStore(modelId: string) {

      await useFetchAuth(
        '/model/meta', {
        method: 'GET',
        params: {
          model_id: modelId
        }
      }
      ).then((data: ModelMeta) => {
        this.piniaModelMetaStore = data;
      }).catch((error) => {
        console.log(error);
      });
    },
  }
})