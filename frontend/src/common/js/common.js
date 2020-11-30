export default {


  //前端使用的全局变量
  baseUrl: 'http://192.168.156.124:8000/',      //后端地址及端口   //gitignore
  //API
  apilist: 'api/list/',
  queryapilist: 'api/queryapilist/',
  newapi: 'api/newapi/',
  editapi: 'api/updateapi/',
  deleteapi: 'api/delapi/',
  detailapi: '/apidetail/',
  createcase: 'api/createcase/',

  //APICASE
  apicaselist: 'api/caselist/',
  querycaselist: 'api/querycaselist/',
  newapicase: 'api/newcase/',
  editapicase: 'api/updatecase/',
  deleteapicase: 'api/delapicase/',
  detailapicase: '/casedetail/',
  runcase: 'api/runcase/',
  testruncase: 'api/testruncase/',
  //DICT
  columntypelist: 'api/columntypelist/',
  optiontypelist: 'api/optiontypelist/',
  optionlist: 'api/optionlist/',


  requestMethod: ['GET', 'POST', 'PUT'],         //请求方法
  status: [{'title': '开发中', 'value': 1},
    {'title': '测试中', 'value': 2},
    {'title': '已上线', 'value': 3},
  ],
  owner: [{'title': '楼文松', 'value': '楼文松'},
    {'title': '张志宇', 'value': '张志宇'},
    {'title': '菜菜', 'value': '菜菜'},
  ],

  //formtable相关数据
  valueType: [
    {'title': '字符串', 'value': 'string'},
    {'title': '数值', 'value': 'number'},
    {'title': '整数', 'value': 'int'},
    {'title': '布尔值', 'value': 'boolean'},
    {'title': '文件', 'value': 'file'},
    {'title': 'null', 'value': null},
  ],
  formDataNull: {
    paramname: '',
    notnull: '',
    type: 'string',
    condition: [],
    conditionValue: {},
    memo: ''
  },

  condioptions: {
    'text': [
      {
        'title': '字符长度',
        'value': [
          {'title': '大于等于', 'value': 'gt'},
          {'title': '小于等于', 'value': 'lt'},
          {'title': '介于', 'value': 'bt'},
          {'title': '等于', 'value': 'eq'},
        ]
      },
      {
        'title': '特殊字符',
        'value': 'special'
      },
      {
        'title': '正则',
        'value': 'regular'
      },
    ],
    'int': [
      {'title': '数值范围', 'value': 'length'},
      {'title': '负数', 'value': 'negative'},
      {'title': '是否为0', 'value': 'zero'},
    ],
    'checkbox': [],
    'file': [],
    null: []
  },
  cditDefault: {
    'text': {
      'length': {},
      'special': {
        'include': '',
        'notinclude': ''
      },
      'regular': '',
    },
  },
  //分页使用的变量
  currentpage: 1,   //当前页
  pagesize: 10,     //每页展示行数
  pagesizes: [10, 20, 50, 100],     //可选分页行数
  //判断最后一行是否为空
  need_del_null(list) {
    return list[list.length - 1].paramname === "";
  },

  formatDateTime(time) {
    let datetime = time;
    if (datetime) {
      datetime = new Date(datetime);
      let y = datetime.getFullYear() + '-';
      let mon = datetime.getMonth() + 1 + '-';
      let d = datetime.getDate() + ' ';
      let h = datetime.getHours() + ':';
      let m = datetime.getMinutes() + ':';
      let s = datetime.getSeconds();
      return y + mon + d + h + m + s;
    }

    return '---'
  },
}

