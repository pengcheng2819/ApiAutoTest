<template>
    <router-view>
      <apiform></apiform>
      <api-list></api-list>
    </router-view>
</template>

<script>
    import Apiform from "./Apiform";
    import ApiList from "./ApiList";
    export default {
        name: "Api",
      components: {ApiList, Apiform}
    }
</script>

<style scoped>

</style>
