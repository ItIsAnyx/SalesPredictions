<script setup>
import { ref, watch } from "vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";

const props = defineProps({
    items: {
        type: Array,
        required: true
    },
    modelValue: {
        type: [Object, String, Number, null],
        default: null
    },
    placeholder: {
        type: String,
        default: "Select option"
    }
});

const emit = defineEmits(["update:modelValue"]);

const selected = ref(props.modelValue || null);

watch(
    () => props.modelValue,
    (value) => {
        selected.value = value;
    }
);

const selectItem = (item) => {
    selected.value = item;
    emit("update:modelValue", item);
};

const getItemLabel = (item) => {
    if (!item) return "";

    if (typeof item === "object") {
        return item.title || item.name || item.label || "";
    }

    return item;
};

const getItemKey = (item, index) => {
    if (typeof item === "object") {
        return item.id || index;
    }

    return item;
};
</script>

<template>
    <Menu as="div" class="relative w-full">
        <MenuButton
            class="w-full flex items-center justify-between bg-slate-50 border border-slate-200 rounded-lg py-3 px-4 text-left focus:ring-1 focus:ring-secondary outline-none transition-all"
        >
            <span class="text-slate-700">
                {{ getItemLabel(selected) || placeholder }}
            </span>
        </MenuButton>

        <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
        >
            <MenuItems
                class="absolute z-20 mt-1 w-full overflow-hidden rounded-lg border border-slate-200 bg-white shadow-lg focus:outline-none"
            >
                <div class="py-1">
                    <MenuItem
                        v-for="(item, index) in items"
                        :key="getItemKey(item, index)"
                        v-slot="{ active }"
                    >
                        <button
                            type="button"
                            @click="selectItem(item)"
                            :class="[
                                active
                                    ? 'bg-slate-100'
                                    : 'bg-white',
                                'w-full px-4 py-3 text-left text-sm transition-colors'
                            ]"
                        >
                            {{ getItemLabel(item) }}
                        </button>
                    </MenuItem>
                </div>
            </MenuItems>
        </transition>
    </Menu>
</template>