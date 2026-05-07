<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useApiFetch } from "@/composables/useApiFetch";
import ProductGraph from "~/components/products/ProductGraph.vue";
import ProductMetrics from "~/components/products/ProductMetrics.vue";

const api = useApiFetch();

const route = useRoute();

const productId = route.params.productId;

const product = ref(null);

const predictions = ref(null);

const fetchProduct = async (productId) => {
    const res = await api.request(`/api/products/${productId}`);

    product.value = res;
};

onMounted(async () => {
    await fetchProduct(productId);
});

const nowDate = () => {
    return new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date());
};
</script>

<template>
    <div class="mx-auto p-gutter space-y-lg">
        <!-- Product Header Section -->
        <section class="flex flex-col md:flex-row justify-between items-start md:items-end gap-md">
            <div>
                <h2 class="font-display-lg text-display-lg text-on-surface">{{ product?.title }}</h2>
                <div class="flex items-center gap-md mt-sm">
                    <span class="font-data-mono text-2xl font-bold text-on-surface">$74.82</span>
                    <div class="flex items-center px-sm py-xs bg-secondary/10 rounded-lg">
                        <span class="material-symbols-outlined text-secondary text-sm"
                            data-icon="trending_up">trending_up</span>
                        <span class="text-secondary font-bold text-label-sm ml-xs">+1.24%</span>
                    </div>
                    <span class="text-on-surface-variant text-label-sm">{{ nowDate() }}</span>
                </div>
            </div>
        </section>
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 lg:col-span-8 bg-white border border-outline-variant rounded-xl p-lg shadow-sm">
                <ProductGraph :productId="productId" v-model:prediction="predictions"/>
                <product-metrics />
            </div>
            <!-- Forecast Panel -->
            <div class="col-span-12 lg:col-span-4 flex flex-col gap-gutter">
                <!-- Outlook Card -->
                <div
                    class="bg-primary-container text-on-surface p-lg rounded-xl shadow-xl flex-1 relative overflow-hidden h-full min-h-[480px] flex flex-col justify-center">
                    <div class="relative z-10">
                        <div class="flex items-center gap-sm mb-md">
                            <span class="material-symbols-outlined text-white"
                                data-icon="auto_awesome">auto_awesome</span>
                            <h3 class="font-title-sm text-title-sm text-white">AI Price Forecast</h3>
                        </div>
                        <div class="space-y-xl mt-lg">
                            <div>
                                <p class=" mb-xs uppercase">7-Day Outlook</p>
                                <div class="flex items-baseline gap-sm">
                                    <p class="text-5xl font-extrabold text-white font-manrope">$78.40</p>
                                    <span class="text-secondary-fixed font-bold text-lg">+4.78%</span>
                                </div>
                                <p class="text-on-primary-container text-label-sm mt-xs">High confidence probability
                                    (84%)</p>
                            </div>
                            <div class="space-y-md pt-lg">
                                <div class="flex justify-between items-center text-sm">
                                    <span class="text-on-primary-container">30-Day Forecast</span>
                                    <span class="text-white font-bold">$82.15</span>
                                </div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-secondary-fixed h-full w-[65%]"></div>
                                </div>
                                <div class="flex justify-between items-center text-sm">
                                    <span class="text-on-primary-container">Market Sentiment</span>
                                    <span class="text-secondary-fixed font-bold">Strong Bullish</span>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-secondary-fixed/10 rounded-full blur-3xl">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>