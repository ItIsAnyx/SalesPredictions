<script setup>
import { onMounted } from 'vue';
import { useApiFetch } from '@/composables/useApiFetch';

const props = defineProps({
    product: Object
});

const emit = defineEmits(["updated", "close"]);

const api = useApiFetch();

const seasonOptions = ref([])
const weatherConditionOptions = ref([])
const regionOptions = ref([])

const selectedPrice = ref(props.product?.avg_last_price || 0);
const selectedRegion = ref(null);
const selectedSeason = ref(null);
const selectedWeatherCondition = ref(null);
const selectedIsWeekend = ref(false);

const loading = ref(false);

const fetchMetaOptions = async () => {
    const res = await api.request("/api/meta/price-history-options");

    seasonOptions.value = res.seasons;
    weatherConditionOptions.value = res.weather_conditions;
    regionOptions.value = res.regions;
}

const handleSubmit = async () => {
    try {
        loading.value = true;

        const res = await api.request(
            `/api/products/${props.product.product_id}/price`,
            {
                method: "POST",
                body: {
                    price: Number(selectedPrice.value),
                    region_id: selectedRegion.value.id,
                    season: selectedSeason.value,
                    weather_condition: selectedWeatherCondition.value,
                    weekend: selectedIsWeekend.value
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

onMounted(() => {
    fetchMetaOptions();
});
</script>

<template>
    <div class="relative bg-white w-full max-w-[440px] rounded-lg shadow-xl p-lg md:p-xl">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />
        <h2 class="text-lg font-bold mb-lg">Update Price for {{ product.title }}</h2>
        <form class="space-y-lg" @submit.prevent="handleSubmit">
            <div class="space-y-sm">
                <label class="text-slate-600 block" for="price">Initial Price</label>
                <div class="relative group">
                    <span
                        class="absolute left-3 top-1/2 -translate-y-1/2 flex items-center justify-center h-5 w-5 text-slate-400 group-focus-within:text-secondary transition-colors">
                        $
                    </span>
                    <input v-model="selectedPrice" id="price" name="price" type="number" step="0.01" placeholder="0.00"
                        class="w-full bg-slate-50 border border-slate-200 text-slate-700 rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400" />
                </div>
            </div>
            <div class="space-y-sm">
                <label class="text-slate-600 block">
                    Region
                </label>

                <DropoutMenuWindow
                    v-model="selectedRegion"
                    :items="regionOptions"
                    placeholder="Select region"
                />
            </div>

            <div class="space-y-sm">
                <label class="text-slate-600 block">
                    Season Condition
                </label>

                <DropoutMenuWindow
                    v-model="selectedSeason"
                    :items="seasonOptions"
                    placeholder="Select season"
                />
            </div>

            <div class="space-y-sm">
                <label class="text-slate-600 block">
                    Weather Condition
                </label>

                <DropoutMenuWindow
                    v-model="selectedWeatherCondition"
                    :items="weatherConditionOptions"
                    placeholder="Select weather"
                />
            </div>

            <div class="flex items-center justify-between">
                <span class="text-slate-600">Weekend</span>
                <button type="button" @click="selectedIsWeekend = !selectedIsWeekend" :class="[
                    'w-12 h-6 rounded-full transition',
                    selectedIsWeekend ? 'bg-secondary' : 'bg-slate-200'
                ]">
                    <div :class="[
                        'w-5 h-5 bg-white rounded-full shadow transform transition',
                        selectedIsWeekend ? 'translate-x-6' : 'translate-x-1'
                    ]" />
                </button>
            </div>

            <button type="submit" :disabled="loading" class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                        hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed">
                <span v-if="!loading" class="flex items-center gap-2">
                    Update Price
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