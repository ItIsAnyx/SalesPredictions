<script setup>

</script>

<template>
<div class="bg-white rounded-xl p-lg border border-surface-container flex flex-col gap-2 flex-1">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="font-h3 text-h3 text-primary">Portfolio Growth</h3>
                    <p class="font-body-sm text-on-surface-variant">Cumulative AUM scaling</p>
                </div>
                <span class="text-secondary font-h3">+$842k</span>
            </div>
            <div class="relative h-48 w-full mt-md">
                <!-- Simulated Chart -->
                <svg class="w-full h-full" preserveaspectratio="none" viewbox="0 0 100 100">
                    <path d="M0,95 L20,85 L40,88 L60,70 L80,50 L100,10" fill="none" stroke="#000000"
                        stroke-dasharray="0" stroke-width="3"></path>
                    <circle cx="20" cy="85" fill="#000000" r="2"></circle>
                    <circle cx="60" cy="70" fill="#000000" r="2"></circle>
                    <circle cx="100" cy="10" fill="#016a61" r="3"></circle>
                </svg>
                <div
                    class="absolute inset-0 flex justify-between items-end border-b border-l border-surface-container-highest">
                </div>
            </div>
        </div>
</template>