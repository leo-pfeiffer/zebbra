import { useFetchAuth } from "./useFetchAuth";
import { IntegrationValueInfo } from "~~/types/IntegrationValueInfo";


export const useGetPossibleIntegrationValues = async (modelId: string | string[]) => {

    var integrationValuesArray: IntegrationValueInfo[] = undefined;

    await useFetchAuth(
        '/integration/dataEndpoints', {
        method: 'GET',
        params: {
            model_id: modelId
        }
    }
    ).then((data: IntegrationValueInfo[]) => {
        integrationValuesArray = data;
    }).catch((error) => {
        throw error;
    })

    return integrationValuesArray;

}