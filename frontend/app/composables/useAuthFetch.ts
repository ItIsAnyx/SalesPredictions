export const useAuthFetch = () => {
  const baseFetch = useBaseFetch();
  const apiFetch = useApiFetch();

  return {
    login: (body: any) => baseFetch("/api/auth/login", { method: "POST", body }),
    register: (body: any) => baseFetch("/api/auth/register", { method: "POST", body }),
    me: () => apiFetch.request("/api/auth/me"),
    logout: () => baseFetch("/api/auth/logout", { method: "POST" }),
    refresh: () => baseFetch("/api/auth/refresh"),
  };
};