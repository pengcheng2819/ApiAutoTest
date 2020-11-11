import Vue from 'vue'
import ApiList from "../components/api/ApiList";
import Apiform from "../components/api/Apiform";
import VueRouter from "vue-router";
import HelloWorld from "../components/common/HelloWorld";
import Api from "../components/api/Api";
import ApiCase from "../components/api/ApiCase";
import ApiCaseList from "../components/api/ApiCaseList";
import ApiCaseForm from "../components/api/ApiCaseForm";

Vue.use(VueRouter);

//解决当前路由重复报错问题
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
};

const routes = [
  {path: '/home', name: 'home', component: HelloWorld, meta: {title: '首页'}},
  {
    path: '/api', name: "apimanage", component: Api, meta: {title: '接口管理'}, redirect: '/api/apilist',
    children: [
      {path: '/api/apilist', name: "apilist", component: ApiList, meta: {title: '接口列表'}, ismenu: true},
      {path: '/api/newapi', name: "newapi", component: Apiform, meta: {title: '新增接口'}, ismenu: true},
      {path: '/api/editapi', name: "editapi", component: Apiform, meta: {title: '编辑接口'}},
      {path: '/api/detailapi', name: "detailapi", component: Apiform, meta: {title: '接口详情'}},
    ]
  },
  {
    path: '/apicase', name: "apicasemanage", component: ApiCase, meta: {title: '用例管理'}, redirect: '/apicase/caselist',
    children: [
      {path: '/apicase/caselist', name: "caselist", component: ApiCaseList, meta: {title: '用例列表'}, ismenu: true},
      {path: '/apicase/newcase', name: "newcase", component: ApiCaseForm, meta: {title: '新增用例'}, ismenu: true},
      {path: '/apicase/editcase', name: "editcase", component: ApiCaseForm, meta: {title: '编辑接口'}},
      {path: '/apicase/detailcase', name: "detailcase", component: ApiCaseForm, meta: {title: '接口详情'}},
    ]
  },
];


const router = new VueRouter({
  routes: routes,
  mode: 'history',
});

router.afterEach((to, from) => {
  let bodySrcollTop = document.body.scrollTop;
  if (bodySrcollTop !== 0) {
    document.body.scrollTop = 0;
    return
  }
  let docSrcollTop = document.documentElement.scrollTop;
  if (docSrcollTop !== 0) {
    document.documentElement.scrollTop = 0
  }
});

export default router;


