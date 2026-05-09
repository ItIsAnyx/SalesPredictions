<script setup>
import { useAuth } from "@/composables/useAuth";
import MetricsSection from '~/components/me/MetricsSection.vue';
import GraphSection from '~/components/me/GraphSection.vue';

const { user, isLoggedIn } = useAuth();
</script>

<template>
    <div class="flex flex-col items-center w-full">
        <section class="mb-xl w-full">
            <div
                class="bg-surface-container-low rounded-xl p-lg flex flex-col md:flex-row items-center md:items-start gap-lg border border-surface-container-highest">

                <div class="flex-1 text-center md:text-left">

                    <div
                        v-if="user"
                        class="flex flex-col md:flex-row md:items-center justify-between gap-md mb-sm">

                        <div>
                            <h1 class="font-h1 text-h1 text-primary">
                                {{ user.first_name }} {{ user.last_name }}
                            </h1>
                        </div>

                        <button
                            class="bg-secondary text-white px-lg py-sm rounded-lg font-label-md hover:opacity-80 transition-all flex items-center gap-sm self-center md:self-start">
                            <span class="material-symbols-outlined text-[18px]">edit</span>
                            Edit Profile
                        </button>
                    </div>

                    <div
                        v-if="user"
                        class="flex flex-wrap justify-center md:justify-start gap-md mt-sm">

                        <div class="flex items-center gap-xs font-label-sm text-secondary">
                            <span class="material-symbols-outlined text-[16px]">email</span>
                            {{ user.email }}
                        </div>

                    </div>

                </div>
            </div>
        </section>

        <div class="w-full">
            <MetricsSection />
            <GraphSection />
        </div>
    </div>
</template>