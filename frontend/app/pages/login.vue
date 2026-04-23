<template>
    <main class="flex-grow flex items-center justify-center px-gutter py-xl">
        <div class="w-full max-w-[440px]">
            <div class="bg-white border border-slate-200 rounded-lg p-lg md:p-xl shadow-xl relative overflow-hidden">
                <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60"></div>
                <div class="mb-xl">
                    <h2 class="font-display-lg text-headline-md text-on-surface mb-xs">Welcome Back</h2>
                    <p class="font-body-md text-slate-500">Enter your credentials to access the analytical dashboard.</p>
                </div>
                <form action="#" class="space-y-lg">
                <div class="space-y-sm">
                    <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="email">Email Address</label>
                    <div class="relative group">
                        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="mail">mail</span>
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="email" name="email" placeholder="name@precision-analytical.com" type="email"/>
                    </div>
                </div>
                <div class="space-y-sm">
                    <div class="flex justify-between items-center">
                        <label class="font-label-caps text-label-caps text-slate-600 block uppercase" for="password">Password</label>
                        <a class="text-label-sm font-label-sm text-secondary hover:text-secondary/80 transition-colors" href="#">Forgot Password?</a>
                    </div>
                    <div class="relative group">
                        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-secondary transition-colors" data-icon="lock">lock</span>
                        <input class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" id="password" name="password" placeholder="••••••••" type="password"/>
                        <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-on-surface transition-colors" type="button">
                            <span class="material-symbols-outlined text-[20px]" data-icon="visibility">visibility</span>
                        </button>
                    </div>
                </div>
                
                <!-- Sign In Button -->
                <button class="w-full bg-secondary hover:opacity-90 text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all active:scale-[0.98] flex items-center justify-center gap-2" type="submit">
                                        Sign In
                                        <span class="material-symbols-outlined text-[20px]" data-icon="login">login</span>
                </button>
                </form>
            </div>
            <p class="mt-lg text-center font-body-md text-slate-600">
                Don't have an account? 
                <NuxtLink class="text-secondary font-semibold hover:underline underline-offset-4 decoration-secondary/30 transition-all" to="/register">Sign Up</NuxtLink>
            </p>
        </div>
    </main>
</template>