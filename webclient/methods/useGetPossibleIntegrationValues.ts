import { useFetchAuth } from "./useFetchAuth";
import { IntegrationValue } from "~~/types/IntegrationValue";


export const useGetPossibleIntegrationValues = async (modelId: string | string[]) => {

    var integrationValuesArray: IntegrationValue[] = undefined;

    await useFetchAuth(
        '/integration/dataEndpoints', {
        method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: IntegrationValue[]) => {
        integrationValuesArray = data;
    }).catch((error) => {
        throw error;
    })

    return integrationValuesArray;

}