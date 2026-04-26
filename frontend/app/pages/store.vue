<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import ProductRow from '~/components/store/ProductRow.vue';

const route = useRoute();
const router = useRouter();

const currentPage = ref(Number(route.query.page) || 1);

const products = ref([]);
const totalProducts = ref();
const totalChange = ref();
const totalPages = ref();

const fetchProducts = async (page) => {
  // await $fetch(`/api/products?page=${page}`);
  const res = {
    total_items: 1284,
    total_change: 4,
    page: 1,
    total_pages: 100,
    items: [
      {
        product_name: "Core Processor X1",
        product_sku: "CP-X1-2024",
        last_change: 2,
        current_price: 429.5,
        forecast_trend_percent: 2.4
      },
      {
        product_name: "Solid State Drive 2TB",
        product_sku: "SSD-2TB-PRO",
        last_change: 2,
        current_price: 185.0,
        forecast_trend_percent: -1.1
      }
    ]
  };
  products.value = res.items;
  totalPages.value = res.total_pages;
  totalProducts.value = res.total_items;
  totalChange.value = res.total_change;
};

watch(currentPage, async (page) => {
  router.push({
    query: { ...route.query, page }
  });

  await fetchProducts(page);
});

onMounted(() => {
  fetchProducts(currentPage.value);
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
          My Store
        </h2>
        <p class="font-inter text-sm text-on-surface mt-xs">
          Manage your product catalog and manual price entries.
        </p>
      </div>

      <div class="flex">
        <button class="flex items-center gap-xs px-md py-sm bg-secondary text-white text-sm font-semibold rounded-lg hover:opacity-90">
          <span class="material-symbols-outlined text-[18px]">add</span>
          Add New Product
        </button>
      </div>
    </div>

    <!-- TABLE -->
    <div class="bg-white border border-surface-container rounded-lg overflow-hidden shadow-sm">

      <div class="px-md py-md border-b border-surface-container-low flex items-center justify-between">
        <h3 class="font-bold text-lg text-on-surface">
          Inventory Overview
        </h3>

        <div class="flex items-center gap-md text-sm text-outline">
          <span>{{ totalProducts }} Active Items</span>
        </div>
      </div>
      
      <!-- Table -->
        <div class="">
          <table class="w-full text-left">

            <thead>
              <tr class="bg-surface-container-low">
                <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                  Product
                </th>
                <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                  Price
                </th>
                <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                  Updated
                </th>
                <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                  7-Day Forecast Trend
                </th>
                <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                  Update
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-surface-container-low">
              <ProductRow v-for="product in products"
                :key="product.product_sku"
                :product="product"
              />
            </tbody>
          </table>
        </div>

        <div class="px-md py-sm border-t border-surface-container flex items-center justify-between text-outline text-[11px] font-bold uppercase">
          <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 }} of {{ totalProducts }} products</p>

          <div class="flex items-center gap-xs">
            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-surface-container-low"
              @click="currentPage--" :disabled="currentPage === 1"
            >
              <span class="material-symbols-outlined text-[18px]">chevron_left</span>
            </button>

            <button
              v-for="page in visiblePages"
              :key="page"
              @click="currentPage = page"
              class="w-8 h-8 flex items-center justify-center rounded"
              :class="page === currentPage ? 'bg-secondary text-white' : 'hover:bg-surface-container-low'"
            >
              {{ page }}
            </button>

            <button class="w-8 h-8 flex items-center justify-center rounded hover:bg-surface-container-low"
              @click="currentPage++"
            >
              <span class="material-symbols-outlined text-[18px]">chevron_right</span>
            </button>
          </div>
        </div>
      </div>

    </main>
</template>