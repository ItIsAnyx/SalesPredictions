<script setup>
import { computed, onMounted, ref } from 'vue';
import { useApiFetch } from '@/composables/useApiFetch';

const emit = defineEmits(["updated", "close"]);

const api = useApiFetch();

const subscriptions = ref([]);
const selectedSubscription = ref(null);

const durationOptions = ref([]);

const fetchDurationOptions = async () => {
    const res = await api.request(
        "/api/meta/subscription-options"
    );

    durationOptions.value = res.durations;
};

const selectedDuration = ref(durationOptions[0]);

const loading = ref(false);
const errorMessage = ref(null);

const totalPrice = computed(() => {
    if (!selectedSubscription.value) {
        return 0;
    }

    return (
        Number(selectedSubscription.value.price) *
        selectedDuration.value.multiplier
    ).toFixed(2);
});

const fetchSubscriptions = async () => {
    try {
        const res = await api.request("/api/meta/subs");

        subscriptions.value = res.subscriptions;

    } catch (e) {
        errorMessage.value =
            e?.data?.detail ||
            e?.message ||
            "Failed to load subscriptions";
    }
};

const handleSubmit = async () => {
    try {
        errorMessage.value = null;
        loading.value = true;

        if (!selectedSubscription.value) {
            throw new Error("Please select a subscription");
        }

        const res = await api.request(
            `/api/subscriptions/buy`,
            {
                method: "POST",
                body: {
                    id: selectedSubscription.value.id,
                    duration_months: selectedDuration.value.months
                }
            }
        );

        emit("updated", res);
        emit("close");

    } catch (e) {
        errorMessage.value =
            e?.data?.detail ||
            e?.message ||
            "Something went wrong";
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchSubscriptions();
    fetchDurationOptions();
});
</script>

<template>
    <div class="relative bg-white w-full max-w-[440px] rounded-lg shadow-xl p-lg md:p-xl">

        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60"/>

        <h2 class="text-lg font-bold mb-lg">
            Purchase Subscription
        </h2>

        <form class="space-y-lg" @submit.prevent="handleSubmit">

            <div class="space-y-sm">
                <label class="text-slate-600 block">
                    Subscription Plan
                </label>
                <DropoutMenuWindow
                    v-model="selectedSubscription"
                    :items="subscriptions"
                    placeholder="Select subscription"
                />
            </div>

            <div class="space-y-sm">
                <label class="text-slate-600 block">
                    Duration
                </label>
                <DropoutMenuWindow
                    v-model="selectedDuration"
                    :items="durationOptions"
                    placeholder="Select duration"
                />
            </div>

            <div v-if="selectedSubscription" class="bg-slate-50 border border-slate-200 rounded-lg p-md flex flex-col gap-sm">
                <div class="flex items-center justify-between">
                    <span class="text-slate-500">
                        Plan
                    </span>
                    <span class="font-medium text-slate-800">
                        {{ selectedSubscription.name }}
                    </span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-slate-500">
                        Duration
                    </span>
                    <span class="font-medium text-slate-800">
                        {{ selectedDuration.label }}
                    </span>
                </div>
                <div class="h-[1px] bg-slate-200 my-1" />
                <div class="flex items-center justify-between">
                    <span class="text-slate-500">
                        Total Price
                    </span>
                    <span class="font-semibold text-secondary text-xl">
                        ₽{{ totalPrice }}
                    </span>
                </div>
            </div>

            <button
                type="submit"
                :disabled="loading"
                class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed">

                <span v-if="!loading" class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[20px]">
                        workspace_premium
                    </span>
                    Purchase Subscription
                </span>

                <span v-else class="flex items-center gap-2">
                    <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4" fill="none"/>
                        <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
                    </svg>
                    Processing...
                </span>
            </button>
            <p v-if="errorMessage" class="text-red-500 text-sm mt-2" >
                {{ errorMessage }}
            </p>
        </form>
    </div>
</template>