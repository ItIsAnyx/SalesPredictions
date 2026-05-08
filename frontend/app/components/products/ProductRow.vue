<script setup>
const props = defineProps({
    product: Object
})

const isGrowing = props.product.diff_percent > 0

const secondary = "#006a61";
const error = "#ba1a1a";

const barStyle = (i) => {
  const height = isGrowing
    ? (i + 2) * 4
    : (6 - i) * 4;

  const opacity = isGrowing
    ? 0.2 + i * 0.2
    : 0.2 + (4 - i) * 0.2;

  const color = isGrowing ? secondary : error;

  return {
    height: `${height}px`,
    backgroundColor: color,
    opacity
  };
};
</script>

<template>
    <tr class="hover:bg-surface-container-low transition-colors">
        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="font-bold text-on-surface text-sm">{{ product.title }}</p>
                <p class="text-[11px] text-outline">SKU: {{ product.product_id }}</p>
                </div>
            </div>
        </td>

        <td class="px-md py-md">
            <div class="flex items-center gap-md">
                <div>
                    <p class="text-on-surface text-sm">{{ product.store_title || None }}</p>
                </div>
            </div>
        </td>

        <td class="px-md py-md text-sm font-medium text-on-surface">
            ₽{{ product.avg_last_price?.toFixed(2) || 0}}
        </td>

        <td class="px-md py-md">
            <div class="flex items-center gap-sm">
                <div class="flex items-end gap-[2px] h-6">
                    <div
                        v-for="(_, i) in 5"
                        :key="i"
                        class="w-1.5 rounded-sm transition-all"
                        :style="barStyle(i)"
                    />
                </div>
                <span class="text-[11px] font-bold flex items-center gap-1"
                    :class="isGrowing ? 'text-secondary' : 'text-error'"
                >
                <span class="material-symbols-outlined text-[14px]">
                    {{ isGrowing ? "trending_up" : "trending_down" }}
                </span>
                    {{ isGrowing ? "+" : ""}}{{ product.diff_percent?.toFixed(2) || '0.00' }}%
                </span>
            </div>
        </td>

        <td class="px-md py-md flex justify-end">
            <NuxtLink class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg gap-sm hover:opacity-90" :to="'products/' + product.product_id">
                Forecast
            </NuxtLink>
        </td>
    </tr>
</template>