<script setup>
import PriceChangeGraph from './PriceChangeGraph.vue';
import PriceChangesByCategoryGraph from './PriceChangesByCategoryGraph.vue';
</script>

<template>
    <section class="gap-2 flex flex-col pt-lg">
        <PriceChangeGraph />
        <PriceChangesByCategoryGraph />
    </section>
</template>