// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from "axios";
import './common/css/common.css'
import './common/js/tools'


//Json查看插件
import JsonViewer from 'vue-json-viewer'
import 'vue-json-viewer/style.css'
// 引入jshint用于实现js自动补全提示

// 引入代码编辑器
import {codemirror} from "vue-codemirror";
import "codemirror/lib/codemirror.css";

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.prototype.$axios = Axios;
Vue.use(JsonViewer);
Vue.use(codemirror);


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
});


