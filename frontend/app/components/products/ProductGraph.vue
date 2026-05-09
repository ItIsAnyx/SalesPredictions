<script setup>
import { useApiFetch } from "@/composables/useApiFetch";
import DropoutMenuRegions from "../DropoutMenuRegions.vue";

const props = defineProps({
    productId: Number
})

const emit = defineEmits(["update:prediction", "update:historyStats", "update:predictionStats"]);

const api = useApiFetch();

const ranges = {
    "1D": 1 * 24 * 60 * 60 * 1000,
    "1W": 7 * 24 * 60 * 60 * 1000,
    "1M": 30 * 24 * 60 * 60 * 1000,
    "3M": 91 * 24 * 60 * 60 * 1000,
    "1Y": 365 * 24 * 60 * 60 * 1000,
};

const backRange = ref(ranges["1D"]);
const predictionRange = ref(0);

const setBackRange = (value) => {
    backRange.value = value;
};

const setPredRange = (value) => {
    if (predictionRange.value == value) {
        predictionRange.value = 0;
        prediction.value = [];
        return;
    }
    predictionRange.value = value;

}

const history = ref([]);
const prediction = ref([]);
const allData = computed(() => [
    ...history.value,
    ...(prediction?.value || [])
]);

const fetchHistory = async () => {
    const params = new URLSearchParams();

    params.append("range", backRange.value);

    if (selectedRegion.value) {
        params.append("region_id", selectedRegion.value.id);
    }

    const res = await api.request(`/api/products/${props.productId}/prices?${params.toString()}`)

    history.value = res.items;

    console.log(history.value)

    emit("update:historyStats", { "current_price": res.current_price, "trend_value": res.trend_value });
};

const fetchPrediction = async () => {
    if (predictionRange.value === 0) {
        return;
    }

    const params = new URLSearchParams();

    params.append("range", predictionRange.value);

    if (selectedRegion.value) {
        params.append("region_id", selectedRegion.value.id);
    }

    const res = await api.request(`/api/products/${props.productId}/price-prediction?${params.toString()}`);

    prediction.value = res;

    emit("update:prediction", res);
}

onMounted(async () => {
    await fetchMetaRegions();
    await fetchHistory();
})

watch(predictionRange, async () => {
    await fetchPrediction();
    console.log(allData.value)
});

watch(backRange, async () => {
    await fetchHistory();
    if (predictionRange.value !== 0) {
        await fetchPrediction();
    }
})

const regionOptions = ref(null);
const selectedRegion = ref(null);

const fetchMetaRegions = async () => {
  const res = await api.request("/api/meta/regions");

  regionOptions.value = res.regions;

  selectedRegion.value = regionOptions?.value[1];
};

watch(selectedRegion, async () => {
  await fetchHistory();
});

const chartOptions = computed(() => ({
    series: [{
        name: "Price",
        data: allData.value?.map(p => p.price.toFixed(2)) || []
    }],
    chart: {
        height: 400,
        type: "line",
        zoom: {
            enabled: true
        }
    },
    forecastDataPoints: {
        count: prediction.value?.length || 0
    },
    colors: ["#006a61"],
    stroke: {
        width: 5,
        curve: 'smooth'
    },
    xaxis: {
        type: "datetime",
        categories: allData.value?.map(p => p.timestamp) || [],
        tickAmount: 10,
        labels: {
            formatter: function (value, timestamp, opts) {
                return opts.dateFormatter(new Date(timestamp), 'dd MMM')
            }
        }
    },
    title: {
        text: 'Forecast',
        align: 'left',
        style: {
            fontSize: "16px",
            color: '#0b1c30'
        }
    }
}))
</script>

<template>
    <div class="flex justify-between items-center mb-xl">
        <div class="flex flex-col items-center w-full md:flex-row md:justify-between">
            <div class="flex flex-col gap-1">
                <span class="text-slate-600">Back Interval</span>

                <div class="flex bg-surface-container-low p-xs rounded-lg">
                    <button v-for="(item, index) in ranges" :key="'back-' + index" @click="setBackRange(item)"
                        class="px-md py-xs rounded-md font-label-sm transition" :class="backRange === item
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'">
                        {{ index }}
                    </button>
                </div>
            </div>
            <div class="flex flex-col gap-1">
                <span class="text-slate-600">Prediction Interval</span>
                <div class="flex bg-surface-container-low p-xs rounded-lg">
                    <button v-for="(item, index) in ranges" :key="'pred-' + index" @click="setPredRange(item)"
                        class="px-md py-xs rounded-md font-label-sm transition" :class="predictionRange === item
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'">
                        {{ index }}
                    </button>
                </div>
            </div>
            <dropout-menu-regions class="mt-6" v-model="selectedRegion" :items="regionOptions" placeholder="Select Region"/>
        </div>
    </div>
    <div class="w-full bg-slate-50/50 rounded-lg overflow-hidden border border-slate-100 p-md">
        <ApexChart type="line" height="400" :options="chartOptions" :series="chartOptions.series" />
    </div>
</template>