<script setup>
import { computed, onMounted, ref } from "vue";

import { useAuth } from "@/composables/useAuth";
import { useApiFetch } from "@/composables/useApiFetch";

import MetricsSection from '~/components/me/MetricsSection.vue';
import GraphSection from '~/components/me/GraphSection.vue';

import SubscriptionWindow from "~/components/me/CreateSubscriptionView.vue";

const api = useApiFetch();

const { user } = useAuth();

const subscription = ref(null);

const isSubscriptionActive = computed(
    () => subscription.value?.status === "active"
);

const isSubscriptionWindowOpen = ref(false);

const fetchSubscription = async () => {
    try {
        const res = await api.request("/api/subscriptions/me");

        subscription.value = res;

    } catch (e) {
        subscription.value = null;
    }
};

const cancelSubscription = async () => {
    try {
        await api.request("/api/subscriptions/cancel", {
            method: "POST"
        });

        await fetchSubscription();

    } catch (e) {
        console.error("Cancel subscription error:", e);
    }
};

const openSubscriptionWindow = () => {
    isSubscriptionWindowOpen.value = true;
};

const closeSubscriptionWindow = () => {
    isSubscriptionWindowOpen.value = false;
};

onMounted(() => {
    fetchSubscription();
});
</script>

<template>
    <div class="flex flex-col items-center w-full">

        <section class="mb-xl w-full flex flex-row gap-2">

            <!-- PROFILE -->
            <div
                class="bg-surface-container-low rounded-xl p-lg flex flex-col md:flex-row items-center md:items-start gap-lg border border-surface-container-highest w-[80%]"
            >
                <div class="flex-1 text-center md:text-left">

                    <div
                        v-if="user"
                        class="flex flex-col md:flex-row md:items-center justify-between gap-md mb-sm"
                    >

                        <div>
                            <h1 class="font-h1 text-h1 text-primary">
                                {{ user.first_name }}
                                {{ user.last_name }}
                            </h1>
                        </div>

                        <button
                            class="bg-secondary text-white px-lg py-sm rounded-lg font-label-md hover:opacity-80 transition-all flex items-center gap-sm self-center md:self-start"
                        >
                            <span class="material-symbols-outlined text-[18px]">
                                edit
                            </span>

                            Edit Profile
                        </button>

                    </div>

                    <div
                        v-if="user"
                        class="flex flex-wrap justify-center md:justify-start gap-md mt-sm"
                    >

                        <div class="flex items-center gap-xs font-label-sm text-secondary">
                            <span class="material-symbols-outlined text-[16px]">
                                email
                            </span>

                            {{ user.email }}
                        </div>

                    </div>

                </div>
            </div>

            <!-- SUBSCRIPTION -->
            <div
                class="bg-surface-container-low rounded-xl p-lg border border-surface-container-highest w-[20%] flex flex-col justify-between"
            >

                <div>

                    <div class="flex items-center justify-between mb-md">

                        <h2 class="text-lg font-semibold text-primary">
                            Subscription
                        </h2>

                        <span
                            v-if="isSubscriptionActive"
                            class="bg-green-500/15 text-green-500 px-sm py-[2px] rounded-md text-xs font-medium"
                        >
                            Active
                        </span>

                        <span
                            v-else
                            class="bg-red-500/15 text-red-500 px-sm py-[2px] rounded-md text-xs font-medium"
                        >
                            Inactive
                        </span>

                    </div>

                    <div
                        v-if="isSubscriptionActive"
                        class="flex flex-col gap-sm"
                    >

                        <div>
                            <p class="text-sm text-secondary">
                                Plan
                            </p>

                            <p class="font-medium text-primary">
                                {{ subscription.subscription_name }}
                            </p>
                        </div>

                        <div>
                            <p class="text-sm text-secondary">
                                Valid until
                            </p>

                            <p class="font-medium text-primary">
                                {{ new Date(subscription.end_date).toLocaleDateString('ru-RU') }}
                            </p>
                        </div>

                    </div>

                    <div
                        v-else
                        class="text-sm text-secondary"
                    >
                        You don’t have an active subscription.
                    </div>

                </div>

                <button
                    v-if="!isSubscriptionActive"
                    @click="openSubscriptionWindow"
                    class="mt-lg w-full bg-primary text-white py-sm rounded-lg hover:opacity-90 transition-all flex items-center justify-center gap-sm"
                >

                    <span class="material-symbols-outlined text-[18px]">
                        workspace_premium
                    </span>
                    Get Premium
                </button>

                <button
                    v-if="isSubscriptionActive"
                    @click="cancelSubscription"
                    class="mt-2 w-full bg-red-500/10 text-red-500 py-sm rounded-lg hover:bg-red-500/20 transition-all flex items-center justify-center gap-sm"
                >
                    <span class="material-symbols-outlined text-[18px]">
                        cancel
                    </span>

                    Cancel Subscription
                </button>

            </div>

        </section>

        <div class="w-full">
            <MetricsSection />
            <GraphSection />
        </div>

        <div v-if="isSubscriptionWindowOpen" class="fixed inset-0 z-[999] bg-black/50 backdrop-blur-sm flex items-center justify-center p-md" @click.self="closeSubscriptionWindow">
            <SubscriptionWindow @close="closeSubscriptionWindow" @updated="fetchSubscription"/>
        </div>
    </div>
</template>