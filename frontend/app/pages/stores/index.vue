<script setup>
import { ref, computed, watch } from "vue";
import { useApiFetch } from "@/composables/useApiFetch";
import { useRoute, useRouter } from "#vue-router";
import AddStoreWindow from "~/components/store/AddStoreWindow.vue";

const route = useRoute();
const router = useRouter();

const api = useApiFetch();

const stores = ref([]);
const totalStores = ref(0);
const totalPages = ref(0);
const currentPage = ref(Number(route.query.page) || 1);

const menuAddOpen = ref(false);

const toggleMenu = () => {
    menuAddOpen.value = !menuAddOpen.value;
};

onMounted(() => {
    fetchStores(currentPage.value);
})

const fetchStores = async (page) => {
    const res = await api.request(`/api/stores?page=${page}`);

    stores.value = res.items;
    totalPages.value = res.total_pages;
    totalStores.value = res.total_items;
};

watch(currentPage, async (page) => {
    router.push({
        query: { ...route.query, page }
    });

    await fetchStores(page);
});

const visiblePages = computed(() => {
    const total = totalPages.value;
    const current = currentPage.value;
    const maxVisible = 5;

    let start = Math.max(1, current - Math.floor(maxVisible / 2));
    let end = start + maxVisible - 1;

    if (end > total) {
        end = total;
        start = Math.max(1, end - maxVisible + 1);
    }

    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
});
</script>

<template>
    <main class="flex flex-col p-md md:p-lg max-w-[1280px] w-full mx-auto space-y-lg">

        <!-- Header -->
        <div class="mb-xl flex justify-between">
            <div>
                <h2 class="font-manrope text-2xl font-bold text-on-surface">
                    My Stores
                </h2>
                <p class="font-inter text-sm text-on-surface mt-xs">
                    Manage your stores and access their inventory.
                </p>
            </div>

            <div class="flex">
                <button @click="toggleMenu"
                    class="flex items-center gap-xs px-md py-sm bg-secondary text-white text-sm font-semibold rounded-lg hover:opacity-90">
                    <span class="material-symbols-outlined text-[18px]">add</span>
                    Add New Store
                </button>
            </div>
        </div>

        <!-- TABLE -->
        <div class="bg-white border border-surface-container rounded-lg overflow-hidden shadow-sm">

            <!-- top -->
            <div class="px-md py-md border-b border-surface-container-low flex items-center justify-between">
                <h3 class="font-bold text-lg text-on-surface">
                    Store Overview
                </h3>

                <div class="flex items-center gap-md text-sm text-outline">
                    <span>{{ totalStores }} Stores</span>
                </div>
            </div>

            <!-- table -->
            <table class="w-full text-left">
                <thead>
                    <tr class="bg-surface-container-low">
                        <th class="px-md py-sm text-[11px] uppercase text-outline border-b">
                            Name
                        </th>
                        <th class="px-md py-sm text-[11px] uppercase text-outline border-b">
                            Created
                        </th>
                        <th class="px-md py-sm text-[11px] uppercase text-outline border-b text-right">
                            Open
                        </th>
                    </tr>
                </thead>

                <tbody class="divide-y divide-surface-container-low">
                    <StoreRow v-for="store in stores" :key="store.id" :store="store" />
                </tbody>
            </table>

            <!-- pagination -->
            <div
                class="px-md py-sm border-t flex items-center justify-between text-outline text-[11px] font-bold uppercase">
                <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 > totalStores ? totalStores : currentPage * 20 - 1 }}
                    of {{ totalStores }} stores</p>


                <div class="flex items-center gap-xs">
                    <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-surface-container-low"
                        @click="currentPage--" :disabled="currentPage === 1">
                        <span class="material-symbols-outlined text-[18px]">chevron_left</span>
                    </button>

                    <button v-for="page in visiblePages" :key="page" @click="currentPage = page"
                        class="w-8 h-8 flex items-center justify-center rounded"
                        :class="page === currentPage ? 'bg-secondary text-white' : 'hover:bg-surface-container-low'">
                        {{ page }}
                    </button>

                    <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-surface-container-low"
                        @click="currentPage++"
                        :disabled="currentPage * 20 - 1 > totalStores"
                    >
                        <span class="material-symbols-outlined text-[18px]">chevron_right</span>
                    </button>
                </div>
            </div>
        </div>
    </main>

    <!-- modal -->
    <div v-if="menuAddOpen" @click="toggleMenu" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
        <div @click.stop>
            <AddStoreWindow @close="toggleMenu" @updated="fetchStores(currentPage)"/>
        </div>
    </div>
</template>