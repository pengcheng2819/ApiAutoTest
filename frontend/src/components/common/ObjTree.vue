<template>
  <div class="block">
    <el-tree
      :data="data"
      draggable
      node-key="id"
      default-expand-all
      @node-click="setCheck(data,node)"
      :expand-on-click-node="false">
      <span style="height: 50px" class="custom-tree-node" slot-scope="{ node, data }">
        <span>{{ node.label }}</span>

        <span>
          <el-button
            type="text"
            size="mini"
            icon="el-icon-plus"
            circle
            @click="inputOpen(data)">
          </el-button>
          <el-button
            type="text"
            size="mini"
            icon="el-icon-delete"
            circle
            @click="() => remove(node, data)">
          </el-button>
        </span>
      </span>
    </el-tree>


    <el-dialog title="设置本节点校验条件" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="对比选项" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="请选择活动区域">
            <el-option v-for="select in  checkSelect" :label="select.title" :value="select.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="对比值:" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  let id = 1000;
  export default {
    name: "Tree",
    // props: ['value'],
    data() {
      const data = [
        {
          id: 1,
          label: '一级 1',
          children: [{
            id: 4,
            label: '二级 1-1',
            children: [{
              id: 9,
              label: '三级 1-1-1'
            }, {
              id: 10,
              label: '三级 1-1-2'
            }]
          }]
        }, {
          id: 2,
          label: '一级 2',
          children: [{
            id: 5,
            label: '二级 2-1'
          }, {
            id: 6,
            label: '二级 2-2'
          }]
        }, {
          id: 3,
          label: '一级 3',
          children: [{
            id: 7,
            label: '二级 3-1'
          }, {
            id: 8,
            label: '二级 3-2'
          }]
        }];
      return {
        data: JSON.parse(JSON.stringify(data)),
        dialogFormVisible: false,
        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        checkSelect: [
          {"title": "包含对比值", "value": "include"},
          {"title": "对比值被包含", "value": "included"},
          {"title": "等于对比值", "value": "equal"},
          {"title": "大于对比值", "value": "gt"},
          {"title": "小于对比值", "value": "lt"},
        ],
        formLabelWidth: '120px'
      }
    },
    methods: {
      append(data, value) {
        const newChild = {id: id++, label: value, children: []};
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.push(newChild);
      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },

      inputOpen(data) {
        this.$prompt('请输入节点名称', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({value}) => {
          this.append(data, value);
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
      },

      setCheck(data, node) {
        this.dialogFormVisible = true;
      },
    }
  }
</script>

<style scoped>
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 15px;
    padding-right: 8px;
    height: 50px;
  }
</style>
