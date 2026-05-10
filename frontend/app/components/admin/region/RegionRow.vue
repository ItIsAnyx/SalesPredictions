<script setup>
import { useApiFetch } from '@/composables/useApiFetch';

const api = useApiFetch();

const props = defineProps({
    region: Object,
});

const emit = defineEmits(["update-region"]);

const isEditing = ref(false);
const title = ref(props.region?.title || "");

const inputRef = ref(null);

const startEdit = async () => {
    isEditing.value = true;

    await nextTick();
    inputRef.value?.focus();
};

const cancelEdit = () => {
    isEditing.value = false;
    title.value = props.region?.title;
};

const fetchRenameRegion = async () => {
    if (!title.value.trim() || title.value === props.region?.title) {
        cancelEdit();
        return;
    }

    await api.request(`/api/regions/${props.region.id}`, {
        method: "PATCH",
        body: {
            title: title.value
        }
    });

    isEditing.value = false;

    emit("update-region");
};

const fetchDeleteRegion = async () => {
    await api.request(`/api/regions/${props.region.id}`, {
        method: "DELETE"
    });

    emit("update-region");
};

const onKeyDown = (e) => {
    if (e.key === "Enter") fetchRename();
    if (e.key === "Escape") cancelEdit();
};
</script>

<template>
    <tr class="hover:bg-surface-container-low transition-colors">

        <td class="px-md py-md">
            <p class="font-bold text-on-surface text-sm">
                {{ region?.id }}
            </p>
        </td>

        <td class="px-md py-md">
            <div v-if="isEditing">
                <input ref="inputRef" v-model="title" @keydown="onKeyDown" @blur="saveEdit"
                    class="px-sm py-xs border border-surface-variant rounded-lg text-sm w-full" />
            </div>

            <div v-else>
                <p class="text-on-surface text-sm">
                    {{ region?.title }}
                </p>
            </div>
        </td>

        <td class="px-md py-md">
            <button v-if="!isEditing" @click="startEdit"
                class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg">
                Rename
            </button>

            <button v-else @click="fetchRenameRegion" class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg">
                Save
            </button>
        </td>

        <td class="px-md py-md flex justify-end">
            <button @click="fetchDeleteRegion" class="px-md py-sm bg-error text-white text-sm font-bold rounded-lg">
                Delete
            </button>
        </td>

    </tr>
</template>