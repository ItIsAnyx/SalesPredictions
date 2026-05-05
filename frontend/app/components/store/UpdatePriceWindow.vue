<script setup>
const props = defineProps({
  product: Object
});

const price = ref(props.product?.current_price || 0);
const productName = ref(props.product?.product_name || "");

const handleSubmit = () => {
  console.log({
    product: props.product.product_name,
    price: price.value
  });
};
</script>

<template>
    <div class="overflow-hidden relative bg-white w-full max-w-[440px] rounded-lg shadow-xl p-lg md:p-xl">
        <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-secondary to-secondary/60" />
        <h2 class="text-lg font-bold mb-lg">Update Price for {{ productName }}</h2>
        <form class="space-y-lg" @click.prevent="handleSubmit">
            <div class="space-y-sm">
                <label class="text-slate-600 block" for="price">Initial Price</label>
                <div class="relative group">
                    <span class="absolute left-3 top-1/2 -translate-y-1/2 flex items-center justify-center h-5 w-5 text-slate-400 group-focus-within:text-secondary transition-colors">
                        $
                    </span>
                    <input v-model="price"
                        id="price"
                        name="price"
                        type="number"
                        step="0.01"
                        placeholder="0.00"
                        class="w-full bg-slate-50 border border-slate-200 text-on-surface rounded-lg py-3 pl-10 pr-10 focus:ring-1 focus:ring-secondary focus:border-secondary transition-all outline-none placeholder:text-slate-400"/>
                </div>
            </div>
            
            <button
                type="submit"
                :disabled="loading"
                class="w-full bg-secondary text-white font-headline-md text-body-lg py-3 rounded-lg shadow-lg shadow-secondary/20 transition-all flex items-center justify-center gap-2
                        hover:opacity-90 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed"
            >
                <span v-if="!loading" class="flex items-center gap-2">
                    Add Product
                </span>

                <span v-else class="flex items-center gap-2">
                    <svg class="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                    <circle
                        class="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="white"
                        stroke-width="4"
                        fill="none"
                    />
                    <path
                        class="opacity-75"
                        fill="white"
                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                    />
                    </svg>
                    Loading...
                </span>
            </button>
        </form>
    </div>
</template>