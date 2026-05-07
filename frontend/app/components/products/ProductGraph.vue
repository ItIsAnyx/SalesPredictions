<script setup>
import { useApiFetch } from "@/composables/useApiFetch";

const props = defineProps({
    productId: Number
})

const emit = defineEmits(["update:prediction"]);

const api = useApiFetch();

const ranges = ["1D", "1W", "1M", "3M", "1Y"];

const backRange = ref("1W");
const predictionRange = ref("1M");

const setBackRange = (value) => {
    backRange.value = value;
};

const setPredRange = (value) => {
    predictionRange.value = value;
}

const history = ref(null);

const prediction = ref(null);

const fetchHistory = async () => {
    const params = new URLSearchParams();

    params.append("range", convertRange(backRange.value));

    const res = await api.request(`/api/products/${props.productId}/prices?${params.toString()}`)

    history.value = res;
};

const fetchPrediction = async() => {
    const params = new URLSearchParams();

    params.append("range", convertRange(predictionRange.value));

    const res = await api.request(`/api/products/${props.productId}/price-prediction?${params.toString()}`);

    prediction.value = res;

    emit("update:prediction", res);
}

onMounted(async () => {
    await fetchHistory(backRange);
})

watch(predictionRange, async () => {
    await fetchPrediction();
});

const convertRange = (range) => {

};
</script>

<template>
    <div class="flex justify-between items-center mb-xl">
        <div class="flex w-full justify-between">
            <div class="flex flex-col gap-1">
                <span class="text-slate-600">Back Interval</span>

                <div class="flex bg-surface-container-low p-xs rounded-lg">
                    <button v-for="r in ranges" :key="'back-' + r" @click="setBackRange(r)"
                        class="px-md py-xs rounded-md font-label-sm transition" :class="backRange === r
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'">
                        {{ r }}
                    </button>
                </div>
            </div>
            <div class="flex flex-col gap-1">
                <span class="text-slate-600">Prediction Interval</span>
                <div class="flex bg-surface-container-low p-xs rounded-lg">
                    <button v-for="r in ranges" :key="'pred-' + r" @click="setPredRange(r)"
                        class="px-md py-xs rounded-md font-label-sm transition" :class="predictionRange === r
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'">
                        {{ r }}
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- Chart Placeholder with Visual Elements -->
    <div class="relative h-[400px] w-full bg-slate-50/50 rounded-lg overflow-hidden border border-slate-100">
        <div class="absolute inset-0 flex items-end px-md pb-xl">
            <!-- Mock SVG Chart Path -->
            <svg class="w-full h-full" preserveaspectratio="none" viewbox="0 0 1000 400">
                <path
                    d="M0,350 Q50,340 100,360 T200,300 T300,320 T400,220 T500,240 T600,180 T700,200 T800,150 T900,160 T1000,120"
                    fill="none" stroke="#0D9488" stroke-width="3"></path>
                <path
                    d="M0,350 Q50,340 100,360 T200,300 T300,320 T400,220 T500,240 T600,180 T700,200 T800,150 T900,160 T1000,120 V400 H0 Z"
                    fill="url(#chartGradient)" opacity="0.1"></path>
                <defs>
                    <lineargradient id="chartGradient" x1="0%" x2="0%" y1="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#0D9488;stop-opacity:1"></stop>
                        <stop offset="100%" style="stop-color:#0D9488;stop-opacity:0"></stop>
                    </lineargradient>
                </defs>
                <!-- Grid Lines -->
                <line stroke="#E2E8F0" stroke-dasharray="4" x1="0" x2="1000" y1="100" y2="100"></line>
                <line stroke="#E2E8F0" stroke-dasharray="4" x1="0" x2="1000" y1="200" y2="200"></line>
                <line stroke="#E2E8F0" stroke-dasharray="4" x1="0" x2="1000" y1="300" y2="300"></line>
            </svg>
        </div>
    </div>
</template>