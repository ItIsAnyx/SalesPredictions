<script setup>
import { ref, onMounted } from 'vue';
import { useAuth } from "@/composables/useAuth";
import { onClickOutside } from '@vueuse/core';

const sideBarRef = ref(null);
const isSidebarOpen = ref(false)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

onClickOutside(sideBarRef, () => {
  isSidebarOpen.value = false;
});

const { fetchUser } = useAuth();

onMounted(() => {
  fetchUser();
})
</script>

<template>
  <div class="bg-background text-on-background font-body-md selection:bg-secondary-container">

    <LayoutsAppHeader :open="isSidebarOpen" @toggle-sidebar="toggleSidebar" />

    <div class="flex min-h-screen pt-16">
      <LayoutsAppSideBar ref="sideBarRef" :open="isSidebarOpen" @close="isSidebarOpen = false" />

      <main :class="['flex w-full p-container-margin transition-all duration-300',
        isSidebarOpen ? 'ml-[260px]' : 'ml-0']">
        <slot />
      </main>
      
    </div>
  </div>
</template>