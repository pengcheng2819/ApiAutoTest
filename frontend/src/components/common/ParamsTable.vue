<template>
  <div>
    <el-table :data="value" style="width: 100%" size="mini" default-expand-all>
      <el-table-column type="expand">
        <template slot-scope="prop">
          <el-form label-width="100px" align="left" :disabled="disabled">

            <el-form-item v-for="(item,index) in value[prop.$index].condition" :key="index"
                          :label="getOptionTypeById(item)[0].title">
              <el-row>
                <el-col :span="5">
                  <el-select v-model="value[prop.$index].conditionValue[index]">
                    <el-option v-for="item in getOptionByTypeId(item)"
                               :key="item.id"
                               :label="item.title"
                               :value="item.id"></el-option>
                  </el-select>
                </el-col>

                <el-button>{{getWidget(value[prop.$index].conditionValue[item]).widget}}</el-button>

                <el-col :span="12" style="padding-left: 20px"
                        v-if="getWidget(value[prop.$index].conditionValue[item]).widget==='input'">
                  <el-input v-model="value[prop.$index].conditionValue[item]"></el-input>
                </el-col>
              </el-row>

            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column type="index" label="序号" width="60">
      </el-table-column>
      <el-table-column prop="paramname" label="参数名" width="220">
        <template slot-scope="prop">
          <el-input v-model="value[prop.$index].paramname" @change="addRow(prop.$index)"></el-input>
        </template>
      </el-table-column>

      <el-table-column prop="notnull" label="必需" width="60">
        <template slot-scope="prop">
          <el-checkbox v-model="value[prop.$index].notnull"></el-checkbox>
        </template>
      </el-table-column>
      <el-table-column prop="value" label="值类型" width="120">
        <template slot-scope="prop">
          <el-select v-model="value[prop.$index].type" placeholder="值类型" @change="setNull(prop.$index)">
            <el-option
              v-for="item in columnType"
              :key="item.id"
              :label="item.title"
              :value="item.id">
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="condition" label="测试点">
        <template slot-scope="prop">
          <el-select v-model="value[prop.$index].condition" collapse-tags filterable multiple placeholder="测试点">
            <el-option
              v-for="item in getOpTyByColTy(value[prop.$index].type)"
              :key="item.id"
              :label="item.title"
              :value="item.id">
            </el-option>
          </el-select>

          <!--          <el-checkbox v-if="value[prop.$index].type === 'checkbox'" v-model="value[prop.$index].value">{{value[prop.$index].value}} </el-checkbox>-->
          <!--          <el-input v-if="value[prop.$index].type === 'text'" v-model="value[prop.$index].value"></el-input>-->
          <!--          <el-input  v-if="value[prop.$index].type === 'number'" type="number" v-model.number="value[prop.$index].value"></el-input>-->
        </template>
      </el-table-column>

      <el-table-column prop="memo" label="说明">
        <template slot-scope="prop">
          <el-row>
            <el-col :span="22">
              <el-input v-model="value[prop.$index].memo"
                        style="padding-right: 8px"></el-input>
            </el-col>
            <el-col :span="2" style="padding-top: 7px;padding-left: 3px;padding-right: 3px" v-if="isShowDel">
              <el-button circle type="info" size="mini" plain
                         class="el-icon-close" v-if="prop.$index!=value.length-1"
                         @click="delRow(prop.$index)"></el-button>
            </el-col>
          </el-row>
        </template>
      </el-table-column>

    </el-table>
    <el-button v-if="true" @click="outmsg">outmsg</el-button>
  </div>
</template>

<script>
  import common from "../../common/js/common";

  export default {
    name: "ParamsTable",
    props: ['value', 'columnType', 'optiontype', 'options', 'isShowDel', 'disabled'],
    data() {
      return {
        condioptions: common.condioptions,

      }
    },
    methods: {

      addRow: function (index) {
        if (index + 1 === this.value.length) {
          this.value.push(JSON.parse(JSON.stringify(common.formDataNull)));
        }
      },
      delRow: function (index) {
        this.value.splice(index, 1);
      },
      outmsg: function () {
        console.log(this.value);
      },
      //切换类型的时候，把当前值置空
      setNull(index) {
        this.value[index].condition = [];
        this.value[index].condioptions = {};
      },

      getOptionTypeById(id) {
        return this.optiontype.filter(item => item.id == id);
      },

      //根据值类型过滤测试点
      getOpTyByColTy(columnId) {
        return this.optiontype.filter(item => item.column_type == columnId);
      },

      getOptionByTypeId(typeId) {
        return this.options.filter(item => item.option_type == typeId);
      },

      getWidget(optionId) {
        return this.options.filter(item => item.id == optionId)
      }
    },

  }

</script>

<style>
  .el-form-item {
    margin-right: 15px;
    margin-bottom: 10px;
  }
</style>
