import { useFetchAuth } from "~~/methods/useFetchAuth";
import { GetUserResponse } from "~~/types/GetUserResponse";
import { GetWorkspaceResponse } from "~~/types/GetWorkspaceResponse";

export const useIsWorkspaceAdmin = async () => {

    var userId: String;
    var adminId: String;

    //get the username and store it
    const getUserUsername = await useFetchAuth(
        '/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
            userId = data._id;

        }).catch((error) => {
          console.log(error);
          });
    
    //get the admins username and store it
    const getAdminUsername = await useFetchAuth(
        '/workspace',{ method: 'GET'}
    ).then((data:GetWorkspaceResponse) => {
        //get first workspace in response (user can only have one workspace)
        adminId = data[0].admin;
    }).catch((error) => {
        console.log(error);
        });

    //return if equals

    return (adminId === userId);
}