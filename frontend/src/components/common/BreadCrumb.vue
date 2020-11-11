<template>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item
        v-for="(item,index) in breadList"
        :key="index"
        :to="{ path: item.path }"
      >{{item.meta.title}}</el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script>
    export default {
        name: "BreadCrumb",
        data(){
          return {
            breadList:[],
          }
        },
      watch:{
          $route(){
            this.getBreadcrumb();
          }
      },
      methods:{
        isHome(route){
          return route.name === 'home';
        },
        getBreadcrumb(){
          let matched = this.$route.matched;
          if (!this.isHome(matched[0])){
            matched = [{ path: "/home", meta: { title: "首页" } }].concat(matched);
          }
          this.breadList = matched;
        },
      },
      created() {
          this.getBreadcrumb();
      }
    }
</script>

<style scoped>

</style>
