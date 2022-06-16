//adapted from: https://github.com/nuxt/framework/discussions/3801

export const useProfile = () => {
    const token = useState<string>("token");
  
    const setToken = (value: string) => {
      token.value = value;
    };

    const removeToken = () => {
        token.value = null;
      };
  
    return { id: null, name: null, token, setToken, removeToken };
  };
