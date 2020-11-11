<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="5">
            <div style="width: 210px;height: 50px;line-height: 50px">logo</div>
          </el-col>
          <el-col :span="19">
            <!--            <el-menu :default-active="activeName" >-->
            <!--              <el-menu-item index="1">Api测试</el-menu-item>-->
            <!--              <el-submenu index="2">WebUI测试</el-submenu>-->
            <!--              <el-menu-item index="3">APPUI测试</el-menu-item>-->
            <!--              <el-menu-item index="4">性能测试</el-menu-item>-->
            <!--            </el-menu>-->
            <el-tabs style="margin: 0;padding: 0" v-model="activeName" @tab-click="handleClick">
              <el-tab-pane label="Api测试" name="first">Api测试</el-tab-pane>
              <el-tab-pane label="WebUI测试" name="second">WebUI测试</el-tab-pane>
              <el-tab-pane label="APPUI测试" name="third">APPUI测试</el-tab-pane>
              <el-tab-pane label="性能测试" name="fourth">性能测试</el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </el-header>

      <el-container>
        <el-aside width="210px">
          <aside-menu></aside-menu>
        </el-aside>
        <el-main>
          <el-scrollbar style="height:100%;" :wrapStyle="[{'overflow-x':'hidden'}]">
            <div style="margin-right: 28px">
              <div class="breadcrumb">
                <el-row style="height: 45px">
                  <!--                <el-breadcrumb  separator-class="el-icon-arrow-right">-->
                  <!--                  <el-breadcrumb-item :to="{ name: 'home'}">首页</el-breadcrumb-item>-->
                  <!--                  <el-breadcrumb-item :to="{name:'apilist'}">接口列表</el-breadcrumb-item>-->
                  <!--                  <el-breadcrumb-item>接口详情</el-breadcrumb-item>-->
                  <!--                </el-breadcrumb>-->
                  <bread-crumb></bread-crumb>
                </el-row>
              </div>
              <router-view>
                <api></api>
                <api-case></api-case>
              </router-view>
            </div>
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

  import AsideMenu from "./components/common/AsideMenu";
  import router from "./router/index"
  import BreadCrumb from "./components/common/BreadCrumb";
  import Api from "./components/api/Api";
  import ApiCase from "./components/api/ApiCase";

  export default {
    name: 'App',
    components: {ApiCase, Api, AsideMenu, BreadCrumb},
    data() {
      return {
        activeName: "first",
      }
    },
    router: router,
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      }
    }
  }
</script>

<style>
  html, body, #app .el-container {
    margin: 0;
    padding: 0;
    height: 100%;
  }


  .el-header {
    height: 50px;
    position: absolute;
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 52px;
    top: 0;
    left: 0;
    right: 0;
  }

  .el-aside {
    display: block;
    position: absolute;
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    height: auto;
    left: 0;
    top: 50px;
    bottom: 0;
    right: 0;
  }

  .el-main {
    position: absolute;
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 40px;
    top: 50px;
    left: 210px;
    right: 0;
    bottom: 0;
    overflow: auto;
    height: auto;
    padding-right: 0;
  }

  .el-table {
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }

  /*::-webkit-scrollbar {*/
  /*  width: 0 !important;*/
  /*}*/

  /*::-webkit-scrollbar {*/
  /*  width: 0 !important;*/
  /*  height: 0;*/
  /*}*/

  .el-scrollbar .el-scrollbar__wrap {
    overflow-x: hidden;
  / / 隐藏横向滚动条 right: 0;
  }

</style>
