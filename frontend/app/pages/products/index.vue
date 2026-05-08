<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import ProductRow from '~/components/products/ProductRow.vue';
import { useApiFetch } from "@/composables/useApiFetch";

const route = useRoute();
const router = useRouter();

const api = useApiFetch();

const currentPage = ref(Number(route.query.page) || 1);
const selectedRegion = ref(null);

const regionOptions = ref([]);

const products = ref([]);
const totalProducts = ref();
const growth = ref();
const totalPages = ref();

watch(selectedRegion, async () => {
  currentPage.value = 1;
  router.replace({
    query: {
      ...route.query,
      page: String(currentPage.value),
      region_id: selectedRegion.value?.id || undefined
    }
  });
  await fetchProducts(currentPage.value);
  await fetchGrowth();
});

onMounted(async () => {
  currentPage.value = Number(route.query.page) || 1;

  if (route.query.region) {
    selectedRegion.value = {
      id: Number(route.query.region)
    };
  }

  await fetchProducts(currentPage.value);
  await fetchGrowth();
  await fetchMetaRegions();
});

const fetchMetaRegions = async () => {
  const res = await api.request("/api/meta/regions");

  regionOptions.value = res.regions;
};

const fetchProducts = async (page = 1) => {
  const params = new URLSearchParams();

  params.append("page", page);

  if (selectedRegion.value) {
    params.append("region_id", selectedRegion.value.id);
  }

  const res = await api.request(
    `/api/products?${params.toString()}`
  );

  products.value = res.items;
  totalPages.value = res.total_pages;
  totalProducts.value = res.total_items;
};

const fetchGrowth = async () => {
  const params = new URLSearchParams();

  if (selectedRegion.value) {
    params.append("region_id", selectedRegion.value.id);
  }

  const growth_res = await api.request(
    `/api/products/growth?${params.toString()}`
  )

  growth.value = growth_res.growth;
}

watch(currentPage, async (page) => {
  router.replace({
    query: {
      ...route.query,
      page: String(page),
      region_id: selectedRegion.value?.id || undefined
    }
  });

  await fetchProducts(page);
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
            :class="growth > 0 ? 'text-secondary' : 'text-error'"
          >
            {{ growth > 0 ? '+' : '' }}{{growth}}
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
    <div class="bg-white border border-surface-container rounded-lg shadow-sm">

      <!-- Controls -->
      <div class="px-md py-md border-b border-surface-container-low flex items-center justify-between">
        <h3 class="font-bold text-lg text-on-surface">Product Catalog</h3>

        <div>
          <DropoutMenuRegions v-model="selectedRegion" :items="regionOptions" placeholder="Select Region" />
        </div>

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
                Store Name
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
        <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 > totalProducts ? totalProducts : currentPage * 20 - 1 }} of {{ totalProducts }} products</p>

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
            :disabled="currentPage * 20 - 1 > totalProducts"
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