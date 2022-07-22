import { useFetchAuth } from "./useFetchAuth";
import { Sheet } from "~~/types/Model";


export const useSheetUpdate = () => {

    var revenueSheet:Sheet = undefined;
    var costSheet:Sheet = undefined;

    
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

    const updateRevenueSheet = async (modelId: string | string[], revenueSheetIn: Sheet) => {

        const postRevenues = await useFetchAuth(
            '/model/revenues', {
                method: 'POST',
            params: {
                model_id: modelId
            },
            body: revenueSheetIn
        }).then((data:Sheet) => {
            revenueSheet = data;
        }).catch((error) => {
            throw error;
        });

        return revenueSheet;
    
    }

    const getCostSheet = async (modelId: string | string[]) => {

        const getCosts = await useFetchAuth(
            '/model/costs', {
                method: 'GET',
            params: {
                model_id: modelId
            }
        }
        ).then((data: Sheet) => {
            costSheet = data;
        }).catch((error) => {
            throw error;
        });
    
        return costSheet;
    
    }

    const updateCostSheet = async (modelId: string | string[], costSheetIn: Sheet) => {

        const postCosts = await useFetchAuth(
            '/model/costs', {
                method: 'POST',
            params: {
                model_id: modelId
            },
            body: costSheetIn
        }).then((data:Sheet) => {
            costSheet = data;
        }).catch((error) => {
            throw error;
        });

        return costSheet;
    
    }

    return { getRevenueSheet, updateRevenueSheet, getCostSheet, updateCostSheet }

}