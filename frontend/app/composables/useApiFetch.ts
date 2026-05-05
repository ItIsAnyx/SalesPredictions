export const useApiFetch = () => {
  const api = useBaseFetch();
  const authApi = useAuthFetch();
  const router = useRouter();

  let isRefreshing = false;

  const request = async (url: string, options: any = {}) => {
    try {
      return await api(url, options);
    } catch (error: any) {
      const status = error?.status || error?.response?.status;

      if (status !== 401) throw error;

      if (isRefreshing) {
        await new Promise(resolve => setTimeout(resolve, 300));
        return api(url, options);
      }

      isRefreshing = true;

      try {
        await authApi.refresh();

        isRefreshing = false;

        return await api(url, options);
      } catch (refreshError) {
        isRefreshing = false;

        await router.push("/login");
        throw refreshError;
      }
    }
  };

  return { request };
};