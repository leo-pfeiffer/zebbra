import { useFetchAuth } from "~~/methods/useFetchAuth";
import { GetUserResponse } from "~~/types/GetUserResponse";

var userInfo:GetUserResponse;

export const useUserState = () => useState<GetUserResponse>('userState', () => userInfo);

export const updateUserState = async () => {
  
    const request = await useFetchAuth(
      '/user',{ method: 'GET'}
        ).then((data:GetUserResponse) => {
          userInfo = data;
        }).catch((error) => {
          console.log(error);
          });
    
    return userInfo;

}