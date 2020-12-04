<template>
  <div>
    <el-table :data="value" style="width: 100%" size="mini" default-expand-all>
      <el-table-column type="expand">
        <template slot-scope="prop">
          <el-form label-width="100px" align="left" :disabled="disabled">

            <el-form-item v-for="(item,index) in value[prop.$index].condition" :key="index"
                          :label="getOptionTypes(item)[0].title">
              <el-row>
                <el-col :span="6">
                  <el-select filterable v-model="value[prop.$index].conditionValue[item]">
                    <el-option v-for="item in getOptions(item)"
                               :key="item.value"
                               :label="item.title"
                               :value="getObj(item)"></el-option>
                  </el-select>
                </el-col>
                <el-col :span="6" style="padding-left: 20px"
                        v-if="isShow(value[prop.$index].conditionValue[item],'input')">
                  <el-input v-model="value[prop.$index].conditionValue[item].input[0]"></el-input>
                </el-col>
                <el-col :span="12" style="padding-left: 20px"
                        v-if="isShow(value[prop.$index].conditionValue[item],'input-input')">
                  <el-row>
                    <el-col :span="6">
                      <el-input v-model="value[prop.$index].conditionValue[item].input[0]"></el-input>
                    </el-col>
                    <el-col :span="6" style="padding-left: 20px">
                      <el-input v-model="value[prop.$index].conditionValue[item].input[1]"></el-input>
                    </el-col>
                  </el-row>
                </el-col>
                <el-col :span="6" style="padding-left: 20px"
                        v-if="isShow(value[prop.$index].conditionValue[item],'select')">
                  <el-select v-model="value[prop.$index].conditionValue[item].input[0]">
                    <el-option v-for="item in optionInput[value[prop.$index].conditionValue[item].value]"
                               :key="item.value"
                               :label="item.title"
                               :value="item.value"></el-option>
                  </el-select>
                </el-col>
                <el-col :span="12" style="padding-left: 20px"
                        v-if="isShow(value[prop.$index].conditionValue[item],'select-input')">
                  <el-row>
                    <el-col :span="6">
                      <el-select v-model="value[prop.$index].conditionValue[item].input[0]">
                        <el-option v-for="item in optionInput[value[prop.$index].conditionValue[item].value]"
                                   :key="item.value"
                                   :label="item.title"
                                   :value="item.value"></el-option>
                      </el-select>
                    </el-col>
                    <el-col :span="6" style="padding-left: 20px">
                      <el-input v-model="value[prop.$index].conditionValue[item].input[1]"></el-input>
                    </el-col>
                  </el-row>
                </el-col>
              </el-row>
            </el-form-item>


          </el-form>
        </template>
      </el-table-column>
      <el-table-column type=" index
                    " label="序号" width="60">
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
          <el-select v-model="value[prop.$index].type" filterable placeholder="值类型" @change="setNull(prop.$index)">
            <el-option
              v-for="item in columnType"
              :key="item.value"
              :label="item.title"
              :value="item.value">
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="condition" label="测试点">
        <template slot-scope="prop">
          <el-select v-model="value[prop.$index].condition" collapse-tags filterable multiple placeholder="测试点"
                     @change="setConditionValue(value[prop.$index])">
            <el-option
              v-for="item in getOpTyByColTy(value[prop.$index].type)"
              :key="item.typekey"
              :label="item.title"
              :value="item.typekey">
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
    <el-button v-if="false" @click="outmsg">outmsg</el-button>
  </div>
</template>

<script>
  import common from "../../common/js/common";

  export default {
    name: "ParamsTable",
    props: ['value', 'columnType', 'optiontype', 'options', 'isShowDel', 'disabled'],
    data() {
      return {
        optionInput: {
          'date': [
            {
              'title': '日期',
              'value': 'date'
            },
            {
              'title': '时间',
              'value': 'time'
            },
            {
              'title': '时间戳',
              'value': 'timestamp'
            },
            {
              'title': '日期时间',
              'value': 'datetime'
            },
          ]
        }
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
        console.log(typeof this.value);
      },
      //切换类型的时候，把当前值置空
      setNull(index) {
        this.value[index].condition = [];
      },
      //根据值获取选项类型
      getOptionTypes(value) {
        let item = this.optiontype.filter(item => item.typekey == value);
        if (item[0]) {
          return item;
        } else {
          return [{'title': '未知'}]
        }
      },

      //根据值类型过滤测试点
      getOpTyByColTy(type) {
        return this.optiontype.filter(item => item.column_type == type);
      },
      //根据类型获取选项列表
      getOptions(type) {
        return this.options.filter(item => item.option_type == type);
      },
      //找到特定的选项
      getOption(value) {
        return this.options.filter(item => item.value == value)
      },
      //是否需要显示控件
      isShow(item, str) {
        if (item && this.getOption(item.value)[0]) {
          let widget = this.getOption(item.value)[0];
          return widget.widget == str;
        } else
          return false;
      },
      //给条件赋值对象
      getObj(item) {
        let itemc = {};
        itemc.title = item.title;
        itemc.value = item.value;
        itemc.input = [];
        return itemc
      },

      //取消选择测试点的时候，删除相应的选项
      setConditionValue(item) {
        for (var iv in item.conditionValue) {
          if (item.condition.indexOf(iv) === -1) {
            delete item.conditionValue[iv];
          }
        }
      },

    },

  }

</script>

<style>
  .el-form-item {
    margin-right: 15px;
    margin-bottom: 10px;
  }
</style>
