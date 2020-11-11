<template>
  <div>
    <el-table :data="value" style="width: 100%" size="mini">
      <el-table-column type="expand">
        <template slot-scope="prop">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item v-for="(item,index) in value[prop.$index].condition" :key="index" :label="condioptions[index].title">
              <el-input></el-input>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <!--      <el-table-column type="index" label="序号" width="60">-->
      <!--      </el-table-column>-->
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
              v-for="item in options"
              :key="item.value"
              :label="item.title"
              :value="item.value">
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="condition" label="取值范围">
        <template slot-scope="prop">
          <el-select v-model="value[prop.$index].condition" collapse-tags filterable multiple placeholder="取值范围" >
            <el-option
              v-for="item in condioptions"
              :key="item.value"
              :label="item.title"
              :value="item.value">
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
    <el-button v-if="false" @click="outmsg">run</el-button>
  </div>
</template>

<script>
  import common from "../../common/js/common";

  export default {
    name: "ParamsTable",
    props: ['value', 'isShowDel'],
    data() {
      return {
        options: common.valueType,
        condioptions:common.condioptions,
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
        console.log(this.value)
      },
      //切换类型的时候，把当前值置空
      setNull(index) {
        this.value[index].value = null
      },
    }
  }

</script>

<style scoped>
  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
