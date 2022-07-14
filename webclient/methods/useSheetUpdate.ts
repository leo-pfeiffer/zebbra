import { useFetchAuth } from "./useFetchAuth";
import { Sheet } from "~~/types/Model";


export const useSheetUpdate = () => {

    var revenueSheet:Sheet = undefined;
    
    const getRevenueSheet = async (modelId: string | string[]) => {

        const getRevenues = await useFetchAuth(
            '/model/revenues', {
                method: 'GET',
            params: {
                model_id: modelId
            }
        }
        ).then((data: Sheet) => {
            revenueSheet = data;
        }).catch((error) => {
            throw error;
        });
    
        return revenueSheet;
    
    }

    const updateRevenueSheet = async (modelId: string | string[], revenueSheet: Sheet) => {

        const postRevenues = await useFetchAuth(
            '/model/revenues', {
                method: 'POST',
            params: {
                model_id: modelId
            },
            body: revenueSheet
        }).then((data:Sheet) => {
            revenueSheet = data;
        }).catch((error) => {
            throw error;
        });

        return revenueSheet;
    
    }

    return { getRevenueSheet, updateRevenueSheet }

}