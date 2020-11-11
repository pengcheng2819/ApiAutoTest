<template>
  <div class="code-mirror-div">
    <el-row style="margin-bottom: 5px">
      <el-col :span="12">
        <el-radio-group :disabled="false" plain v-model="isJson" size="medium">
          <el-radio-button label="raw"></el-radio-button>
          <el-radio-button label="json"></el-radio-button>
          <el-radio-button v-if="isShowForm" label="form"></el-radio-button>
        </el-radio-group>
      </el-col>
      <el-col :span="12" align="right" v-if="isJson==='json'">
        <el-select v-model="cmTheme" filterable placeholder="请选择" size="medium" style="width:120px">
          <el-option v-for="item in cmThemeOptions" :key="item" :label="item" :value="item"></el-option>
        </el-select>
        <el-select v-model="cmEditorMode" filterable placeholder="请选择" size="medium" style="width:120px"
                   @change="onEditorModeChange">
          <el-option v-for="item in cmEditorModeOptions" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </el-col>
    </el-row>

    <codemirror
      ref="myCm"
      :value="editorValue"
      :options="cmOptions"
      @changes="onCmCodeChanges"
      @blur="onCmBlur"
      @keydown.native="onKeyDown"
      @mousedown.native="onMouseDown"
      @paste.native="OnPaste"
      v-if="isJson==='json' && isShowForm">
    </codemirror>
    <codemirror
      ref="myCm"
      :value="codeValue"
      :options="cmOptions"
      @changes="onCmCodeChanges"
      @blur="onCmBlur"
      @keydown.native="onKeyDown"
      @mousedown.native="onMouseDown"
      @paste.native="OnPaste"
      v-if="isJson==='json' && !isShowForm">
    </codemirror>
    <el-button v-if="false" @click="outmsg">输出code值</el-button>

    <el-input ref="myraw" v-if="isJson==='raw'" type="textarea" :autosize="{ minRows: 14, maxRows: 14}"
              v-model="editorValue" @input="sendValue"></el-input>
    <params-table v-if="isJson==='form' && isShowForm" v-model="codeValue" :is-show-del="true"></params-table>
  </div>
</template>


<script>
  import {codemirror} from "vue-codemirror";
  import "codemirror/theme/blackboard.css";
  import "codemirror/mode/javascript/javascript.js";
  import "codemirror/mode/xml/xml.js";
  import "codemirror/mode/htmlmixed/htmlmixed.js";
  import "codemirror/mode/css/css.js";
  import "codemirror/mode/yaml/yaml.js";
  import "codemirror/mode/sql/sql.js";
  import "codemirror/mode/python/python.js";
  import "codemirror/mode/markdown/markdown.js";
  import "codemirror/addon/hint/show-hint.css";
  import "codemirror/addon/hint/show-hint.js";
  import "codemirror/addon/hint/javascript-hint.js";
  import "codemirror/addon/hint/xml-hint.js";
  import "codemirror/addon/hint/css-hint.js";
  import "codemirror/addon/hint/html-hint.js";
  import "codemirror/addon/hint/sql-hint.js";
  import "codemirror/addon/hint/anyword-hint.js";
  import "codemirror/addon/lint/lint.css";
  import "codemirror/addon/lint/lint.js";
  import "codemirror/addon/lint/json-lint";
  import "codemirror/addon/lint/javascript-lint.js";
  import "codemirror/addon/fold/foldcode.js";
  import "codemirror/addon/fold/foldgutter.js";
  import "codemirror/addon/fold/foldgutter.css";
  import "codemirror/addon/fold/brace-fold.js";
  import "codemirror/addon/fold/xml-fold.js";
  import "codemirror/addon/fold/comment-fold.js";
  import "codemirror/addon/fold/markdown-fold.js";
  import "codemirror/addon/fold/indent-fold.js";
  import "codemirror/addon/edit/closebrackets.js";
  import "codemirror/addon/edit/closetag.js";
  import "codemirror/addon/edit/matchtags.js";
  import "codemirror/addon/edit/matchbrackets.js";
  import "codemirror/addon/selection/active-line.js";
  import "codemirror/addon/search/jump-to-line.js";
  import "codemirror/addon/dialog/dialog.js";
  import "codemirror/addon/dialog/dialog.css";
  import "codemirror/addon/search/searchcursor.js";
  import "codemirror/addon/search/search.js";
  import "codemirror/addon/display/autorefresh.js";
  import "codemirror/addon/selection/mark-selection.js";
  import "codemirror/addon/search/match-highlighter.js";
  import jsonlint from 'jsonlint'; //引入
  import ParamsTable from "./ParamsTable";
  import common from "../../common/js/common";

  window.jsonlint = jsonlint;  //全局化

  export default {
    components: {codemirror, ParamsTable},
    model: {
      prop: 'codeValue',//这个字段，是指父组件设置 v-model 时，将变量值传给子组件的 codeValue
      event: 'getValue'//这个字段，是指父组件监听 getValue 事件
    },
    props: {
      codeValue: [Array,String],
      isShowForm: Boolean
    },
    data() {
      return {
        isJson: this.isShowForm ? 'form' : 'json',
        formData: this.codeValue,
        editorValue: this.codeValue,
        cmTheme: "idea", // codeMirror主题
        // codeMirror主题选项
        cmThemeOptions: [
          "default",
          "3024-day",
          "3024-night",
          "abcdef",
          "ambiance",
          "ayu-dark",
          "ayu-mirage",
          "base16-dark",
          "base16-light",
          "bespin",
          "blackboard",
          "cobalt",
          "colorforth",
          "darcula",
          "dracula",
          "duotone-dark",
          "duotone-light",
          "eclipse",
          "elegant",
          "erlang-dark",
          "gruvbox-dark",
          "hopscotch",
          "icecoder",
          "idea",
          "isotope",
          "lesser-dark",
          "liquibyte",
          "lucario",
          "material",
          "material-darker",
          "material-palenight",
          "material-ocean",
          "mbo",
          "mdn-like",
          "midnight",
          "monokai",
          "moxer",
          "neat",
          "neo",
          "night",
          "nord",
          "oceanic-next",
          "panda-syntax",
          "paraiso-dark",
          "paraiso-light",
          "pastel-on-dark",
          "railscasts",
          "rubyblue",
          "seti",
          "shadowfox",
          "the-matrix",
          "tomorrow-night-bright",
          "tomorrow-night-eighties",
          "ttcn",
          "twilight",
          "vibrant-ink",
          "xq-dark",
          "xq-light",
          "yeti",
          "yonce",
          "zenburn"
        ],
        cmEditorMode: "json", // 编辑模式
        // 编辑模式选项
        cmEditorModeOptions: [
          "default",
          "json",
          "textile",
          "sql",
          "javascript",
          "css",
          "xml",
          "html",
          "yaml",
          "markdown",
          "python"
        ],
        cmMode: "application/json", //codeMirror模式
        jsonIndentation: 2, // json编辑模式下，json格式化缩进 支持字符或数字，最大不超过10，默认缩进2个空格
        autoFormatJson: true, // json编辑模式下，输入框失去焦点时是否自动格式化，true 开启， false 关闭
        cmOptions: {
          theme: !this.cmTheme || this.cmTheme == "default" ? "idea" : this.cmTheme,
          mode: !this.cmMode || this.cmMode == "default" ? "application/json" : this.cmMode,
          lineWrapping: true,
          lineNumbers: true,
          autofocus: true,
          smartIndent: false,
          autocorrect: true,
          spellcheck: true,
          extraKeys: {
            Tab: "autocomplete",
            "Ctrl-Alt-L": () => {
              try {
                if (this.cmOptions.mode == "application/json" && this.editorValue) {
                  this.editorValue = this.formatStrInJson(this.editorValue);
                }
              } catch (e) {
                this.$message.error(
                  "格式化代码出错：" + e.toString()
                );
              }
            }
          },
          lint: true,
          gutters: [
            "CodeMirror-lint-markers",
            "CodeMirror-linenumbers",
            "CodeMirror-foldgutter"
          ],
          foldGutter: true,
          autoCloseBrackets: true,
          autoCloseTags: true,
          matchTags: {bothTags: true},
          matchBrackets: true,
          styleActiveLine: true,
          autoRefresh: true,
          highlightSelectionMatches: {
            minChars: 2,
            style: "matchhighlight",
            showToken: true
          },
          styleSelectedText: true,
          enableAutoFormatJson: this.autoFormatJson == null ? true : this.autoFormatJson,
          defaultJsonIndentation: !this.jsonIndentation || typeof this.jsonIndentation != typeof 1 ? 2 : this.jsonIndentation
        },
        enableAutoFormatJson:
          this.autoFormatJson == null ? true : this.autoFormatJson,
        defaultJsonIndentation: !this.jsonIndentation || typeof this.jsonIndentation != typeof 1 ? 2 : this.jsonIndentation
      };
    },

    watch: {
      cmTheme: function (newValue, oldValue) {
        try {
          let theme = this.cmTheme == "default" ? "blackboard" : this.cmTheme;
          require("codemirror/theme/" + theme + ".css");
          this.cmOptions.theme = theme;
          this.resetLint();
        } catch (e) {
          this.$message.error("切换编辑器主题出错：" + e.toString());
        }
      },
      cmMode: function (newValue, oldValue) {
        this.$set(this.cmOptions, "mode", this.cmMode);
        this.resetLint();
        this.resetFoldGutter();
      },
      isJson: function (newValue, oldValue) {
        if (oldValue === 'form') {
          this.formToJson();
        }
        if (newValue === 'raw') {
          this.editorValue = this.formatRaw();
        } else if (newValue === 'json') {
          this.editorValue = this.formatStrInJson(this.editorValue);
        } else if (newValue === 'form') {
          this.toFormdata()
        }
      },
      formData: function (newValue, oldValue) {
        if (this.isShowForm) {
          this.sendValue();
        }
      },
      editorValue: function (newValue, oldValue) {
        if (!this.isShowForm) {
          this.sendValue();
        }
      }
    },

    methods: {
      // 切换编辑模式事件处理函数
      onEditorModeChange(value) {
        switch (value) {
          case "json":
            this.cmMode = "application/json";
            break;
          case "sql":
            this.cmMode = "sql";
            break;
          case "textile":
            this.cmMode = "Textile";
            break;
          case "javascript":
            this.cmMode = "javascript";
            break;
          case "xml":
            this.cmMode = "xml";
            break;
          case "css":
            this.cmMode = "css";
            break;
          case "html":
            this.cmMode = "htmlmixed";
            break;
          case "yaml":
            this.cmMode = "yaml";
            break;
          case "markdown":
            this.cmMode = "markdown";
            break;
          case "python":
            this.cmMode = "python";
            break;
          default:
            this.cmMode = "application/json";
        }

      },
      resetLint() {
        if (!this.$refs.myCm.codemirror.getValue()) {
          this.$nextTick(() => {
            this.$refs.myCm.codemirror.setOption("lint", false);
          });
          return;
        }

        this.$refs.myCm.codemirror.setOption("lint", false);
        this.$nextTick(() => {
          this.$refs.myCm.codemirror.setOption("lint", true);
        });
      },
      resetFoldGutter() {
        this.$refs.myCm.codemirror.setOption("foldGutter", false);
        this.$nextTick(() => {
          this.$refs.myCm.codemirror.setOption("foldGutter", true);
        });
      },
      // 获取值
      getValue() {
        try {
          return this.$refs.myCm.codemirror.getValue();
        } catch (e) {
          let errorInfo = e.toString();
          this.$message.error("获取编辑框内容失败：" + errorInfo);
          return errorInfo;
        }
      },
      formatRaw() {
        return this.editorValue.toString().replace(/\n|\s/g, '');
      },
      // 修改值
      setValue(value) {
        try {
          if (typeof value != typeof "") {
            this.$message.error(
              "修改编辑框内容失败：编辑内容只能为字符串"
            );
            return;
          }
          if (this.cmOptions.mode == "application/json") {
            this.editorValue = this.formatStrInJson(value);
          } else {
            this.editorValue = value;
          }
        } catch (e) {
          this.$message.error("修改编辑框内容失败：" + e.toString());
        }
      },
      // 黏贴事件处理函数
      OnPaste(event) {
        if (this.cmOptions.mode == "application/json") {
          try {
            this.editorValue = this.formatStrInJson(this.editorValue);
          } catch (e) {
            // 啥都不做
          }
        }
      },
      // 失去焦点时处理函数
      onCmBlur(cm, event) {
        try {
          let editorValue = cm.getValue();
          if (this.cmOptions.mode == "application/json" && editorValue) {
            if (!this.enableAutoFormatJson) {
              return;
            }
            this.editorValue = this.formatStrInJson(editorValue);
          }
        } catch (e) {
          // 啥也不做
        }
      },
      // 按下键盘事件处理函数
      onKeyDown(event) {
        const keyCode = event.keyCode || event.which || event.charCode;
        const keyCombination = event.ctrlKey || event.altKey || event.metaKey;
        if (!keyCombination && keyCode > 64 && keyCode < 123) {
          this.$refs.myCm.codemirror.showHint({completeSingle: false});
        }
      },
      // 按下鼠标时事件处理函数
      onMouseDown(event) {
        this.$refs.myCm.codemirror.closeHint();
      },
      onCmCodeChanges(cm, changes) {
        this.editorValue = cm.getValue();
        this.resetLint();
        if (!this.isShowForm) {
          this.$emit('getValue', this.editorValue);
        }
      },
      // 格式化字符串为json格式字符串
      formatStrInJson(strValue) {
        return JSON.stringify(JSON.parse(strValue), null, this.defaultJsonIndentation);
      },
      created() {
        try {
          if (!this.editorValue) {
            this.cmOptions.lint = false;
            return;
          }
          if (this.cmOptions.mode == "application/json") {
            if (!this.enableAutoFormatJson) {
              return;
            }
            this.editorValue = this.formatStrInJson(this.editorValue);
          }
        } catch (e) {
          console.log("初始化codemirror出错：" + e);
          // this.$message.error("初始化codemirror出错：" + e);
        }
      },
      sendValue() {
        if(this.isShowForm){
        this.$emit('getValue', this.formData)}
        else {
          this.$emit('getValue', this.editorValue)
        }
      },
      toFormdata() {
        let obj = JSON.parse(this.editorValue);
        for (let key in obj) {
          let index = 0;
          let type = 'text';
          switch (typeof obj[key]) {
            case "number":
              type = 'number';
              break;
            case "boolean" :
              type = 'checkbox';
              break;
            default:
              type = 'text';
          }
          for (index in this.formData) {
            if (key === this.formData[index].paramname) {
              this.formData[index].value = obj[key];
              this.formData[index].type = type;
              break;
            }
          }
          if (parseInt(index) === this.formData.length - 1) {

            console.log(typeof obj[key]);
            this.formData.splice(this.formData.length - 1, 0, {
              paramname: key,
              notnull: '',
              type: type,
              value: obj[key],
              memo: ''
            });
          }
        }
        return
      },
      formToJson() {
        let obj = {};
        for (let index = 0; index < this.codeValue.length - 1; index++) {
          obj[this.codeValue[index].paramname] = this.codeValue[index].value;
        }
        this.editorValue = JSON.stringify(obj);
      },
      outmsg() {
        console.log('editor', this.editorValue);
        console.log('code', this.codeValue)
        console.log('formdata', this.formData)
      },
    },
  };
</script>


<style scoped>

  .CodeMirror-selected {

    background-color: blue !important;

  }


  .CodeMirror-selectedtext {

    color: white !important;

  }


  .cm-matchhighlight {

    background-color: #ae00ae;

  }

  .CodeMirror {
    position: absolute;
    top: 80px;
    left: 2px;
    right: 5px;
    bottom: 0px;
    padding: 2px;
    height: auto;
    overflow-y: auto;
  }

  .code-mirror-div {
    width: 100%;
    line-height: 20px;
    size: 20px;
  }

</style>



