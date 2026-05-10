<script setup>
import { useApiFetch } from "@/composables/useApiFetch";

const api = useApiFetch();

const ranges = {
    "1D": 1 * 24 * 60 * 60 * 1000,
    "1W": 7 * 24 * 60 * 60 * 1000,
    "1M": 30 * 24 * 60 * 60 * 1000,
    "3M": 91 * 24 * 60 * 60 * 1000,
    "1Y": 365 * 24 * 60 * 60 * 1000,
};

const graphRange = ref(ranges["1D"]);

const setGraphRange = (value) => {
    graphRange.value = value;
};

const rows = ref(null);

const options = computed(() => ({
    series: [{
        name: "Price Changes",
        data: rows.value?.map(p => p.value),
    }],
    chart: {
        height: 400,
        type: "line",
        zoom: {
            enabled: true,
        }
    },
    colors: ["#006a61"],
    stroke: {
        curve: "smooth",
        width: 5,
    },
    title: {
        text: "Price Changes Timeline",
        align: "left",
        style: {
            fontSize: "16px",
            color: '#0b1c30'
        }
    },
    xaxis: {
        type: "datetime",
        categories: rows.value?.map(p => p.timestamp) || [],
        tickAmount: 10,
        labels: {
            formatter: function (value, timestamp, opts) {
                return opts.dateFormatter(new Date(timestamp), 'dd MMM')
            }
        }
    }
}));

const fetchTimeline = async () => {
    const res = await api.request(
        `/api/metrics/price-changes-timeline?range_ms=${graphRange.value}`
    );

    rows.value = res || [];
};

watch(graphRange, async () => {
    await fetchTimeline();
});

onMounted(async () => {
    await fetchTimeline();
    console.log(rows)
});
</script>

<template>
    <h2 class="font-h2 text-h2 text-primary">
        Historical Analysis
    </h2>

    <div
        class="bg-white rounded-xl p-lg border border-surface-container flex flex-col gap-2 flex-1"
    >
        <div class="flex items-center justify-between">
            <div>
                <h3 class="font-h3 text-h3 text-primary">
                    Performance History
                </h3>

                <p class="font-body-sm text-on-surface-variant">
                    User price changes activity
                </p>
            </div>

            <div class="flex bg-surface-container-low p-xs rounded-lg">
                <button
                    v-for="(item, index) in ranges"
                    :key="index"
                    @click="setGraphRange(item)"
                    class="px-md py-xs rounded-md font-label-sm transition"
                    :class="
                        graphRange === item
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'
                    "
                >
                    {{ index }}
                </button>
            </div>
        </div>

        <div class="relative w-full mt-md">
            <ApexChart
                :options="options"
                :series="options.series"
            />
        </div>
    </div>
</template>