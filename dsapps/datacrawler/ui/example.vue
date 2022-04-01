<template lang="pug">
div 
  .mb-3.row
    .d-flex.flex-column.col-6
      label.col-sm-2.col-form-label.m-auto Character

      .col-sm-11.m-auto
        input.col-12(v-model="inputCharacter")/

    .d-flex.flex-column.col-6
      label.col-sm-2.col-form-label.m-auto Realm

      .col-sm-11.m-auto
        input.col-12(v-model="inputRealm")/

  .d-flex.flex-row.mx-2.my-2.gap-1
    textarea.form-control.jsonarea(
      readonly,
      v-model="inputText",
      rows="20",
      placeholder="Raw Data will show here."
    )/

    textarea.form-control.jsonarea(
      readonly,
      v-model="outputText",
      rows="20",
      placeholder="Type Data Here."
    )/
  .d-flex
    button.btn.btn-secondary.m-auto(@click="query()") Submit
</template>

<style>
.jsonarea {
  font-family: Consolas, Monaco, Lucida Console, Liberation Mono,
    DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace;
}
</style>

<script>
import { ref } from "vue";
import { queryRaidData, parseData, dataToTable } from "../query.js";

export default {
  setup() {
    const inputCharacter = ref("Yapriesty");
    const inputRealm = ref("Azralon");
    const inputAreaText = ref("");
    const outputAreaText = ref("");

    async function query() {
      var data = await queryRaidData(this.inputCharacter, this.inputRealm);
      this.inputText = JSON.stringify(data);

      var parsedData = await parseData(data);
      this.outputText = dataToTable(parsedData).toString();
    }

    return {
      inputCharacter,
      inputRealm,
      inputText: inputAreaText,
      outputText: outputAreaText,
      query,
    };
  },
};
</script>