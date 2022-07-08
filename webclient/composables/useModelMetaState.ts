import { ModelMeta, Model } from "~~/types/Model"

var modelMetaState:ModelMeta;

export const useModelMetaState = () => useState<ModelMeta>('modelMetaState', () => modelMetaState);

export const getModelMeta = async (modelId: string | string[]) => {

    const getModel = await useFetchAuth(
        'http://localhost:8000/model', {
            method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: Model[]) => {
        modelMetaState = data[0].meta;
    }).catch((error) => {
        console.log(error);
    });

    return modelMetaState;

}