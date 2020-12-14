<template>
  <div style="height: auto;">
    <el-row style="padding-bottom: 20px">
      <el-col :span="16" align="left">
        <el-input placeholder="搜索API" v-model="search.text" style="background-color: #E9EEF3;width: 80%;"
                  @change="queryApiList">
          <el-select v-model="search.method" clearable slot="prepend" style="width: 110px" @change="queryApiList"
                     placeholder="请求方法">
            <el-option v-for="method in common.requestMethod" :key="method" :label="method"
                       :value="method"></el-option>
          </el-select>
          <i v-if="search.text" slot="suffix" class="el-input__icon el-icon-close "
             @click="deleteSearch"></i>
          <el-button slot="append" icon="el-icon-search" @click="queryApiList"></el-button>
        </el-input>
      </el-col>

      <el-col :span="8" align="right">
        <el-button-group>
          <el-button type="primary" icon="el-icon-plus" @click="newApiRouter">新增</el-button>
          <el-button type="primary" icon="el-icon-upload2">导入</el-button>
          <el-button type="primary" icon="el-icon-download">导出</el-button>
        </el-button-group>
      </el-col>
    </el-row>

    <el-table :data="pageapis" align="center" style="width: 100%" :default-sort="{prop: 'id', order: 'descending'}"
              size="mini" @selection-change="setChoiceId">
      <el-table-column type="selection"></el-table-column>
      <el-table-column prop="id" label="ID" width="65" align="center" sortable></el-table-column>
      <el-table-column prop="api_name" label="接口名称" width="180" align="center" sortable></el-table-column>
      <el-table-column prop="path" label="路径" align="center" sortable></el-table-column>
      <el-table-column prop="request_method" width="100" label="请求方法" sortable></el-table-column>
      <el-table-column prop="owner" width="100" label="责任人" sortable></el-table-column>
      <el-table-column prop="create_time" label="创建时间"
                       sortable :formatter="formatDate"></el-table-column>
      <el-table-column prop="status" width="100" align="center" label="状态" :formatter="statusFormat"
                       sortable></el-table-column>
      <el-table-column label="操作" align="center" width="60">
        <template slot-scope="scope">
          <el-dropdown>
            <el-button icon="el-icon-edit" circle type="info" plain size="mini"></el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <span type="success" @click="detailApiRouter(scope.row.id)">查看详情</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span type="primary" @click="editApiRouter(scope.row.id)">编辑接口</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span type="primary" @click="createCase(scope.row.id)">生成case</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span type="primary" @click="createCaseOne(scope.row.id)">测试生成case</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span @click="deleteApi([scope.row.id])">删除接口</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>

    <el-row style="margin-top:20px" align="middle">
      <el-col :span="8" align="left">
        <el-button type="primary" icon="el-icon-delete" size="medium" @click="deleteAll">批量删除</el-button>
      </el-col>
      <el-col :span="16" align="right">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentpage"
          :page-sizes="pagesizes"
          :page-size="pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total" small>
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import common from "../../common/js/common";
  import {Loading} from 'element-ui'
  export default {
    name: "ApiList",
    data() {
      return {

        apilist: [],    //全部的api数据
        pageapis: [],    //当前页的api
        total: 0, //总页数
        currentpage: common.currentpage,   //当前页
        pagesize: common.pagesize,     //每页展示行数
        pagesizes: common.pagesizes,    //可选分页行数
        search: {
          method: '',
          text: '',
        },
        selectIds: '',
        common: common,
      }
    },
    mounted() {
      this.getApiList();
    },
    methods: {
      getApiList: function () {
        let that = this;
        that.$axios
          .get(common.baseUrl + common.apilist)
          .then(function (res) {
            if (res.data.status === 1) {
              that.apilist = res.data.data;
              if (that.apilist) {
                that.total = res.data.data.length;
              }
              that.getPageApis()
            } else {

              that.$message({
                message: res.data.msg,
                type: 'error',
                showClose: true
              });
            }
          })
          .catch(function (err) {
            that.$message.error(err.toString());
          })
      },
      queryApiList: function () {
        this.currentpage = 1;
        let that = this;
        that.$axios
          .post(common.baseUrl + common.queryapilist, that.search)
          .then(res => {
            if (res.data.status === 1) {
              that.apilist = res.data.data;
              if (that.apilist) {
                that.total = res.data.data.length;
              }else {
                that.total=0;
              }
              that.getPageApis();
            } else {
              this.$message({
                type: 'error',
                message: '查询失败' + res.data.msg
              });
            }
          })
          .catch(err => {
            this.$message({
              type: 'error',
              message: '查询失败' + err.toString()
            });
          });
      },
      deleteSearch: function () {
        this.search.text = '';
        this.search.method = '';
        this.getApiList();
      },
      handleSizeChange(val) {
        this.pagesize = val;
        this.getPageApis()
      },
      handleCurrentChange(val) {
        this.currentpage = val;
        this.getPageApis()
      },
      getPageApis: function () {
        this.pageapis = [];
        for (let i = 0, start = (this.currentpage - 1) * this.pagesize;
             i < this.pagesize && start < this.total; i++, start++) {
          this.pageapis.push(this.apilist[start]);
        }
      },
      newApiRouter: function () {
        this.$router.push({
          name: 'newapi',
        })
      },
      editApiRouter: function (apiId) {
        this.$router.push({
          name: 'editapi',
          query: {apiId: apiId}
        })
      },
      detailApiRouter: function (apiId) {
        this.$router.push({
          name: 'detailapi',
          query: {apiId: apiId}
        })
      },
      createCase: function (id) {
        this.$confirm('您确定需要为I为【' + id.toString() + '】的接口自动生成case吗?如果已经生成过，则会删除旧的重新生成', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            let that = this;
            this.openFullScreen();
            that.$axios
              .post(common.baseUrl + common.createcase, {
                id: id,
                istest: false,
              })
              .then(res => {
                if (res.data.status === 1) {
                  that.getApiList();
                  this.closeFullScreen(this.openFullScreen());
                  this.$message({
                    type: 'success',
                    message: '生成成功!'
                  });
                } else {
                  this.closeFullScreen(this.openFullScreen());
                  this.$message({
                    type: 'error',
                    message: '生成失败' + res.data.msg
                  });
                }
              })
              .catch(err => {
                this.closeFullScreen(this.openFullScreen());
                this.$message({
                  type: 'error',
                  message: '生成失败' + err.toString()
                });
              });

          }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消生成'
          });
        });
      },
      createCaseOne: function (id) {
        this.$confirm('您确定需要为I为【' + id.toString() + '】的接口自动生成一条case吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            let that = this;
            that.$axios
              .post(common.baseUrl + common.createcase, {
                id: id,
                istest: true,
              })
              .then(res => {
                if (res.data.status === 1) {
                  that.getApiList();
                  this.$message({
                    type: 'success',
                    message: '生成成功!'
                  });
                } else {
                  this.$message({
                    type: 'error',
                    message: '生成失败' + res.data.msg
                  });
                }
              })
              .catch(err => {
                this.$message({
                  type: 'error',
                  message: '生成失败' + err.toString()
                });
              });

          }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消生成'
          });
        });
      },
      deleteApi: function (ids) {
        this.$confirm('您确定需要删除ID为【' + ids.toString() + '】的接口吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            let that = this;
            that.$axios
              .post(common.baseUrl + common.deleteapi, {
                id: ids
              })
              .then(res => {
                if (res.data.status === 1) {
                  that.getApiList();
                  this.$message({
                    type: 'success',
                    message: '删除成功!'
                  });
                } else {
                  this.$message({
                    type: 'error',
                    message: '删除失败' + res.data.msg
                  });
                }
              })
              .catch(err => {
                this.$message({
                  type: 'error',
                  message: '删除失败' + err.toString()
                });
              });

          }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      openFullScreen: function(){
        const loading = this.$loading({
          lock:true,
          text:'正在努力,请稍候',
          spinner:'el-icon-loading',
          background:'rgba(0,0,0,0.7)'
        });
        return loading;
      },
      closeFullScreen(loading){
        loading.close();
      },
      statusFormat: function (row, column) {
        for (var index in common.status) {
          if (row.status === common.status[index].value)
            return common.status[index].title;
        }
        return '无效状态';
      },
      formatDate: function (row, column, cellValue, index) {
        return common.formatDateTime(cellValue)
      },

      setChoiceId: function (selection) {
        this.selectIds = selection;
      },
      deleteAll: function () {
        if (this.selectIds.length) {
          let delIds = [];
          for (let i = 0; i < this.selectIds.length; i++) {
            delIds.push(this.selectIds[i].id);
          }
          this.deleteApi(delIds.sort())
        } else {
          this.$message({
            type: 'info',
            message: '至少要选中一个接口，才能使用批量删除功能！'
          })
        }
      }
    },

  }
</script>

<style scoped>

</style>
