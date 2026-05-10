<script setup>
import { computed } from "vue";

const props = defineProps({
    history: {
        type: Array,
        default: () => []
    }
});

const stats = computed(() => {
    const data = props.history || [];

    if (!data.length) {
        return {
            open: 0,
            high: 0,
            low: 0,
            volume: 0
        };
    }

    const prices = data.map(i => Number(i.price || 0));

    return {
        open: prices[0] || 0,
        high: Math.max(...prices),
        low: Math.min(...prices),
        volume: prices.reduce((sum, p) => sum + p, 0)
    };
});
</script>

<template>
    <div class="grid grid-cols-4 gap-md mt-lg pt-lg border-t border-slate-100">

        <div class="space-y-xs">
            <p class="text-label-caps text-on-surface-variant">OPEN</p>
            <p class="font-data-mono text-on-surface">
                ₽{{ stats.open }}
            </p>
        </div>

        <div class="space-y-xs">
            <p class="text-label-caps text-on-surface-variant">HIGH</p>
            <p class="font-data-mono text-on-surface">
                ₽{{ stats.high }}
            </p>
        </div>

        <div class="space-y-xs">
            <p class="text-label-caps text-on-surface-variant">LOW</p>
            <p class="font-data-mono text-on-surface">
                ₽{{ stats.low }}
            </p>
        </div>

        <div class="space-y-xs">
            <p class="text-label-caps text-on-surface-variant">VOL (M)</p>
            <p class="font-data-mono text-on-surface">
                {{ (stats.volume / 1000).toFixed(1) }}K
            </p>
        </div>

    </div>
</template>