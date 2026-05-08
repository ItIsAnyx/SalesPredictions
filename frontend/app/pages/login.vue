<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth";

const { login, isLoggedIn } = useAuth();
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
  loading.value = true;
  error.value = null;

  try {
    await login(email.value, password.value);

    await navigateTo("/");
  } catch (e) {
    error.value = "Invalid credentials";
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
    if (isLoggedIn.value) {
        await navigateTo("/");
    }
});
</script>

<template>
    <main class="flex-grow flex items-center justify-center">
        <div class="w-full max-w-[440px]">
            <div class="bg-white border border-slate-200 rounded-lg p-lg md:p-xl shadow-xl relative overflow-hidden">
                <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />
                <div class="mb-xl">
                    <h2 class="text-lg font-semibold text-on-surface mb-xs">Welcome Back</h2>
                    <p class="text-slate-500">Enter your credentials to access the analytical dashboard.</p>
                </div>
                <form class="space-y-lg" @submit.prevent="handleLogin">
                    <div class="space-y-sm">
                        <label class="text-slate-600 block" for="email">Email Address</label>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="mail">mail</span>
                            <input v-model="email" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="email" name="email" placeholder="name@precision-analytical.com" type="email"/>
                        </div>
                    </div>
                    <div class="space-y-sm">
                        <div class="flex justify-between items-center">
                            <label class="text-slate-600 block" for="password">Password</label>
                            <a class="text-label-sm font-label-sm text-secondary hover:text-secondary/80 transition-colors" href="#">Forgot Password?</a>
                        </div>
                        <div class="relative group">
                            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="lock">lock</span>
                            <input v-model="password" class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="password" name="password" placeholder="••••••••" type="password"/>
                            <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-on-surface transition-colors" type="button">
                                <span class="material-symbols-outlined text-[20px] w-full h-full item-center flex" data-icon="visibility">visibility</span>
                            </button>
                        </div>
                    </div>
                    
                    <!-- Sign In Button -->
                    <button
                        type="submit"
                        :disabled="loading"
                        class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                                hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        <span v-if="!loading" class="flex items-center gap-2">
                            Sign In
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
            <p class="mt-lg text-center text-slate-600">
                Don't have an account? 
                <NuxtLink class="text-secondary font-semibold hover:underline underline-offset-4 decoration-secondary/30 transition-all" to="/register">Sign Up</NuxtLink>
            </p>
        </div>
    </main>
</template>