<script setup>

</script>

<template>
    <!-- Forecast Panel -->
    <div class="col-span-12 lg:col-span-4 flex flex-col gap-gutter">
        <!-- Outlook Card -->
        <div
            class="bg-primary-container text-on-surface p-lg rounded-xl shadow-xl flex-1 relative overflow-hidden h-full min-h-[480px] flex flex-col justify-center">
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
                        <p class="text-on-primary-container text-label-sm mt-xs">High confidence probability
                            (84%)</p>
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
            <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-secondary-fixed/10 rounded-full blur-3xl">
            </div>
        </div>
    </div>
</template>