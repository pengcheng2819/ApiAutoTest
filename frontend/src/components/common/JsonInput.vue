<template>
  <div>
    <el-button @click="beautify">beautify</el-button>
    <el-input type="textarea" :autosize="{ minRows: 5, maxRows: 10}"
              v-model="jsoninput" @change="sendvalue"></el-input>
  </div>
</template>

<script>
  export default {
    name: "JsonInput",
    props: ["value"],
    data(){
      return {
        jsoninput:this.value
      }
    },
    methods: {
      beautify: function () {
        this.jsoninput = JSON.stringify(JSON.parse(this.jsoninput), null, 4);
      },
      sendvalue:function () {
        this.$emit('jsonInput', this.jsoninput)
      }
    }
  }
</script>

<style scoped>

</style>
