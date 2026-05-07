<script setup>
import { ref } from "vue";
import { useApiFetch } from '@/composables/useApiFetch';

const emit = defineEmits(["updated", "close"]);

const api = useApiFetch();

const storeName = ref("");

const loading = ref(false);

const handleSubmit = async () => {
    try {
        loading.value = true;

        const res = await api.request(
            `/api/stores`,
            {
                method: "POST",
                body: {
                    store_name: storeName.value
                }
            }
        );

        emit("updated", res);
        emit("close");

    } catch (e) {
        console.error("Failed to update price:", e);
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="overflow-hidden relative bg-white w-full max-w-[440px] rounded-lg shadow-xl p-lg md:p-xl">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />
        <h2 class="text-lg font-bold mb-xl">Add Product</h2>
        <form class="space-y-lg" @submit.prevent="handleSubmit">
            <div class="space-y-sm">
                <label class="text-slate-600 block" for="product_name">Store Name</label>
                <div class="relative">
                    <input v-model="storeName" id="product_name" name="product_name" type="text"
                        placeholder="Core Processor X1"
                        class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 px-4 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" />
                </div>
            </div>

            <button type="submit" :disabled="loading" class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                        hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed">
                <span v-if="!loading" class="flex items-center gap-2">
                    Add Store
                </span>

                <span v-else class="flex items-center gap-2">
                    <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4" fill="none" />
                        <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                    </svg>
                    Loading...
                </span>
            </button>
        </form>
    </div>
</template>