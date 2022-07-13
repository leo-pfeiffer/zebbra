import { Sheet } from "~~/types/Model"

var revenueState: Sheet;

export const useRevenueState = () => useState<Sheet>('revenueState', () => revenueState);

export const getRevenueState = async (backendUrlBase:string, modelId: string | string[]) => {

    const getRevenues = await useFetchAuth(
        backendUrlBase + '/model/revenues', {
            method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: Sheet) => {
        revenueState = data;
    }).catch((error) => {
        throw error;
    });

    return revenueState;

}

export const updateRevenueState = async (backendUrlBase:string, modelId: string | string[], revenueSheet: Sheet) => {

    const postRevenues = await useFetchAuth(
        backendUrlBase + '/model/revenues', {
            method: 'POST',
        params: {
            model_id: modelId
        },
        body: revenueSheet
    }).then((data:Sheet) => {
        revenueState = data;
    }).catch((error) => {
        throw error;
    });

}