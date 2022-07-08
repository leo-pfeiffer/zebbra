import { Sheet } from "~~/types/Model"

var revenueState: Sheet;

export const useRevenueState = () => useState<Sheet>('revenueState', () => revenueState);

export const getRevenueState = async (modelId: string | string[]) => {

    const getRevenues = await useFetchAuth(
        'http://localhost:8000/model/revenues', {
            method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: Sheet) => {
        revenueState = data;
    }).catch((error) => {
        console.log(error);
    });

    return revenueState;

}

export const updateRevenueState = async (modelId: string | string[], revenueSheet: Sheet) => {

    const postRevenues = await useFetchAuth(
        'http://localhost:8000/model/revenues', {
            method: 'POST',
        params: {
            model_id: modelId
        },
        body: revenueSheet
    }).then((data:Sheet) => {
        revenueState = data;
    }).catch((error) => {
        console.log(error);
    });

}