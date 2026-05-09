<script setup>
import { useApiFetch } from '@/composables/useApiFetch';

const api = useApiFetch();

const totalPriceChanges = ref(null);
const mostChangableProduct = ref(null);
const mostActiveMonth = ref(null);
const mostUnstableProduct = ref(null);
const mostActiveCategory = ref(null);
const avgPriceChangeRange = ref(null);

const METRIC_URLS = {
    totalPriceChanges: "/api/metrics/total-price-changes",
    mostChangableProduct: "/api/metrics/most-changable-product",
    mostActiveMonth: "/api/metrics/most-active-month",
    mostUnstableProduct: "/api/metrics/most-unstable-product",
    mostActiveCategory: "/api/metrics/most-active-category",
    avgPriceChangeRange: "/api/metrics/avg-price-change-range",
};

const fetchGridData = async () => {
    try {
        const [
            totalPriceChangesRes,
            mostChangableProductRes,
            mostActiveMonthRes,
            mostUnstableProductRes,
            mostActiveCategoryRes,
            avgPriceChangeRangeRes,
        ] = await Promise.all([
            api.request(METRIC_URLS.totalPriceChanges),
            api.request(METRIC_URLS.mostChangableProduct),
            api.request(METRIC_URLS.mostActiveMonth),
            api.request(METRIC_URLS.mostUnstableProduct),
            api.request(METRIC_URLS.mostActiveCategory),
            api.request(METRIC_URLS.avgPriceChangeRange),
        ]);

        totalPriceChanges.value =
            totalPriceChangesRes.data;

        mostChangableProduct.value =
            mostChangableProductRes.data;

        mostActiveMonth.value =
            mostActiveMonthRes.data;

        mostUnstableProduct.value =
            mostUnstableProductRes.data;

        mostActiveCategory.value =
            mostActiveCategoryRes.data;

        avgPriceChangeRange.value =
            avgPriceChangeRangeRes.data;

    } catch (error) {
        console.error("Failed to fetch metrics:", error);
    }
};

onMounted(async () => {
    await fetchGridData();
})

</script>

<template>
    <section class="lg:col-span-5 flex flex-col gap-2">
        <h2 class="font-h2 text-h2 text-primary">Core Metrics</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 md:grid-rows-3 gap-2 flex-1">
            <!-- Card 1 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Total Price Changes</span>
                <div class="mt-sm">
                    <span class="font-display text-h1 text-primary">{{ totalPriceChanges?.value || 0 }}</span>
                    <div v-if="totalPriceChanges?.trend > 0"
                        class="flex items-center gap-xs text-secondary font-label-sm mt-xs">
                        <span class="material-symbols-outlined text-[14px]">trending_up</span>
                        +{{ totalPriceChanges?.trend }}%
                    </div>
                    <div v-else class="flex items-center gap-xs text-error font-label-sm mt-xs">
                        <span class="material-symbols-outlined text-[14px]">trending_down</span>
                        {{ totalPriceChanges?.trend }}%
                    </div>
                </div>
            </div>
            <!-- Card 2 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Most Changable
                    Product</span>
                <div class="mt-sm flex flex-col">
                    <span class="font-display text-h1 text-primary">
                        {{ mostChangableProduct?.title || "" }}
                    </span>

                    <span class="font-display text-slate-600">
                        ID: {{ mostChangableProduct?.id || 0 }}
                    </span>

                    <span class="font-display text-h1 text-secondary">
                        {{ mostChangableProduct?.value || 0 }}
                    </span>
                </div>
            </div>
            <!-- Card 3 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Most Unstable
                    Product</span>
                <div class="mt-sm">
                    <span class="font-display text-h1 text-primary">
                        {{ mostUnstableProduct?.title || "" }}
                    </span>

                    <span class="block font-label-sm text-on-surface-variant">
                        ID: {{ mostUnstableProduct?.id || 0 }}
                    </span>

                    <span class="font-display text-h2 text-secondary">
                        ₽{{ mostUnstableProduct?.value || 0 }}
                    </span>
                </div>
            </div>
            <!-- Card 4 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Most Active Month</span>
                <div class="mt-sm">
                    <span class="font-display text-h1 text-primary">
                        {{ mostActiveMonth?.month || "—" }}
                    </span>

                    <div class="font-label-sm text-secondary mt-xs">
                        {{ mostActiveMonth?.value || 0 }} changes
                    </div>
                </div>
            </div>
            <!-- Card 5 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Most Active Category</span>
                <div class="mt-sm">
                    <span class="font-display text-h1 text-primary">
                        {{ mostActiveCategory?.title || "—" }}
                    </span>

                    <div class="font-label-sm text-secondary mt-xs">
                        {{ mostActiveCategory?.value || 0 }} changes
                    </div>
                </div>
            </div>
            <!-- Card 6 -->
            <div
                class="bg-surface-container-low rounded-lg p-md border border-surface-container-highest flex flex-col justify-between">
                <span class="font-label-md text-on-surface-variant uppercase tracking-wider">Avg Days Between
                    Changes</span>
                <div class="mt-sm">
                    <span class="font-display text-h1 text-primary">
                        {{ avgPriceChangeRange?.value || 0 }}
                    </span>

                    <div class="flex items-center gap-xs font-label-sm text-secondary mt-xs">
                        <span class="material-symbols-outlined text-[14px]">schedule</span>
                        Avg days between changes
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>