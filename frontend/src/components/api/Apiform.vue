<template>
  <div style="padding-left: 20px">
    <el-form ref="form" :disabled="isView" :model="apiform" label-width="100px" align="left">
      <div class="separate" style="margin-top: 0">基础信息</div>
      <el-row>
        <el-col :span="12">
          <el-form-item label="接口名称：">
            <el-input v-model="apiform.api_name"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12" style="padding-left: 20px">
          <el-form-item label="请求方法：">
            <el-select v-model="apiform.request_method" placeholder="请求方法" @change="setActiveName">
              <el-option v-for="method in common.requestMethod" :key="method" :label="method"
                         :value="method"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="状  态：">
            <el-select v-model="apiform.status" placeholder="状  态">
              <el-option v-for="status in common.status" :key="status.value" :label="status.title"
                         :value="status.value"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12" style="padding-left: 20px">
          <el-form-item label="责  任  人：">
            <el-select v-model="apiform.owner" filterable placeholder="责任人">
              <el-option v-for="owner in common.owner" :key="owner.value" :label="owner.title"
                         :value="owner.value"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="接口路径：">
        <el-input v-model="apiform.path"></el-input>
      </el-form-item>
      <el-form-item label="接口描述：">
        <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 6}" v-model="apiform.memo"></el-input>
      </el-form-item>

      <div class="separate">请求参数</div>
      <el-tabs v-model="activeName" style="padding-bottom: 30px">
        <el-tab-pane label="Params" name="first">
          <params-table v-model="apiform.params" :column-type="columntype" :optiontype="optiontype"
                        :options="options" :is-show-del="true" :disabled="isView"></params-table>
        </el-tab-pane>
        <el-tab-pane label="Body" name="second">
          <!--          <json-viewer v-if="isView" v-model="apiform.base_body" :expand-depth=5 copyable boxed sort></json-viewer>-->
          <params-table v-model="apiform.base_body" :column-type="columntype" :optiontype="optiontype"
                        :options="options" :is-show-del="true" :disabled="isView"></params-table>
        </el-tab-pane>
        <el-tab-pane label="Base_Headers" name="third">
          <json-viewer v-if="isView" v-model="apiform.base_head" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isEdit||isNew" v-model="apiform.base_head" :is-show-form="false"></json-code>
        </el-tab-pane>
        <el-tab-pane label="Base_Cookies" name="fourth">
          <json-viewer v-if="isView" v-model="apiform.cookies" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isEdit||isNew" v-model="apiform.cookies" :is-show-form="false"></json-code>
        </el-tab-pane>
      </el-tabs>
      <el-button type="primary" @click="outMsg" plain v-if="isNew||isEdit">
        测试运行
        <i class="el-icon-caret-right el-icon--right"></i>
      </el-button>
      <div class="separate">期望返回值</div>
      <!--      <json-viewer v-if="isView" v-model="apiform.base_expect" :expand-depth=5 copyable boxed sort></json-viewer>-->
      <!--      <json-code v-model="apiform.base_expect" :is-show-form="true"></json-code>-->
      <params-table v-model="apiform.base_expect" :column-type="columntype" :optiontype="optiontype"
                    :options="options" :is-show-del="true"></params-table>
      <el-form-item style="padding-top: 20px" v-if="isNew||isEdit">
        <el-button type="primary" @click="onSubmit">保存</el-button>
        <el-button @click="goBackPage">取消</el-button>
      </el-form-item>
    </el-form>
    <el-row style="margin: 20px" v-if="isView">
      <el-button type="primary" @click="goBackPage">返回</el-button>
    </el-row>
  </div>
</template>

<script>
  import common from "../../common/js/common";
  import ParamsTable from "../common/ParamsTable";
  import JsonInput from "../common/JsonInput";
  import "codemirror/theme/ambiance.css"; // 这里引入的是主题样式，根据设置的theme的主题引入，一定要引入！！
  import "codemirror/theme/idea.css"
  import "codemirror/mode/javascript/javascript"; // 这里引入的模式的js，根据设置的mode引入，一定要引入！！
  import JsonCode from "../common/JsonCode";

  export default {
    name: "Apiform",
    components: {ParamsTable, JsonInput, JsonCode},
    data() {
      return {
        apiform: {
          api_name: '',
          path: '',
          memo: '',
          request_method: 'GET',
          params: [JSON.parse(JSON.stringify(common.formDataNull))],
          cookies: '{}',
          base_head: '{}',
          base_body: [JSON.parse(JSON.stringify(common.formDataNull))],
          base_expect: [JSON.parse(JSON.stringify(common.formDataNull))],
          owner: '',
          status: '',
        },
        common: common,
        activeName: 'first',
        cmOptions: {
          // value: '',    //默认初始值
          mode: "application/json",   //支持的语言
          theme: "idea",      //主题风格
          lineNumbers: true,   //是否显示行号
        },
        isView: false,
        isEdit: false,
        isNew: true,
        columntype: [],
        optiontype: [],
        options: [],
      }
    },
    mounted() {
      this.isView = this.$route.name === 'detailapi';
      this.isEdit = this.$route.name === 'editapi';
      this.isNew = this.$route.name === 'newapi';
      if (this.isEdit || this.isView) {
        this.setApiForm(this.$route.query.apiId);
      }
      ;
      this.getColumnType();
      this.getOptionType();
      this.getOptions();
    },

    methods: {
      onSubmit() {
        let that = this;
        let url = common.baseUrl + common.newapi;
        let bodydata = JSON.parse(JSON.stringify(that.apiform));
        let paramList = [bodydata.params, bodydata.base_body, bodydata.base_expect];
        //提交时需要去掉最后一行空的

        if (common.need_del_null(bodydata.params)) {
          bodydata.params.pop();
        }
        if (common.need_del_null(bodydata.base_expect)) {
          bodydata.base_expect.pop();
        }
        if (common.need_del_null(bodydata.base_body)) {
          bodydata.base_body.pop();
        }
        bodydata.params = JSON.stringify(bodydata.params);
        bodydata.base_expect = JSON.stringify(bodydata.base_expect);
        bodydata.base_body = JSON.stringify(bodydata.base_body);
        if (that.isEdit) {
          url = common.baseUrl + common.editapi;
          bodydata['id'] = that.$route.query.apiId;
        }
        that.$axios
          .post(url, bodydata)
          .then(res => {

              let msg = that.isNew ? "恭喜您添加接口成功！" : "恭喜您编辑接口成功！";
              this.$router.push({name: 'apilist'});
              this.$message({
                type: "success",
                message: msg,
                showClose: true
              });
            }
          )
          .catch(err => {
            this.$message({
              type: "error",
              message: "保存接口失败，错误信息：" + err.toString(),
              showClose: true
            });
            console.log(err.toString())
          })
      },
      goBackPage: function () {
        if (!this.isView) {
          let msg = this.isNew ? '您确定需要取消新增API吗?' : '您确定需要取消编辑API吗?';
          let that = this;
          this.$confirm(msg, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(function () {
            that.$router.go(-1);
          }).catch(function (err) {
            console.log(err.toString())
          });
        } else {
          this.$router.go(-1);
        }

      },
      setActiveName: function () {
        if (this.apiform.request_method === 'GET') {
          this.activeName = 'first';
          console.log("请求等于GET")
        } else {
          this.activeName = 'second';
        }
      },
      setApiForm: function (apiid) {
        let that = this;
        that.$axios
          .get(common.baseUrl + "api/" + apiid.toString() + common.detailapi)
          .then(res => {
            if (res.data.status) {
              that.apiform = res.data.data;
              //需要将表格数据的字符串转为对象
              that.apiform.params = JSON.parse(that.apiform.params ? that.apiform.params : []);
              that.apiform.base_head = JSON.parse(that.apiform.base_head ? that.apiform.base_head : {});
              that.apiform.cookies = JSON.parse(that.apiform.cookies ? that.apiform.cookies : {});
              //查看的时候，需要将字符串转为json，才能在插件中高亮跟折叠
              that.apiform.base_body = JSON.parse(that.apiform.base_body ? that.apiform.base_body : []);
              that.apiform.base_expect = JSON.parse(that.apiform.base_expect ? that.apiform.base_expect : []);
              if (that.isEdit) {
                // 编辑的时候自动新增一行空数据
                that.apiform.base_head = that.apiform.base_head ? JSON.stringify(that.apiform.base_head) : '{}';
                that.apiform.cookies = that.apiform.cookies ? JSON.stringify(that.apiform.cookies) : '{}';
                that.apiform.params.push(JSON.parse(JSON.stringify(common.formDataNull)));
                that.apiform.base_body.push(JSON.parse(JSON.stringify(common.formDataNull)));
                that.apiform.base_expect.push(JSON.parse(JSON.stringify(common.formDataNull)));
              }
            } else {
              this.$message({
                type: "error",
                message: "获取API信息失败，错误信息：" + res.msg.toString(),
                showClose: true
              });
            }
          }).catch(err => {
          this.$message({
            type: "error",
            message: "数据赋值失败，错误信息：" + err.toString(),
            showClose: true
          });
          console.log(err.toString())
        })
      },
      outMsg: function () {
        console.log(this.apiform.base_expect)
      },
      getColumnType() {
        let that = this;
        that.$axios
          .get(common.baseUrl + common.columntypelist)
          .then(function (res) {
            if (res.data.status === 1) {
              that.columntype = res.data.data;
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
      getOptionType() {
        let that = this;
        that.$axios
          .get(common.baseUrl + common.optiontypelist)
          .then(function (res) {
            if (res.data.status === 1) {
              that.optiontype = res.data.data;
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
      getOptions() {
        let that = this;
        that.$axios
          .get(common.baseUrl + common.optionlist)
          .then(function (res) {
            if (res.data.status === 1) {
              that.options = res.data.data;
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
    },
  }
</script>

<style scoped>


</style>

