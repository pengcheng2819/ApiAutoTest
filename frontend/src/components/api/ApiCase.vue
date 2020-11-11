<template>
    <router-view>
      <api-case-form></api-case-form>
      <api-case-list></api-case-list>
    </router-view>
</template>

<script>
  import ApiCaseForm from "./ApiCaseForm";
  import ApiCaseList from "./ApiCaseList";
    export default {
        name: "ApiCase",
      components: {ApiCaseList, ApiCaseForm}
    }
</script>

<style scoped>

</style>
