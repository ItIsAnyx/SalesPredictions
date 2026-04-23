<script setup>
import { ref } from 'vue'

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
        isSidebarOpen ? 'lg:ml-[230px]' : 'lg:ml-0']">
        <slot />
      </main>
    </div>
  </div>
</template>