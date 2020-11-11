<template>

  <el-menu
    default-active="2"
    class="el-menu-vertical-demo" router
    @open="handleOpen"
    @close="handleClose">
    <template v-for="(route,key) in routes">
      <!--      有子级菜单显示-->
      <el-submenu v-if="route.hasOwnProperty('children')" :key="key" :index="route.path">
        <template slot="title">
          <i :class="icon[key]"></i>
          <span>{{route.meta.title}}</span>
        </template>
        <el-menu-item v-if="child.ismenu"
                      v-for="(child,key) in route.children"
                      :key="key" :index="child.path">{{child.meta.title}}
        </el-menu-item>
      </el-submenu>
      <!--      无子级菜单显示-->
      <el-menu-item v-if="!route.hasOwnProperty('children')" :key="key" :index="route.path">
        <template slot="title">
          <i :class="icon[key]"></i>
          <span>{{route.meta.title}}</span>
        </template>
      </el-menu-item>
    </template>
  </el-menu>
</template>


<script>
  export default {
    name: "AsideMenu",
    mounted() {

    },
    data() {
      return {
        routes: this.$router.options.routes,
        //按顺序列表展示图标
        icon: ['el-icon-s-home', 'el-icon-s-management','el-icon-s-order']
      }
    },
    methods: {
      handleOpen(key, keyPath) {
        // console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        // console.log(key, keyPath);
      }
    },
  }
</script>

<style scoped>

</style>
