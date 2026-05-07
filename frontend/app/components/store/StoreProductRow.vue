<script setup>
const props = defineProps({
    product: Object
})
const emit = defineEmits(["update-price"]);

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

const timeAgo = (dateString) => {
  const date = new Date(dateString);

  const now = new Date();

  const diffMs = now - date;

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) return `${seconds}s ago`;
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
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

        <td class="px-md py-md text-sm font-medium text-on-surface">
            ₽{{ product.avg_last_price?.toFixed(2) || 0}}
        </td>

        <td class="px-md py-md text-sm font-medium text-on-surface">
            {{ timeAgo(product.last_change || new Date()) }}
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
                    {{ isGrowing ? "+" : ""}}{{ product.diff_percent?.toFixed(2) || 0 }}%
                </span>
            </div>
        </td>

        <td class="px-md py-md flex justify-end">
            <button
                class="px-md py-sm bg-secondary text-white text-sm font-bold rounded-lg hover:opacity-90"
                @click="emit('update-price', product)"
            >
                Update Price
            </button>
        </td>
    </tr>
</template>