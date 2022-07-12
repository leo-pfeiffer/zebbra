import { ModelMeta } from "~~/types/Model"

var modelMetaState:ModelMeta;

export const useModelMetaState = () => useState<ModelMeta>('modelMetaState', () => modelMetaState);

export const getModelMeta = async (modelId: string | string[]) => {

    const getModel = await useFetchAuth(
        'http://localhost:8000/model/meta', {
            method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: ModelMeta) => {
        modelMetaState = data;
    }).catch((error) => {
        console.log(error);
    });

    return modelMetaState;

}