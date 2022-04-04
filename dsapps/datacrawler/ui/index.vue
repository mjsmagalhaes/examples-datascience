<template lang="pug">
.m-3
  h1.text-center DataCrawler
  p.text-center.mt-4 A list of apps:

  .d-flex.flex-column.col-6.m-auto.align-items-center.gap-2.mt-4
    router-link(to="/raids") WoW Encounters Raids
</template>

<script>
export default {
  setup() {},
};
</script>