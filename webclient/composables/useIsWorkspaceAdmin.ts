import { useFetchAuth } from "./useFetchAuth"

import { GetUserResponse } from "~~/types/GetUserResponse";
import { GetWorkspaceResponse } from "~~/types/GetWorkspaceResponse";

export const useIsWorkspaceAdmin = async () => {

    var userUsername: String;
    var adminUsername: String;

    //get the username and store it
    const getUserUsername = await useFetchAuth(
        'http://localhost:8000/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
          userUsername = data.username;

        }).catch((error) => {
          console.log(error);
          });
    
    //get the admins username and store it
    const getAdminUsername = await useFetchAuth(
    'http://localhost:8000/workspace',{ method: 'GET'}
    ).then((data:GetWorkspaceResponse) => {
        adminUsername = data[0].admin;
    }).catch((error) => {
        console.log(error);
        });

    //return if equals

    return (adminUsername === userUsername);
}