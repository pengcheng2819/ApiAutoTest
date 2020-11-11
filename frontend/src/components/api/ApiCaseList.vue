<template>
  <div style="height: auto;">
    <el-row style="padding-bottom: 20px">
      <el-col :span="19" align="left">
        <el-input placeholder="搜索CASE" v-model="search.text" style="background-color: #E9EEF3;width: 80%;"
                  @change="queryCaseList">
          <el-select v-model="search.api" multiple filterable collapse-tags
                     clearable slot="prepend" style="width: 180px;height: 50px" @change="queryCaseList"
                     placeholder="所属接口">
            <el-option v-for="(api,key) in apilist" :key="key" :label="api.api_name"
                       :value="api.id"></el-option>
          </el-select>
          <i v-if="search.text" slot="suffix" class="el-input__icon el-icon-close " @click="deleteSearch"></i>
          <el-button slot="append" icon="el-icon-search" @click="queryCaseList"></el-button>
        </el-input>
      </el-col>

      <el-col :span="5" align="right">
        <el-button type="primary" icon="el-icon-plus" @click="newRouter">新增用例</el-button>
      </el-col>
    </el-row>

    <el-table :data="pagedatas" align="center" style="width: 100%" :default-sort="{prop: 'id', order: 'descending'}"
              size="mini" @selection-change="setChoiceId">
      <el-table-column type="selection"></el-table-column>
      <el-table-column prop="id" label="ID" width="65" align="center" sortable></el-table-column>
      <el-table-column prop="case_name" label="用例名称" width="180" align="center" sortable></el-table-column>
      <el-table-column prop="api" label="所属接口" align="center" :formatter="apiFormat"
                       sortable></el-table-column>
      <el-table-column prop="head" label="请求头" :show-overflow-tooltip="true" sortable></el-table-column>
      <el-table-column prop="body" label="请求体" :show-overflow-tooltip="true" sortable></el-table-column>
      <el-table-column prop="expect" label="预期值" :show-overflow-tooltip="true" sortable></el-table-column>
      <el-table-column prop="create_time" label="创建时间" :formatter="formatDate"
                       sortable></el-table-column>
      <el-table-column prop="status" width="100" align="center" label="状态" :formatter="statusFormat"
                       sortable></el-table-column>
      <el-table-column label="操作" align="center" width="60">
        <template slot-scope="scope">
          <el-dropdown>
            <el-button icon="el-icon-edit" circle type="info" plain size="mini"></el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <span type="success" @click="detailRouter(scope.row.id)">详情</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span type="success" @click="runcaseRouter(scope.row.id)">运行</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span type="primary" @click="editRouter(scope.row.id)">编辑</span>
              </el-dropdown-item>
              <el-dropdown-item>
                <span @click="deleteCase([scope.row.id])">删除</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>

    <el-row style="margin-top:20px" align="middle">
      <el-col :span="8" align="left">
        <el-button type="primary" icon="el-icon-video-play" size="medium" @click="runCaseAll">批量执行</el-button>
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

  export default {
    name: "apiCaseList",
    data() {
      return {
        apilist: [],//接口列表
        datalist: [],    //全部的数据
        pagedatas: [],    //当前页的数据
        total: 0, //总条数
        currentpage: common.currentpage,   //当前页
        pagesize: common.pagesize,     //每页展示行数
        pagesizes: common.pagesizes,    //可选分页行数
        search: {
          api: [],
          text: '',
        },
        selectIds: '',
        common: common,
      }
    },
    mounted() {
      this.getList();
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
      getList: function () {
        let that = this;
        that.$axios
          .get(common.baseUrl + common.apicaselist)
          .then(function (res) {
            if (res.data.status === 1) {
              that.datalist = res.data.data;
              that.total = res.data.data.length;
              that.getPageDatas()
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
      queryCaseList: function () {
        this.currentpage = 1;
        let that = this;
        that.$axios
          .post(common.baseUrl + common.querycaselist, that.search)
          .then(res => {
            if (res.data.status === 1) {
              that.datalist = res.data.data;
              that.total = res.data.data.length;
              that.getPageDatas();
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
        this.search.api = '';
        this.getList();
      },
      handleSizeChange(val) {
        this.pagesize = val;
        this.getPageDatas()
      },
      handleCurrentChange(val) {
        this.currentpage = val;
        this.getPageDatas()
      },
      getPageDatas: function () {
        this.pagedatas = [];
        for (let i = 0, start = (this.currentpage - 1) * this.pagesize;
             i < this.pagesize && start < this.total; i++, start++) {
          this.pagedatas.push(this.datalist[start]);
        }
      },
      newRouter: function () {
        this.$router.push({
          name: 'newcase',
        })
      },
      editRouter: function (caseId) {
        this.$router.push({
          name: 'editcase',
          query: {caseId: caseId}
        })
      },
      detailRouter: function (caseId) {
        this.$router.push({
          name: 'detailcase',
          query: {caseId: caseId}
        })
      },
      runcaseRouter: function (caseId) {
        this.$router.push({
          name: 'runcase',
          query: {caseId: caseId}
        })
      },
      deleteCase: function (ids) {
        this.$confirm('您确定需要删除ID为【' + ids.toString() + '】的Case吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            let that = this;
            that.$axios
              .post(common.baseUrl + common.deleteapicase, {
                id: ids
              })
              .then(res => {
                if (res.data.status === 1) {
                  that.getList();
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
      statusFormat: function (row, column) {
        for (var index in common.status) {
          if (row.status === common.status[index].value)
            return common.status[index].title;
        }
        return '无效状态';

      },
      apiFormat: function (row, column) {
        for (var index in this.apilist) {
          if (row.api === this.apilist[index].id)
            return this.apilist[index].api_name;
        }
        return '无效接口';
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
          this.deleteCase(delIds.sort())
        } else {
          this.$message({
            type: 'info',
            message: '至少要选中一个Case，才能使用批量删除功能！'
          })
        }
      },
      runCase: function (ids) {
        this.$confirm('您确定需要运行ID为【' + ids.toString() + '】的Case吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            let that = this;
            that.$axios
              .post(common.baseUrl + common.runcase, {
                id: ids
              })
              .then(res => {
                if (res.data.status === 1) {
                  that.getList();
                  this.$message({
                    type: 'success',
                    message: '执行成功!'
                  });
                } else {
                  this.$message({
                    type: 'error',
                    message: '执行失败' + res.data.msg
                  });
                }
              })
              .catch(err => {
                this.$message({
                  type: 'error',
                  message: '执行失败' + err.toString()
                });
              });

          }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      runCaseAll: function () {
        if (this.selectIds.length) {
          let runCaseIds = [];
          for (let i = 0; i < this.selectIds.length; i++) {
            runCaseIds.push(this.selectIds[i].id);
          }
          this.runCase(runCaseIds.sort())
        } else {
          this.$message({
            type: 'info',
            message: '至少要选中一个Case，才能使用批量删除功能！'
          })
        }
      }
    },

  }
</script>

<style scoped>

</style>
