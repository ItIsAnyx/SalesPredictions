export const useAuth = () => {
    const auth = useAuthFetch();

    const user = useState("user", () => null);
    const isLoggedIn = useState("isLoggedIn", () => false);

    const setUser = (data: any) => {
        user.value = data;
        isLoggedIn.value = !!data;
    };

    const login = async (email: string, password: string) => {
        const data = await auth.login({ email, password });
        setUser(data);
    };

    const register = async (
        first_name: string,
        last_name: string,
        login: string,
        email: string,
        password: string,
        repeat_password: string
    ) => {
        const data = await auth.register({ 
            first_name, 
            last_name, 
            login, 
            email, 
            password, 
            repeat_password 
        });

        console.log(data);

        setUser(data);
    };

    const fetchUser = async () => {
        try {
            const data = await auth.me();

            setUser(data);
        } catch {
            setUser(null);
        }
    };

    const refresh = async () => {
        await auth.refresh();
    };

    const logout = async () => {
        await auth.logout();

        setUser(null);
    };

    return { user, isLoggedIn, login, register, fetchUser, refresh, logout };
};