export interface GetUserResponse {
    _id: string;
    username: string;
    first_name: string;
    last_name: string;
    workspaces: string[];
    models: string[];
    disabled: boolean;
}
