<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useApiFetch } from "@/composables/useApiFetch";
import ProductGraph from "~/components/products/ProductGraph.vue";
import ProductMetrics from "~/components/products/ProductMetrics.vue";
import ForecastPanel from "~/components/products/ForecastPanel.vue";

const api = useApiFetch();

const route = useRoute();

const productId = route.params.productId;

const product = ref(null);

const predictions = ref(null);

const historyStats = ref(null);
const predictionStats = ref(null);

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
    <div class="mx-auto space-y-lg max-w-[1280px] w-full p-md md:p-lg">
        <!-- Product Header Section -->
        <section class="flex md:flex-row justify-between items-start md:items-end gap-md">
            <div>
                <h2 class="font-bold font-display-lg text-display-lg text-on-surface">{{ product?.title }}</h2>
                <div class="flex items-center gap-md mt-sm">
                    <span class="font-data-mono text-2xl font-bold text-on-surface">₽{{ historyStats?.current_price }}</span>
                    <div v-if="historyStats?.trend_value > 0" class="flex items-center px-sm py-xs bg-secondary/10 rounded-lg">
                        <span class="material-symbols-outlined text-secondary text-sm" data-icon="trending_up">
                            trending_up
                        </span>
                        <span class="text-secondary font-bold text-label-sm ml-xs">+{{ historyStats?.trend_value.toFixed(2) }}%</span>
                    </div>
                    <div v-else class="flex items-center px-sm py-xs bg-error/10 rounded-lg">
                        <span class="material-symbols-outlined text-error text-sm" data-icon="trending_down">
                            trending_down
                        </span>
                        <span class="text-error font-bold text-label-sm ml-xs">{{ historyStats?.trend_value.toFixed(2) }}%</span>
                    </div>
                    <span class="text-on-surface-variant text-label-sm">{{ nowDate() }}</span>
                </div>
            </div>
        </section>
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 lg:col-span-8 bg-white border border-outline-variant rounded-xl p-lg shadow-sm">
                <ProductGraph :productId="productId" v-model:prediction="predictions" v-model:historyStats="historyStats" v-model:predictionStats="predictionStats"/>
                <product-metrics />
            </div>
            <forecast-panel />
        </div>
    </div>
</template>