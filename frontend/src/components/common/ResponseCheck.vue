<template>
  <div>
    <el-table :data="value" style="width: 100%" size="mini" default-expand-all
              :tree-props="{children: 'children', hasChildren: 'hasChildren'}">
      <el-table-column type=" index
                    " label="序号" width="60">
      </el-table-column>
      <el-table-column prop="paramname" label="参数名" width="220">
        <template slot-scope="prop">
          <el-input v-model="value[prop.$index].paramname" disabled></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="notnull" label="是否校验" width="80">
        <template slot-scope="prop">
          <el-checkbox v-model="value[prop.$index].notnull"></el-checkbox>
        </template>
      </el-table-column>
      <el-table-column prop="value" label="比对类型" width="120">
        <template slot-scope="prop">
          <el-select v-if="value[prop.$index].notnull" v-model="value[prop.$index].type" filterable placeholder="值类型"
                     @change="setNull(prop.$index)">
            <el-option
              v-for="item in columnType"
              :key="item.value"
              :label="item.title"
              :value="item.value">
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column prop="condition" label="比对值">
        <template slot-scope="prop">
          <el-input v-model="value[prop.$index].checkvalue" style="padding-right: 8px"></el-input>
        </template>
      </el-table-column>

      <el-table-column prop="memo" label="返回字段说明">
        <template slot-scope="prop">
          <el-input v-model="value[prop.$index].memo" style="padding-right: 8px"></el-input>
        </template>
      </el-table-column>

    </el-table>
    <el-button v-if="false" @click="outmsg">outmsg</el-button>
  </div>
</template>

<script>


  export default {
    name: "ResponseCheck",
    model: {
      prop: 'value',//这个字段，是指父组件设置 v-model 时，将变量值传给子组件的 value
      event: 'getValue'//这个字段，是指父组件监听 getValue 事件
    },
    props: {
      value: [Object],
      isShowRaw: {
        type: Boolean,
        required: false,
        default: true
      }
    },
    data() {
      return {
        list:[]
      }
    },
    mounted() {

    },
    methods: {
      setList(value,listc){
        var obj = {name:value}
        if(Object.prototype.toString.call(value)==="[object Object]"){
          obj = {name:value,children: []};
          for(var v in value){
            this.setList(value[v],obj['children'])
          }
        }else {
           listc.push(obj);
        }
      },
      outmsg: function () {
        console.log(typeof this.value);
      },
      //切换类型的时候，把当前值置空
      setNull(index) {
        this.value[index].checkvalue = '';
      },

    },
  }
</script>

<style scoped>

</style>
