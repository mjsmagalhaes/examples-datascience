<template>
  <div>
    <div>Vue says Hello {{ name }}!!!</div>

    <span>
      font-awesome: <i class="fa-solid fa-sliders"></i>
      <i class="fa-solid fa-coffee"></i
    ></span>

    <div class="mb-3 row">
      <div class="d-flex flex-column col-6">
        <label for="inputPassword" class="col-2 col-form-label m-auto">
          Character
        </label>
        <div class="col-sm-11 m-auto">
          <input class="col-12" v-model="inputCharacter" />
        </div>
      </div>
      <div class="d-flex flex-column col-6">
        <label for="inputPassword" class="col-sm-2 col-form-label m-auto"
          >Realm</label
        >
        <div class="col-sm-11 m-auto">
          <input class="col-12" v-model="inputRealm" />
        </div>
      </div>
    </div>

    <div class="d-flex flex-row mx-2 my-2 gap-1">
      <textarea v-model="inputText" v-bind="inputArea"></textarea>
      <textarea v-model="outputText" v-bind="outputArea"></textarea>
    </div>

    <div class="d-flex">
      <button class="btn btn-secondary m-auto" @click="query()">Submit</button>
    </div>
  </div>
</template>

<style>
.jsonarea {
  font-family: Consolas, Monaco, Lucida Console, Liberation Mono,
    DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace;
}
</style>

<script>
import { queryRaidData, parseData, dataToTable } from "../query.js";

export default {
  data() {
    return {
      inputCharacter: "Yapriesty",
      inputRealm: "Azralon",
      inputText: "",
      inputArea: {
        class: "form-control jsonarea",
        rows: 20,
        placeholder: "Type Data Here.",
      },
      outputText: "",
      outputArea: {
        readonly: true,
        class: "form-control jsonarea",
        rows: 20,
        placeholder: "Nothing Yet.",
      },
      name: "Example",
    };
  },
  methods: {
    async query() {
      var data = await queryRaidData(this.inputCharacter, this.inputRealm);
      this.inputText = JSON.stringify(data);
      var parsedData = await parseData(data);
      this.outputText = dataToTable(parsedData).toString();
      // console.log(table);
    },
  },
};
</script>