export const useAuthFetch = () => {
  const api = useBaseFetch();

  return {
    login: (body: any) => api("/api/auth/login", { method: "POST", body }),
    register: (body: any) => api("/api/auth/register", { method: "POST", body }),
    me: () => api("/api/auth/me"),
    logout: () => api("/api/auth/logout", { method: "POST" }),
    refresh: () => api("/api/auth/refresh"),
  };
};