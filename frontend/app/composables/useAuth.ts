import { ref } from "vue";

const user = ref();
const isLoggedIn = ref(false);

export const useAuth = () => {
    const login = async (email: string, password: string) => {
        // await $fetch("/api/auth/login", {
        //     method: "POST",
        //     body: { email, password },
        //     credentials: "include"
        // });

        await fetchUser();
    };

    const register = async (firstName: string, lastName: string, email: string, password: string, repeatPassword: string) => {
        // await $fetch("/api/auth/register", {
        //     method: "POST",
        //     body: { firstName, lastName, email, password, repeatPassword },
        //     credentials: "include"
        // });
        
        await fetchUser();
    }

    const fetchUser = async () => {
        try {
            // const data = await $fetch("/api/me", {
            //     credentials: "include"
            // });

            const data = {
                id: 1,
                name: "Alex",
                role: "admin",
                email: "alex@mail.com"
            };

            user.value = data;
            isLoggedIn.value = true;
        } catch (e) {
            user.value = null;
            isLoggedIn.value = false;
        }
    };

    const logout = async () => {
        // await $fetch("/api/auth/logout", {
        //     method: "POST",
        //     credentials: "include"
        // });
        user.value = null;
        isLoggedIn.value = false;
    }

    return { user, isLoggedIn, login, register, fetchUser, logout }
};