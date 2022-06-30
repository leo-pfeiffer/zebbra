

//middleware that checks whether the route to be accessed matches the users workspace
export default defineNuxtRouteMiddleware( async (to, from) => {

    await updateUserState();
    const user = useUserState();

    const userWorkspace = user.value.workspaces[0];
    const path = to.fullPath.split("/");

    if(!(userWorkspace === path[1])) {
        if(path.length === 2){
            navigateTo(`/${userWorkspace}`);
        } else if (path.length === 3) {
            navigateTo(`/${userWorkspace}/${path[2]}`);
        } else if (path.length === 4) {
            navigateTo(`/${userWorkspace}/${path[2]}/${path[3]}`);
        }
    }
});
