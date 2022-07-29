import { GetUserResponse } from '~~/types/GetUserResponse';
import { useFetchAuth } from '~~/methods/useFetchAuth';


//middleware that checks whether the route to be accessed matches the users workspace
export default defineNuxtRouteMiddleware( async (to, from) => {

    let user:GetUserResponse;

    try{

        await useFetchAuth(
            '/user', { method: 'GET' }
          ).then((data: GetUserResponse) => {
            user = data;
          }).catch((error) => {
            throw error
          });

    } catch(e) {
        navigateTo('/login')
        console.log("User state could not be accessed");
        console.log(e);
        //todo message
    }

    //const userWorkspace = user.value.workspaces[0].name;

    var userWorkspace:string;
    
    try {
        userWorkspace = user.workspaces[0].name;
    } catch(error) {
        navigateTo('/login')
        console.log("User state could not be accessed");
        console.log(error);
        //todo message
    }

    const path:string[] = to.fullPath.split("/");

                            //handle case where name includes a space (%20)
    if(!(userWorkspace === path[1].split("%20").join(" "))) {
        if(path.length === 2){
            navigateTo(`/${userWorkspace}`);
        } else if (path.length === 3) {
            navigateTo(`/${userWorkspace}/${path[2]}`);
        } else if (path.length === 4) {
            navigateTo(`/${userWorkspace}/${path[2]}/${path[3]}`);
        }
    }
});
