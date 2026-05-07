<script setup>
const props = defineProps({
    store: Object
})
</script>

<template>
    <tr class="hover:bg-surface-container-low transition-colors">

        <!-- Store info -->
        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="font-bold text-on-surface text-sm">
                        {{ store.title }}
                    </p>

                    <p class="text-[11px] text-outline">
                        Store ID: {{ store.id }}
                    </p>
                </div>
            </div>
        </td>

        <!-- Created date -->
        <td class="px-md py-md text-sm font-medium text-on-surface">
            {{ new Date(store.created_at).toLocaleDateString() }}
        </td>

        <!-- Action -->
        <td class="px-md py-md flex justify-end">
            <NuxtLink :to="`/stores/${store.id}`"
                class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg hover:opacity-90">
                Open Store
            </NuxtLink>
        </td>

    </tr>
</template>