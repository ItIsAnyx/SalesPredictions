<script setup>
import { useAuth } from "@/composables/useAuth";

const { user, isLoggedIn } = useAuth();

const adminMenuOpen = ref(false);

const props = defineProps({
  open: Boolean
})

const toggleAdminMenu = () => {
  adminMenuOpen.value = !adminMenuOpen.value;
};

const emit = defineEmits(['close'])
</script>

<template>
  <aside :class="[
    'fixed top-0 bottom-0 left-0 z-50 w-[260px] bg-surface-container-low border-r border-surface-variant flex flex-col transition-transform duration-300',
    open ? 'translate-x-0' : '-translate-x-full'
  ]">

    <NuxtLink to="/" class="h-16 flex items-center justify-center mb-4">
      <span class="font-manrope font-bold text-lg text-on-background">
        SalesPrediction
      </span>
    </NuxtLink>

    <nav class="flex flex-col gap-1">
      <NuxtLink
        class="text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
        active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
        to="/">
        <span class="material-symbols-outlined mr-3">dashboard</span>
        Dashboard
      </NuxtLink>

      <NuxtLink v-if="isLoggedIn"
        class="text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
        active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
        to="/stores">
        <span class="material-symbols-outlined mr-3">storefront</span>
        My Store
      </NuxtLink>


      <NuxtLink
        class="text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
        active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
        to="/products">
        <span class="material-symbols-outlined mr-3">inventory_2</span>
        All Products
      </NuxtLink>

      <button
        v-if="user?.role === 'ADMIN'"
        class="text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
        active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
        @click="toggleAdminMenu">
        <span class="material-symbols-outlined mr-3">person</span>
        Admin Panel
      </button>

      <transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 scale-y-95 -translate-y-2"
        enter-to-class="opacity-100 scale-y-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 scale-y-100 translate-y-0"
        leave-to-class="opacity-0 scale-y-95 -translate-y-2"
      >
        <div v-if="adminMenuOpen" class="overflow-hidden">
          <NuxtLink
            class="ml-5 text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
            active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
            to="/admin/users">
            <span class="material-symbols-outlined mr-3">
              person
            </span>

            User Control
          </NuxtLink>

          <NuxtLink
            class="ml-5 text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
            active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
            to="/admin/categories">
            <span class="material-symbols-outlined mr-3">
              box
            </span>

            Category Control
          </NuxtLink>

          <NuxtLink
            class="ml-5 text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
            active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
            to="/admin/regions">
            <span class="material-symbols-outlined mr-3">
              inventory_2
            </span>

            Region Region
          </NuxtLink>
        </div>
      </transition>

      <NuxtLink
        class="text-slate-600 hover:text-teal-600 flex items-center px-4 py-3 transition-all cursor-pointer text-sm font-medium tracking-wide"
        active-class="text-teal-500 hover:text-teal-600 bg-surface-container-highest/50 border-r-4 border-secondary font-bold"
        to="/about">
        <span class="material-symbols-outlined mr-3">info</span>
        About Us
      </NuxtLink>
    </nav>

  </aside>
</template>
