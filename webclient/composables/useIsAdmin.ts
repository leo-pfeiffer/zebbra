import { useFetchAuth } from "./useFetchAuth"

export const useIsAdmin = async () => {

    var userUsername: String;
    var adminUsername: String;

    type GetUserResponse = {
        username: String;
        first_name: String;
        last_name: String;
        workspaces: String[];
        disabled: Boolean;
    }

    type GetWorkspaceResponse = {
        name: String;
        admin: String;
        users: String[];
    }

    //get the username and store it
    const getUserUsername = await useFetchAuth(
        'http://localhost:8000/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
          console.log(data);
          userUsername = data.username;

        }).catch((error) => {
          console.log(error);
          });
    
    //get the admins username and store it
    const getAdminUsername = await useFetchAuth(
    'http://localhost:8000/workspace',{ method: 'GET'}
    ).then((data:GetWorkspaceResponse) => {
        console.log(data);
        adminUsername = data[0].admin;
    }).catch((error) => {
        console.log(error);
        });

    //return if equals

    return (adminUsername === userUsername);
}