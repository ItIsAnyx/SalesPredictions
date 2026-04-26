<script setup>
import { ref, onMounted } from 'vue';
import { useAuth } from "@/composables/useAuth";

const { fetchUser } = useAuth();

onMounted(() => {
  fetchUser();
})

const isSidebarOpen = ref(false)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}


</script>

<template>
  <div class="bg-background text-on-background font-body-md selection:bg-secondary-container">

    <LayoutsAppHeader :open="isSidebarOpen" @toggle-sidebar="toggleSidebar" />

    <div class="flex min-h-screen pt-16">
      <LayoutsAppSideBar :open="isSidebarOpen" @close="isSidebarOpen = false" />

      <main :class="['flex w-full p-container-margin transition-all duration-300',
        isSidebarOpen ? 'ml-[260px]' : 'ml-0']">
        <slot />
      </main>
      
    </div>
  </div>
</template>