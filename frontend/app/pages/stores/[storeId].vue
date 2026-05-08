<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import StoreProductRow from '@/components/store/StoreProductRow.vue';
import AddProductWindow from "@/components/store/AddProductWindow.vue";
import UpdatePriceWindow from "@/components/store/UpdatePriceWindow.vue";
import { useApiFetch } from "@/composables/useApiFetch";

const route = useRoute();
const router = useRouter();

const api = useApiFetch();

const storeId = computed(() => route.params.storeId);

const currentPage = ref(Number(route.query.page) || 1);
const selectedRegion = ref(null);

const products = ref([]);
const totalProducts = ref(0);
const totalPages = ref(0);

const selectedUpdateProduct = ref(null);
const menuUpdateOpen = ref(false);

const regionOptions = ref([]);

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
});

const openUpdatePrice = (product) => {
  selectedUpdateProduct.value = product;
  menuUpdateOpen.value = true;
};

const closeModal = () => {
  menuUpdateOpen.value = false;
  selectedUpdateProduct.value = null;
};

const menuAddOpen = ref(false);

const toggleMenu = () => {
  menuAddOpen.value = !menuAddOpen.value;
};

const toggleUpdateMenu = () => {
  menuUpdateOpen.value = !menuUpdateOpen.value;
};

onMounted(async () => {
  currentPage.value = Number(route.query.page) || 1;

  if (route.query.region) {
    selectedRegion.value = {
      id: Number(route.query.region)
    };
  }

  await fetchProducts(currentPage.value);
  await fetchMetaRegions();

  console.log(products)
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
    `/api/stores/${storeId.value}/products?${params.toString()}`
  );

  products.value = res.items;
  totalPages.value = res.total_pages;
  totalProducts.value = res.total_items;
};

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
        <button @click="toggleMenu"
          class="flex items-center gap-xs px-md py-sm bg-secondary text-white text-sm font-semibold rounded-lg hover:opacity-90">
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

        <div>
          <DropoutMenuRegions v-model="selectedRegion" :items="regionOptions" placeholder="Select region" />
        </div>

        <div class="flex items-center gap-md text-sm text-outline">
          <span>{{ totalProducts }} Active Products</span>
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
                Last Change Forecast Trend
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                Update
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                Forecast
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-surface-container-low">
            <StoreProductRow v-for="product in products" :key="product.product_id" :product="product"
              @update-price="openUpdatePrice" />
          </tbody>
        </table>
      </div>

      <div
        class="px-md py-sm border-t border-surface-container flex items-center justify-between text-outline text-[11px] font-bold uppercase">
        <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 >
          totalProducts ? totalProducts : currentPage * 20 - 1 }} of {{
            totalProducts }} products</p>

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
            @click="currentPage++" :disabled="currentPage * 20 - 1 > totalProducts">
            <span class="material-symbols-outlined text-[18px]">chevron_right</span>
          </button>
        </div>
      </div>
    </div>
  </main>
  <div v-if="menuAddOpen" @click="toggleMenu" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
    <div @click.stop>
      <AddProductWindow :store-id="storeId" @close="toggleMenu" @updated="fetchProducts(currentPage)" />
    </div>
  </div>
  <div v-if="menuUpdateOpen" @click="closeModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
    <div @click.stop>
      <UpdatePriceWindow :product="selectedUpdateProduct" @close="toggleUpdateMenu"
        @updated="fetchProducts(currentPage)" />
    </div>
  </div>
</template>