<script setup>
import { useApiFetch } from '@/composables/useApiFetch';
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";

const api = useApiFetch();

const props = defineProps({
    user: Object,
    current_user: Object
})

const emit = defineEmits(["update-users"])

const changeRole = async (newRole) => {
    if (newRole === props.user?.role) return;

    await api.request(`/api/users/${props.user?.id}/role`, {
        method: "PATCH",
        body: {
            role: newRole
        }
    });

    emit("update-users");
};

const deleteUser = async () => {
    await api.request(`/api/users/${props.user?.id}`, {
        method: "DELETE"
    });

    emit("update-users");
};

const allowdRoles = ref(null);

const fetchMetaRoles = async () => {
    const res = await api.request(`/api/meta/roles`);

    allowdRoles.value = res.roles;
};

onMounted(() => {
    fetchMetaRoles();
});
</script>

<template>
    <tr class="hover:bg-surface-container-low transition-colors">
        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="font-bold text-on-surface text-sm">{{ user?.id }}</p>
                </div>
            </div>
        </td>

        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="text-on-surface text-sm">{{ user?.email }}</p>
                </div>
            </div>
        </td>

        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="text-on-surface text-sm">{{ user?.login }}</p>
                </div>
            </div>
        </td>

        <td class="px-md py-md">
            <Menu as="div" class="relative w-full">

                <MenuButton :disabled="current_user?.id === user?.id"
                    class="w-full flex items-center justify-between bg-slate-50 border border-slate-200 rounded-lg py-2 px-3 text-sm text-slate-700 disabled:opacity-50 disabled:cursor-not-allowed">
                    {{ user?.role }}
                    <span class="material-symbols-outlined text-sm">expand_more</span>
                </MenuButton>

                <transition enter-active-class="transition duration-100 ease-out" enter-from-class="opacity-0 scale-95"
                    enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-75 ease-in"
                    leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
                    <MenuItems
                        class="absolute z-20 mt-1 w-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-lg focus:outline-none">
                        <div class="py-1">
                            <MenuItem v-for="role in allowdRoles" :key="role" v-slot="{ active }">
                                <button type="button" @click="changeRole(role)" :class="[
                                    active ? 'bg-slate-100' : '',
                                    'w-full px-4 py-2 text-left text-sm'
                                ]">
                                    {{ role }}
                                </button>
                            </MenuItem>
                        </div>
                    </MenuItems>
                </transition>

            </Menu>
        </td>

        <td class="px-md py-md flex justify-end">
            <button :disabled="current_user?.id === user?.id" @click="deleteUser" :class="[
                'px-md py-sm bg-error text-white text-sm font-bold rounded-lg transition-all',
                current_user?.id === user?.id
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:opacity-90'
            ]">
                Delete
            </button>
        </td>
    </tr>
</template>