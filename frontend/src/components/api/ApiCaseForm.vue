<template>
  <div style="padding-left: 20px">
    <el-form ref="form" :disabled="isView" :model="form" label-width="100px" align="left">
      <div class="separate" style="margin-top: 0">基础信息</div>
      <el-row>
        <el-col :span="12">
          <el-form-item label="所属接口：">
            <el-select v-model="form.api" filterable placeholder="所属接口" @change="setBaseValue">
              <el-option v-for="(api,key) in apilist" :key="key" :label="api.api_name"
                         :value="api.id"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12" style="padding-left: 20px">
          <el-form-item label="请求方法：">
            <el-select v-model="form.request_method" placeholder="请求方法" disabled>
              <el-option v-for="method in common.requestMethod" :key="method.value" :label="method.title"
                         :value="method.value"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="接口路径：">
        <el-input v-model="form.path" disabled></el-input>
      </el-form-item>

      <el-form-item label="用例名称：">
        <el-input v-model="form.case_name"></el-input>
      </el-form-item>


      <el-form-item label="用例描述：">
        <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 6}" v-model="form.memo"></el-input>
      </el-form-item>
      <div class="separate">请求参数</div>
      <el-tabs v-model="activeName" style="padding-bottom: 30px">
        <el-tab-pane label="Params" name="first">
          <json-viewer v-if="isView" v-model="form.params" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isNew||isEdit" v-model="form.params" :is-show-form="false"></json-code>
        </el-tab-pane>
        <el-tab-pane label="Body" name="second">
          <json-viewer v-if="isView" v-model="form.body" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isNew||isEdit" v-model="form.body" :is-show-form="false"></json-code>
        </el-tab-pane>
        <el-tab-pane label="Headers" name="third">
          <json-viewer v-if="isView" v-model="form.head" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isNew||isEdit" v-model="form.head" :is-show-form="false"></json-code>
        </el-tab-pane>
        <el-tab-pane label="Cookies" name="fourth">
          <json-viewer v-if="isView" v-model="form.cookies" :expand-depth=5 copyable boxed sort></json-viewer>
          <json-code v-if="isNew||isEdit" v-model="form.cookies" :is-show-form="false"></json-code>
        </el-tab-pane>
      </el-tabs>
      <el-button type="primary" plain @click="testRunCase" v-if="isNew||isEdit">
        测试运行
        <i class="el-icon-caret-right el-icon--right"></i>
      </el-button>
      <div class="separate">期望返回值</div>
      <json-viewer v-if="isView" v-model="form.expect" :expand-depth=5 copyable boxed sort></json-viewer>
      <json-code v-if="isEdit||isNew" v-model="form.expect" :is-show-form="false"></json-code>

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
    name: "ApiCaseForm",
    components: {ParamsTable, JsonInput, JsonCode},
    data() {
      return {
        apilist: [],
        form: {
          case_name: '',
          api: '',
          path: '',
          request_method: '',
          params: '{}',
          cookies: '{}',
          head: '{}',
          body: '{}',
          expect: '{}',
          status: 1,
        },
        common: common,
        activeName: 'second',
        cmOptions: {
          // value: '',    //默认初始值
          mode: "application/json",   //支持的语言
          theme: "idea",      //主题风格
          lineNumbers: true,   //是否显示行号
        },
        isView: false,
        isEdit: false,
        isNew: true,
      }
    },
    mounted() {
      this.getApiList();
      this.isView = this.$route.name === 'detailcase';
      this.isEdit = this.$route.name === 'editcase';
      this.isNew = this.$route.name === 'newcase';
      document.body
      if (this.isEdit || this.isView) {
        this.setCaseForm(this.$route.query.caseId);
      }
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
      onSubmit() {
        let that = this;
        let url = common.baseUrl + common.newapicase;
        let bodydata = JSON.parse(JSON.stringify(that.form));
        //编辑的时候带上ID
        if (that.isEdit) {
          url = common.baseUrl + common.editapicase;
          bodydata['id'] = that.$route.query.caseId;
          if ('create_time' in bodydata) {
            delete bodydata.create_time;
          }
          if ('update_time' in bodydata) {
            delete bodydata.update_time;
          }

        }
        that.$axios
          .post(url, bodydata)
          .then(res => {
              let msg = that.isNew ? "恭喜您添加接口成功！" : "恭喜您编辑接口成功！";
              this.$router.push({
                name: 'caselist'
              });
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
          let msg = this.isNew ? '您确定需要取消新增Case吗?' : '您确定需要取消编辑Case吗?';
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
      setCaseForm: function (caseid) {
        let that = this;
        that.$axios
          .get(common.baseUrl + "api/" + caseid.toString() + common.detailapicase)
          .then(res => {
            if (res.data.status) {
              that.form = res.data.data;
              if (that.isView) {
                //查看的时候，需要将字符串转为json，才能在插件中高亮跟折叠
                that.form.body = JSON.parse(that.form.body);
                that.form.expect = JSON.parse(that.form.expect);
                that.form.params = JSON.parse(that.form.params);
                that.form.head = JSON.parse(that.form.head);
                that.form.cookies = JSON.parse(that.form.cookies);
              }
            } else {
              this.$message({
                type: "error",
                message: "获取Case信息失败，错误信息：" + res.msg.toString(),
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
      setBaseValue: function () {
        if (this.form.api) {
          let that = this;
          that.$axios
            .get(common.baseUrl + "api/" + that.form.api.toString() + common.detailapi)
            .then(res => {
              if (res.data.status) {
                let apidata = res.data.data;
                // that.form = res.data.data;
                //需要将表格数据的字符串转为对象
                that.form.params = this.formToJson(JSON.parse(apidata.params));
                that.form.head = this.formToJson(JSON.parse(apidata.base_head));
                that.form.cookies = this.formToJson(JSON.parse(apidata.cookies));
                that.form.body = this.formToJson(JSON.parse(apidata.base_body));
                that.form.expect = this.formToJson(JSON.parse(apidata.base_expect));
                that.form.path = apidata.path;
                that.form.request_method = apidata.request_method;

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
        }
      },
      formToJson(fromObject) {
        let obj = {};
        for (let index = 0; index < fromObject.length - 1; index++) {
          obj[fromObject[index].paramname] = fromObject[index].value;
        }
        return JSON.stringify(obj);

      },
      testRunCase: function () {
        let that = this;
        let url = common.baseUrl + common.testruncase;
        let bodydata = JSON.parse(JSON.stringify(this.form));
        console.log(bodydata);
        console.log(url);
        that.$axios
          .post(url, bodydata)
          .then(res => {

          that.form.expect = res.data;

            }
          )
          .catch(err => {
            this.$message({
              type: "error",
              message: "调用测试运行接口失败，错误信息：" + err.toString(),
              showClose: true
            });
            console.log(err.toString())
          })
      },
    }
    ,
  }


</script>

<style scoped>
  .separate {
    border-left: 6px solid #409eff;
    padding-left: 20px;
    margin-bottom: 30px;
    margin-top: 20px;
    color: #409eff;
  }

  .el-select {
    width: 100%;
  }
</style>
