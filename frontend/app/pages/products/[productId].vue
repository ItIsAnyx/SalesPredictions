<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useApiFetch } from "@/composables/useApiFetch";
import ProductGraph from "~/components/products/ProductGraph.vue";
import ProductMetrics from "~/components/products/ProductMetrics.vue";
import ForecastPanel from "~/components/products/ForecastPanel.vue";
import PurchaseSubscriptionView from "~/components/me/PurchaseSubscriptionView.vue";

const api = useApiFetch();

const route = useRoute();

const productId = route.params.productId;

const product = ref(null);

const prediction = ref(null);
const history = ref(null);

const historyStats = ref(null);

const showSubscriptionRequired = ref(false);

const openSubscriptionWindow = () => {
    showSubscriptionRequired.value = true;
};

const closeSubscriptionWindow = () => {
    showSubscriptionRequired.value = false;
};

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
                    <span class="font-data-mono text-2xl font-bold text-on-surface">₽{{ historyStats?.current_price
                        }}</span>
                    <div v-if="historyStats?.trend_value > 0"
                        class="flex items-center px-sm py-xs bg-secondary/10 rounded-lg">
                        <span class="material-symbols-outlined text-secondary text-sm" data-icon="trending_up">
                            trending_up
                        </span>
                        <span class="text-secondary font-bold text-label-sm ml-xs">+{{
                            historyStats?.trend_value.toFixed(2) }}%</span>
                    </div>
                    <div v-else class="flex items-center px-sm py-xs bg-error/10 rounded-lg">
                        <span class="material-symbols-outlined text-error text-sm" data-icon="trending_down">
                            trending_down
                        </span>
                        <span class="text-error font-bold text-label-sm ml-xs">{{
                            historyStats?.trend_value.toFixed(2) }}%</span>
                    </div>
                    <span class="text-on-surface-variant text-label-sm">{{ nowDate() }}</span>
                </div>
            </div>
        </section>
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-12 lg:col-span-8 bg-white border border-outline-variant rounded-xl p-lg shadow-sm">
                <ProductGraph :productId="productId" v-model:prediction="prediction"
                    v-model:historyStats="historyStats" v-model:history="history"
                    @open:subscription="openSubscriptionWindow" />
                <product-metrics :history="history" />
            </div>
            <forecast-panel :prediction="prediction" :history="history" />
        </div>
    </div>
    <div v-if="showSubscriptionRequired" class="fixed inset-0 z-[999] bg-black/50 backdrop-blur-sm flex items-center justify-center p-md" @click.self="closeSubscriptionWindow">
        <PurchaseSubscriptionView @close="closeSubscriptionWindow"/>
    </div>
</template>