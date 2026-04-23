<template>
    <main class="flex-grow flex items-center justify-center px-gutter py-xl">
        <div class="w-full max-w-[440px]">
            <div class="bg-white border border-slate-200 rounded-lg p-lg md:p-xl shadow-xl relative overflow-hidden">
                <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60"></div>
                    <div class="mb-xl">
                        <h2 class="font-display-lg text-headline-md text-on-surface mb-xs">Join the Platform</h2>
                        <p class="font-body-md text-slate-500">Access analytical precision and real-time forecasts.</p>
                    </div>
                <form action="#" class="space-y-lg">
                <!-- Full Name Input -->
                <div class="space-y-sm">
                    <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="full_name">Full Name</label>
                    <div class="relative group">
                        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="person">person</span>
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="full_name" name="full_name" placeholder="John Doe" type="text"/>
                    </div>
                </div>
                <!-- Email Input -->
                <div class="space-y-sm">
                    <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="email">Email Address</label>
                    <div class="relative group">
                        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="mail">mail</span>
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="email" name="email" placeholder="name@example.com" type="email"/>
                    </div>
                </div>
                <!-- Password Input -->
                <div class="space-y-sm">
                    <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="password">Password</label>
                    <div class="relative group">
                        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="lock">lock</span>
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="password" name="password" placeholder="••••••••" type="password"/>
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
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="confirm_password" name="confirm_password" placeholder="••••••••" type="password"/>
                    </div>
                </div>
                <!-- Create Account Button -->
                <button class="w-full bg-secondary hover:opacity-90 text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all active:scale-[0.98] flex items-center justify-center gap-2" type="submit">
                    Create Account
                    <span class="material-symbols-outlined text-[20px]" data-icon="arrow_forward">arrow_forward</span>
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