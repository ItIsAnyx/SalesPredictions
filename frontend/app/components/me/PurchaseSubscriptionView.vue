<script setup>
const emit = defineEmits(["close"]);
</script>

<template>
    <div class="relative bg-white w-full max-w-[420px] rounded-xl shadow-xl p-lg md:p-xl">

        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />

        <h2 class="text-lg font-bold text-primary mb-sm">
            Subscription required
        </h2>

        <p class="text-sm text-secondary mb-lg">
            You need an active subscription to use this feature.
        </p>

        <div class="flex flex-col gap-sm">

            <NuxtLink
                to="/me"
                class="w-full bg-secondary text-white py-sm rounded-lg hover:opacity-90 transition-all flex items-center justify-center gap-sm"
            >
                <span class="material-symbols-outlined text-[18px]">
                    workspace_premium
                </span>

                Continue to subscription
            </NuxtLink>

            <button
                @click="emit('close')"
                class="w-full bg-surface-container-low text-primary py-sm rounded-lg hover:opacity-80 transition-all"
            >
                Cancel
            </button>

        </div>

    </div>
</template>