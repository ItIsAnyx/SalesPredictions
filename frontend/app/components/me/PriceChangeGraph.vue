<script setup>
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

watch(graphRange, async () => {
})
</script>

<template>
    <h2 class="font-h2 text-h2 text-primary">Historical Analysis</h2>
    <div class="bg-white rounded-xl p-lg border border-surface-container flex flex-col gap-2 flex-1">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="font-h3 text-h3 text-primary">Performance History</h3>
                <p class="font-body-sm text-on-surface-variant">Rolling 30-day signal accuracy</p>
            </div>
            <div class="flex bg-surface-container-low p-xs rounded-lg">
                    <button v-for="(item, index) in ranges" :key="index" @click="setGraphRange(item)"
                        class="px-md py-xs rounded-md font-label-sm transition" :class="graphRange === item
                            ? 'bg-white shadow-sm text-secondary'
                            : 'text-on-surface-variant hover:text-on-surface'">
                        {{ index }}
                    </button>
                </div>
        </div>
        <div class="relative h-48 w-full mt-md">
            <!-- Simulated Chart -->
            <svg class="w-full h-full" preserveaspectratio="none" viewbox="0 0 100 100">
                <path d="M0,80 Q10,75 20,85 T40,60 T60,65 T80,30 T100,20" fill="none" stroke="#016a61" stroke-width="3">
                </path>
                <path d="M0,80 Q10,75 20,85 T40,60 T60,65 T80,30 T100,20 L100,100 L0,100 Z" fill="url(#grad1)"
                    opacity="0.1"></path>
                <defs>
                    <lineargradient id="grad1" x1="0%" x2="0%" y1="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#016a61;stop-opacity:1"></stop>
                        <stop offset="100%" style="stop-color:#016a61;stop-opacity:0"></stop>
                    </lineargradient>
                </defs>
            </svg>
            <div
                class="absolute inset-0 flex justify-between items-end border-b border-l border-surface-container-highest">
            </div>
        </div>
    </div>

</template>