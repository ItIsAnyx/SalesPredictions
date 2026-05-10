<script setup>
import { computed } from "vue";

const props = defineProps({
    prediction: {
        type: Array,
        default: () => []
    },
    history: {
        type: Object
    }
});

const forecast = computed(() => {
    const data = props.prediction || [];
    const base = props.history?.at(-1)?.price ?? 0;

    if (!data.length) {
        return {
            base: 0,
            last: 0,
            percent: 0
        };
    }

    const prices = data.map(i => Number(i.price || 0));

    const last = prices[prices.length - 1] || 0;
    
    const percent =
        base !== 0
            ? ((last - base) / base) * 100
            : 0;

    return {
        base,
        last,
        percent
    };
});
</script>

<template>
    <div class="col-span-12 lg:col-span-4 flex flex-col gap-gutter">

        <div
            class="bg-primary-container text-on-surface p-lg rounded-xl shadow-xl flex-1 relative overflow-hidden h-full min-h-[480px] flex flex-col justify-center">

            <div class="relative z-10">

                <div class="flex items-center gap-sm mb-md">
                    <span class="material-symbols-outlined text-white">auto_awesome</span>
                    <h3 class="font-title-sm text-title-sm text-white">
                        AI Price Forecast
                    </h3>
                </div>

                <div class="space-y-xl mt-lg">

                    <div>
                        <p class="mb-xs uppercase">7-Day Outlook</p>

                        <div class="flex items-baseline gap-sm">

                            <p class="text-5xl font-extrabold text-white font-manrope">
                                ₽{{ forecast.last ? forecast.last.toFixed(2) : "0.00" }}
                            </p>

                            <span :class="forecast.percent >= 0 ? 'text-green-400' : 'text-red-400'"
                                class="font-bold text-lg">
                                {{ forecast.percent >= 0 ? '+' : '' }}{{ forecast.percent.toFixed(2) }}%
                            </span>

                        </div>
                    </div>

                </div>
            </div>

            <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-secondary-fixed/10 rounded-full blur-3xl">
            </div>

        </div>
    </div>
</template>