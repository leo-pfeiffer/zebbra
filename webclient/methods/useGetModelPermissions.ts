
import { useFetchAuth } from "./useFetchAuth";

export const useGetModelPermissions = async (modelId:string) => {

    var returnArray;

    try {
        await useFetchAuth(
            '/model/users', {
            method: 'GET',
            params: {
                model_id: modelId
            }
        }
        ).then((data) => {
            returnArray = data;
        })
    } catch (error) {
        throw error;
    }

    return returnArray;

}