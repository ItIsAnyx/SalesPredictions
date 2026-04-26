<script setup>
import { useAuth } from '@/composables/useAuth';

const { user, isLoggedIn } = useAuth();

const props = defineProps({
  open: Boolean
})

const emit = defineEmits(['toggle-sidebar'])
</script>

<template>
  <header :class="['fixed top-0 right-0 z-50 bg-white border-b border-slate-200 flex justify-between items-center w-full px-4 h-16',
    open ? 'pl-[276px]' : '']">
    <div class="flex items-center gap-sm">
      <button @click="emit('toggle-sidebar')" class="p-2 hover:bg-slate-50 rounded-lg">
        <span class="material-symbols-outlined flex w-full h-full text-slate-900">menu</span>
      </button>
      <NuxtLink to="/">
        <span :class="['font-manrope font-black text-slate-900 text-lg tracking-tight',
        open ? 'hidden' : '']">
          SalesPrediction
        </span>
      </NuxtLink>  
    </div>
    <nav :class="['hidden md:flex items-center gap-xl', open ? 'md:hidden' : '']">
      <NuxtLink 
        class="font-manrope text-sm font-medium text-slate-500 hover:text-teal-600 transition-colors" 
        to="/dashboard"
        active-class="text-teal-600">
        Dashboard
      </NuxtLink>
      <NuxtLink 
        class="font-manrope text-sm font-medium text-slate-500 hover:text-teal-600 transition-colors" 
        to="/products"
        active-class="text-teal-600">
        All Products
      </NuxtLink>
      <NuxtLink 
        class="font-manrope text-sm font-medium text-slate-500 hover:text-teal-600 transition-colors" 
        to="/about"
        active-class="text-teal-600">
        About Us
      </NuxtLink>
    </nav>
    <div v-if="isLoggedIn" >
        <NuxtLink to="/me">
          <div class="w-8 h-8 rounded-full bg-slate-200 overflow-hidden border border-slate-300" />
        </NuxtLink>
    </div>
    <div v-else class="flex items-center gap-md">
        <NuxtLink class="hidden sm:block px-4 py-2 font-manrope text-sm font-bold text-slate-900" to="/login">Login</NuxtLink>
        <NuxtLink class="px-4 py-2 bg-[#0D9488] text-white rounded font-manrope text-sm font-bold shadow-sm" to="/register">Register</NuxtLink>
    </div>
  </header>
</template>