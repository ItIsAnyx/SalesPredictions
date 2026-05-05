<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const productId = route.params.productId;

onMounted(() => {

});
</script>

<template>
    <div class="mx-auto p-gutter space-y-lg">
    <!-- Product Header Section -->
        <section class="flex flex-col md:flex-row justify-between items-start md:items-end gap-md">
            <div>
            <h2 class="font-display-lg text-display-lg text-on-surface">Crude Oil WTI (CL1)</h2>
            <div class="flex items-center gap-md mt-sm">
                <span class="font-data-mono text-2xl font-bold text-on-surface">$74.82</span>
                <div class="flex items-center px-sm py-xs bg-secondary/10 rounded-lg">
                    <span class="material-symbols-outlined text-secondary text-sm" data-icon="trending_up">trending_up</span>
                    <span class="text-secondary font-bold text-label-sm ml-xs">+1.24%</span>
                </div>
                <span class="text-on-surface-variant text-label-sm">Oct 24, 14:20 UTC</span>
            </div>
            </div>
        </section>
        <div class="grid grid-cols-12 gap-4">
            <!-- Main Historical Chart -->
            <div class="col-span-12 lg:col-span-8 bg-white border border-outline-variant rounded-xl p-lg shadow-sm">
                <div class="flex justify-between items-center mb-xl">
                    <h3 class="font-title-sm text-title-sm text-on-surface">Historical Performance</h3>
                    <div class="flex bg-surface-container-low p-xs rounded-lg">
                        <button class="px-md py-xs bg-white shadow-sm text-secondary rounded-md font-label-sm">1D</button>
                        <button class="px-md py-xs text-on-surface-variant font-label-sm hover:text-on-surface">1W</button>
                        <button class="px-md py-xs text-on-surface-variant font-label-sm hover:text-on-surface">1M</button>
                        <button class="px-md py-xs text-on-surface-variant font-label-sm hover:text-on-surface">3M</button>
                        <button class="px-md py-xs text-on-surface-variant font-label-sm hover:text-on-surface">1Y</button>
                    </div>
                </div>
                <!-- Chart Placeholder with Visual Elements -->
                <div class="relative h-[400px] w-full bg-slate-50/50 rounded-lg overflow-hidden border border-slate-100">
                    <div class="absolute inset-0 flex items-end px-md pb-xl">
                    <!-- Mock SVG Chart Path -->
                        <svg class="w-full h-full" preserveaspectratio="none" viewbox="0 0 1000 400">
                            <path d="M0,350 Q50,340 100,360 T200,300 T300,320 T400,220 T500,240 T600,180 T700,200 T800,150 T900,160 T1000,120" fill="none" stroke="#0D9488" stroke-width="3"></path>
                            <path d="M0,350 Q50,340 100,360 T200,300 T300,320 T400,220 T500,240 T600,180 T700,200 T800,150 T900,160 T1000,120 V400 H0 Z" fill="url(#chartGradient)" opacity="0.1"></path>
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
                <div class="grid grid-cols-4 gap-md mt-lg pt-lg border-t border-slate-100">
                    <div class="space-y-xs">
                        <p class="text-label-caps text-on-surface-variant">OPEN</p>
                        <p class="font-data-mono text-on-surface">$73.55</p>
                    </div>
                    <div class="space-y-xs">
                        <p class="text-label-caps text-on-surface-variant">HIGH</p>
                        <p class="font-data-mono text-on-surface">$75.10</p>
                    </div>
                    <div class="space-y-xs">
                        <p class="text-label-caps text-on-surface-variant">LOW</p>
                        <p class="font-data-mono text-on-surface">$72.90</p>
                    </div>
                    <div class="space-y-xs">
                        <p class="text-label-caps text-on-surface-variant">VOL (M)</p>
                        <p class="font-data-mono text-on-surface">342.5K</p>
                    </div>
                </div>
            </div>
            <!-- Forecast Panel -->
            <div class="col-span-12 lg:col-span-4 flex flex-col gap-gutter">
                <!-- Outlook Card -->
                <div class="bg-primary-container text-on-surface p-lg rounded-xl shadow-xl flex-1 relative overflow-hidden h-full min-h-[480px] flex flex-col justify-center">
                    <div class="relative z-10">
                        <div class="flex items-center gap-sm mb-md">
                            <span class="material-symbols-outlined text-white" data-icon="auto_awesome">auto_awesome</span>
                            <h3 class="font-title-sm text-title-sm text-white">AI Price Forecast</h3>
                        </div>
                        <div class="space-y-xl mt-lg">
                            <div>
                                <p class=" mb-xs uppercase">7-Day Outlook</p>
                                <div class="flex items-baseline gap-sm">
                                    <p class="text-5xl font-extrabold text-white font-manrope">$78.40</p>
                                    <span class="text-secondary-fixed font-bold text-lg">+4.78%</span>
                                </div>
                                <p class="text-on-primary-container text-label-sm mt-xs">High confidence probability (84%)</p>
                            </div>
                            <div class="space-y-md pt-lg">
                                <div class="flex justify-between items-center text-sm">
                                    <span class="text-on-primary-container">30-Day Forecast</span>
                                    <span class="text-white font-bold">$82.15</span>
                                </div>
                                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                    <div class="bg-secondary-fixed h-full w-[65%]"></div>
                                </div>
                                <div class="flex justify-between items-center text-sm">
                                    <span class="text-on-primary-container">Market Sentiment</span>
                                    <span class="text-secondary-fixed font-bold">Strong Bullish</span>
                                </div>
                            </div>

                        </div>
                    </div>
                    <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-secondary-fixed/10 rounded-full blur-3xl"></div>
                </div>
            </div>
        </div>
    </div>
</template>