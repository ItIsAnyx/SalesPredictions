<script setup>
import { useApiFetch } from "@/composables/useApiFetch";

const api = useApiFetch();

const rows = ref(null);

const options = computed(() => ({
    series: [{
        data: rows.value?.map(r => r.value)
    }],
    chart: {
        type: 'bar',
        height: 400
    },
    title: {
        text: "Count values by Category",
        align: "left",
        style: {
            fontSize: "16px",
            color: '#0b1c30'
        }
    },
    colors: ["#006a61"],
    plotOptions: {
        bar: {
            borderRadius: 4,
            borderRadiusApplication: 'end',
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        categories: rows.value?.map(r => r.title)
    }
}));

const fetchTimeline = async () => {
    const res = await api.request(
        `/api/metrics/price-changes-by-category`
    );

    rows.value = res || [];
};

onMounted(async () => {
    await fetchTimeline();
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
                    User price changes by category
                </p>
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