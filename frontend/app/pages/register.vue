<script setup> 
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth";

const { register, isLoggedIn } = useAuth();

const router = useRouter();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const repeatPassword = ref("");

const loading = ref(false);
const error = ref(null);

const handleRegister = async () => {
    loading.value = true;
    error.value = null;

    try {
        await register(firstName.value, lastName.value, email.value, password.value, repeatPassword.value);

        router.push("/");
    } catch (e) {
        error.value = "Invalid Credentials";
    } finally {
        loading.value = false;
    }
};

// onMounted(() => {
//     if (isLoggedIn) {
//         router.push("/");
//     }
// });
</script>

<template>
    <main class="flex-grow flex items-center justify-center px-gutter py-xl">
        <div class="w-full max-w-[440px]">
            <div class="bg-white border border-slate-200 rounded-lg p-lg md:p-xl shadow-xl relative overflow-hidden">
                <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />
                <div class="mb-xl">
                    <h2 class="font-display-lg text-headline-md text-on-surface mb-xs">Join the Platform</h2>
                    <p class="font-body-md text-slate-500">Access analytical precision and real-time forecasts.</p>
                </div>
                <form class="space-y-lg" @submit.prevent="handleRegister">
                    <!-- First Name Input -->
                    <div class="space-y-sm">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="full_name">First Name</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="person">person</span>
                            <input v-model="firstName" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="first_name" name="first_name" placeholder="John" type="text"/>
                        </div>
                    </div>
                    <!-- Last Name Input -->
                    <div class="space-y-sm">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="full_name">Second Name</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="person">person</span>
                            <input v-model="lastName" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="last_name" name="last_name" placeholder="Doe" type="text"/>
                        </div>
                    </div>
                    <!-- Email Input -->
                    <div class="space-y-sm">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="email">Email Address</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="mail">mail</span>
                            <input v-model="email" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="email" name="email" placeholder="name@example.com" type="email"/>
                        </div>
                    </div>
                    <!-- Password Input -->
                    <div class="space-y-sm">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="password">Password</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="lock">lock</span>
                            <input v-model="password" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="password" name="password" placeholder="••••••••" type="password"/>
                            <button class="absolute items-center h-full right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-on-surface transition-colors" type="button">
                                <span class="flex material-symbols-outlined text-[20px]" data-icon="visibility">visibility</span>
                            </button>
                        </div>
                    </div>
                    <!-- Confirm Password Input -->
                    <div class="space-y-sm">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="confirm_password">Confirm Password</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="verified_user">verified_user</span>
                            <input v-model="repeatPassword" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="confirm_password" name="confirm_password" placeholder="••••••••" type="password"/>
                        </div>
                    </div>
                    <!-- Create Account Button -->
                    <button
                        type="submit"
                        :disabled="loading"
                        class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                                hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                        <span v-if="!loading" class="flex items-center gap-2">
                            Sign Up
                            <span class="material-symbols-outlined text-[20px]">login</span>
                        </span>

                        <span v-else class="flex items-center gap-2">
                            <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                            <circle
                                class="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="white"
                                stroke-width="4"
                                fill="none"
                            />
                            <path
                                class="opacity-75"
                                fill="white"
                                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                            />
                            </svg>
                            Loading...
                        </span>
                    </button>
                </form>
            </div>
            <p class="mt-lg text-center font-body-md text-slate-600">
                Already have an account? 
                <NuxtLink class="text-secondary font-semibold hover:underline underline-offset-4 decoration-secondary/30 transition-all" to="/login">Login</NuxtLink>
            </p>
        </div>
    </main>
</template>