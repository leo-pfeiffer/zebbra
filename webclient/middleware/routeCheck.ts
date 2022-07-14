//middleware that checks whether the route to be accessed matches the users workspace
export default defineNuxtRouteMiddleware( async (to, from) => {

    console.log("route check middleware");

    const user = useUserState();
    user.value = await updateUserState();

    //const userWorkspace = user.value.workspaces[0].name;

    var userWorkspace:string;
    
    try {
        userWorkspace = user.value.workspaces[0].name;
    } catch(error) {
        console.log("User state could not be accessed");
        console.log(error);
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
