// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'normalize.css/normalize.css'
import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.config.productionTip = false;
Vue.prototype.$axios = Axios;

Vue.use(ElementUI);

new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
});