<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import ProductRow from '~/components/products/ProductRow.vue';

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
        product_id: "mf73i3njhfuerufiom23io4h32",
        product_name: "Core Processor X1",
        current_price: 429.5,
        forecast_trend_percent: 2.4
      },
      {
        product_id: "mfhr349238udjfeuusdfsdfsdf",
        product_name: "Solid State Drive 2TB",
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
  <section class="p-md md:p-lg max-w-[1280px] w-full mx-auto space-y-lg">

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-md">
      <div class="bg-white border border-surface-container p-md rounded-lg flex flex-col justify-between">
        <span class="text-outline text-[11px] font-bold uppercase">Total Products</span>
        <div class="flex items-baseline gap-sm mt-sm">
          <span class="text-2xl font-bold text-on-surface">{{ totalProducts }}</span>
          <span class="text-xs font-bold"
            :class="totalChange > 0 ? 'text-secondary' : 'text-error'"
          >
            {{ totalChange > 0 ? '+' : '' }}{{totalChange}}%
        </span>
        </div>
      </div>

      <div class="bg-white border border-surface-container p-md rounded-lg flex flex-col justify-between">
        <span class="text-outline text-[11px] font-bold uppercase">Avg. Price Stability</span>
        <div class="flex items-baseline gap-sm mt-sm">
          <span class="text-2xl font-bold text-on-surface">94.2%</span>
          <span class="text-secondary text-xs font-bold">Stable</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white border border-surface-container rounded-lg overflow-hidden shadow-sm">

      <!-- Controls -->
      <div class="px-md py-md border-b border-surface-container-low flex items-center justify-between">
        <h3 class="font-bold text-lg text-on-surface">Product Catalog</h3>

        <div class="flex items-center gap-sm">

          <button class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg flex items-center gap-sm hover:opacity-90">
            <span class="material-symbols-outlined text-sm">download</span>
            Export CSV
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="">
        <table class="w-full text-left">

          <thead>
            <tr class="bg-surface-container-low">
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Product Name
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Current Price
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                7-Day Forecast Trend
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                See forecast
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
  </section>

  <div>

  </div>
</template>