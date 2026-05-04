<script setup>
import { onClickOutside } from "@vueuse/core";
import { ref } from "vue";
import { useAuth } from '@/composables/useAuth';

const { isLoggedIn, logout } = useAuth();

const props = defineProps({
  open: Boolean
})

const emit = defineEmits(['toggle-sidebar'])

const menuOpen = ref(false);
const menuRef = ref(null);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const handleLogout = async () => {
  await logout();
  toggleMenu();
}

onClickOutside(menuRef, () => {
  menuOpen.value = false;
})
</script>

<template>
  <header :class="['fixed top-0 right-0 z-50 bg-white border-b border-slate-200 w-full h-16 px-4 flex items-center', open ? 'pl-[276px]' : '']">
    <div class="flex justify-between item-center w-full">
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
      <div v-if="isLoggedIn" class="flex items-center">
        <div class="relative" ref="menuRef">
          <button @click="toggleMenu" class="flex items-center w-8 h-8 rounded-full bg-slate-200 border border-slate-300 overflow-hidden" />
        
          <div
            v-if="menuOpen"
            class="absolute right-0 mt-2 w-40 bg-white border border-slate-200 rounded-lg shadow-lg py-1 z-50"
          >
            <NuxtLink
              to="/me"
              class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50"
              @click="menuOpen = false"
            >
              Profile
            </NuxtLink>

            <button
              @click="handleLogout"
              class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-slate-50"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
      <div v-else class="flex items-center gap-md">
          <NuxtLink class="px-4 py-2 font-manrope text-sm font-bold text-slate-900" to="/login">Login</NuxtLink>
          <NuxtLink class="px-4 py-2 bg-secondary text-white rounded font-manrope text-sm font-bold shadow-sm" to="/register">Register</NuxtLink>
      </div>
    </div>
    <nav :class="['hidden md:fixed md:flex top-0 left-1/2 -translate-x-1/2 gap-xl h-16 items-center', open ? 'md:hidden' : '']">
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
  </header>
</template>