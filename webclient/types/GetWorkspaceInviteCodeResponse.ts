export interface GetWorkspaceInviteCodeResponse {
    invite_code: string;
    workspace_id: string;
    expires: string;
    used_by: string;
}