export interface GetUserResponse {
    _id: String;
    username: String;
    first_name: String;
    last_name: String;
    workspaces: String[];
    models: String[];
    disabled: Boolean;
}
