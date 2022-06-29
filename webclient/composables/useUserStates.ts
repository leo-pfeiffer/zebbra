import { GetUserResponse } from "~~/types/GetUserResponse"

var userInfo:GetUserResponse;

export const updateUserState = async () => {

    const request = await useFetchAuth(
        'http://localhost:8000/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
          userInfo = data;
        }).catch((error) => {
          console.log(error);
          });
    
    return userInfo;

}

export const useUserState = () => useState<GetUserResponse>('userState', () => userInfo);