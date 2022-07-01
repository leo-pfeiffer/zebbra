export interface GetUserResponse {
    _id: string;
    username: string;
    first_name: string;
    last_name: string;
    workspaces: { _id: string, name: string }[];
    models: { _id: string, name: string }[];
}