<script setup>
const props = defineProps({
  open: Boolean
})

const emit = defineEmits(['close'])
</script>

<template>
  <aside
    :class="[
      'fixed top-0 bottom-0 left-0 z-50 w-[230px] bg-[#0F172A] border-r border-slate-800 transition-transform duration-300 flex flex-col',
      open ? 'translate-x-0' : '-translate-x-full'
    ]">
    <NuxtLink
      to="/"
      class="h-16 px-4 border-b border-slate-800 flex items-center justify-center shrink-0">
      <span class="font-manrope font-black text-white text-lg leading-none">
        SalesPrediction
      </span>
    </NuxtLink>

    <div class="flex flex-col flex-1 pt-4">
      
      <nav class="flex flex-col gap-base">
        <NuxtLink class="flex items-center gap-md text-slate-400 py-3 px-4 font-manrope text-sm font-medium hover:bg-slate-800 hover:text-slate-200"
          to="/"
          active-class="bg-slate-800 text-white border-l-4 border-teal-500">
          <span class="material-symbols-outlined">dashboard</span>
          Dashboard
        </NuxtLink>

        <NuxtLink class="flex items-center gap-md text-slate-400 py-3 px-4 font-manrope text-sm font-medium hover:bg-slate-800 hover:text-slate-200"
          to="/store"
          active-class="bg-slate-800 text-white border-l-4 border-teal-500">
          <span class="material-symbols-outlined">storefront</span>
          My Store
        </NuxtLink>

        <NuxtLink class="flex items-center gap-md text-slate-400 py-3 px-4 font-manrope text-sm font-medium hover:bg-slate-800 hover:text-slate-200"
          to="/products"
          active-class="bg-slate-800 text-white border-l-4 border-teal-500">
          <span class="material-symbols-outlined">inventory_2</span>
          All Products
        </NuxtLink>

        <NuxtLink class="flex items-center gap-md text-slate-400 py-3 px-4 font-manrope text-sm font-medium hover:bg-slate-800 hover:text-slate-200"
          to="/about"
          active-class="bg-slate-800 text-white border-l-4 border-teal-500">
          <span class="material-symbols-outlined">info</span>
          About Us
        </NuxtLink>
      </nav>

    </div>
  </aside>
</template>