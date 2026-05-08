let refreshPromise: Promise<any> | null = null;

export const useApiFetch = () => {
  const api = useBaseFetch();

  const request = async (url: string, options: any = {}) => {
    try {
      return await api(url, options);
    } catch (error: any) {
      const status =
        error?.status ||
        error?.response?.status;

      if (status !== 401) {
        throw error;
      }

      try {
        if (!refreshPromise) {
          refreshPromise = api("/api/auth/refresh");
        }

        await refreshPromise;

        refreshPromise = null;

        return await api(url, options);
      } catch (refreshError) {
        refreshPromise = null;

        throw refreshError;
      }
    }
  };

  return { request };
};