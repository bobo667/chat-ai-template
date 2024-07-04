import Vue from 'vue';
import ElementUI from 'element-ui';
import hljs from 'highlight.js';
import App from './App.vue';
import router from './router/index';
import store from './store/index';
import i18n from './language/i18n';
import 'element-ui/lib/theme-chalk/index.css';
import moment from 'moment';
import './styles/tailwindcss.css';
import './styles/github-markdown.css';
import {
	dateFormat,
} from './libs/util.js';

// require styles
import './styles/common.scss';
import './styles/element-variables.scss';

Vue.use( ElementUI );

Vue.config.productionTip = false;
Vue.prototype.$moment = moment;


// 如果开启了typescript 需要额外安装 npm install @types/highlight.js
// 通过 import * as hljs from 'highlight.js' 引入
Vue.directive( 'highlight', ( el ) => {
	const blocks = el.querySelectorAll( 'pre code' );
	blocks.forEach( ( block ) => {
		hljs.highlightBlock( block );
	} );
} );
// 也可以把这自定义指令封装 通过Vue.use()，来注入


Vue.filter( 'dateFormat', dateFormat );

new Vue( {
	router,
	store,
	i18n,
	render: h => h( App ),
} ).$mount( '#app' );
