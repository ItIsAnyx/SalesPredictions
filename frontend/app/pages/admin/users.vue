<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { useApiFetch } from "@/composables/useApiFetch";
import UserRow from "~/components/admin/user/UserRow.vue";
import  { useAuth } from "@/composables/useAuth";

const { user } = useAuth();

const route = useRoute();
const router = useRouter();

const api = useApiFetch();

const currentPage = ref(Number(route.query.page) || 1);

const users = ref([]);
const totalUsers = ref();
const totalPages = ref();

onMounted(async () => {
  currentPage.value = Number(route.query.page) || 1;

  await fetchUsers(currentPage.value);
});

const fetchUsers = async (page = 1) => {
  const params = new URLSearchParams();

  params.append("page", page);
  try {
    const res = await api.request(
      `/api/users?${params.toString()}`
    );

    users.value = res.items;
    totalPages.value = res.total_pages;
    totalUsers.value = res.total_items;
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

  await fetchUsers(page);
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
        <h3 class="font-bold text-lg text-on-surface">Users Control</h3>
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
                Email
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Login
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container">
                Change Role
              </th>
              <th class="px-md py-sm text-[11px] uppercase text-outline border-b border-surface-container text-right">
                Delete
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-surface-container-low">
            <UserRow v-for="u in users"
              :key="u.id"
              :user="u"
              :current_user="user"
              @update-users="fetchUsers"
              />
          </tbody>
        </table>
      </div>

      <div class="px-md py-sm border-t border-surface-container flex items-center justify-between text-outline text-[11px] font-bold uppercase">
        <p>Showing {{ currentPage === 1 ? currentPage : (currentPage - 1) * 20 }} to {{ currentPage * 20 - 1 > totalUsers ? totalUsers : currentPage * 20 - 1 }} of {{ totalUsers }} users</p>

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
            :disabled="currentPage * 20 - 1 > totalUsers"
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