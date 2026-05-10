<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { useApiFetch } from "@/composables/useApiFetch";
import CategoryRow from "~/components/admin/category/CategoryRow.vue";
import AddCategoryWindow from "~/components/admin/category/AddCategoryWindow.vue";

const route = useRoute();
const router = useRouter();

const api = useApiFetch();

const currentPage = ref(Number(route.query.page) || 1);

const categories = ref([]);
const totalCategories = ref();
const totalPages = ref();

const menuAddOpen = ref(false);

const toggleMenu = () => {
    menuAddOpen.value = !menuAddOpen.value;
};

onMounted(async () => {
  currentPage.value = Number(route.query.page) || 1;

  await fetchCategories(currentPage.value);
});

const fetchCategories = async (page = 1) => {
  const params = new URLSearchParams();

  params.append("page", page);
  try {
    const res = await api.request(
      `/api/categories?${params.toString()}`
    );

    categories.value = res.items;
    totalPages.value = res.total_pages;
    totalCategories.value = res.total_items;
  } catch (error) {
    navigateTo("/");
  }
};

watch(currentPage, async (page) => {
  router.replace({
    query: {
      ...route.query,
      page: String(page)
    }
  });

  await fetchCategories(page);
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
    <!-- Table -->
    <div class="bg-white border border-surface-container rounded-lg shadow-sm">

      <!-- Controls -->
      <div class="px-md py-md border-b border-surface-container-low flex items-center justify-between">
        <h3 class="font-bold text-lg text-on-surface">Category Control</h3>
        <div class="flex">
                <button @click="toggleMenu"
                    class="flex items-center gap-xs px-md py-sm bg-secondary text-white text-sm font-semibold rounded-lg hover:opacity-90">
                    <span class="material-symbols-outlined text-[18px]">add</span>
                    Add New Category
                </button>
            </div>
      </div>

      <!-- Table -->
      <div class="">
        <table class="w-full text-left">

          <thead>
            <tr class="bg-surface-container-low">
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                ID
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Name
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Rename
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                Delete
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-surface-container-low">
            <CategoryRow v-for="c in categories"
              :key="c.id"
              :category="c"
              @update-categories="fetchCategories"
              />
          </tbody>
        </table>
      </div>

      <div class="px-md py-sm border-t border-surface-container flex items-center justify-between text-outline text-[11px] font-bold uppercase">
        <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 > totalCategories ? totalCategories : currentPage * 20 - 1 }} of {{ totalCategories }} categories</p>

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
            :disabled="currentPage * 20 - 1 > totalCategories"
          >
            <span class="material-symbols-outlined text-[18px]">chevron_right</span>
          </button>
        </div>
      </div>

    </div>
  </section>
  <div v-if="menuAddOpen" @click="toggleMenu" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
        <div @click.stop>
            <AddCategoryWindow @close="toggleMenu" @updated="fetchCategories(currentPage)"/>
        </div>
    </div>
</template>