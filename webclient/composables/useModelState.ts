import { Model } from "~~/types/Model"

var modelState:Model;

export const useModelState = () => useState<Model>('modelState', () => modelState);

export const updateModelState = async (modelId:string | string[]) => {

    const getModel = await useFetchAuth(
        'http://localhost:8000/model',{ method: 'GET',
        params: {
            model_id: modelId
        }}
        ).then((data:Model[]) => {
            modelState = data[0];
        }).catch((error) => {
          console.log(error);
          });
    
    return modelState;

}