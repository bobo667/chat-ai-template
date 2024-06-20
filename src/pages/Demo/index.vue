<template>
  <div class="">
    <el-container>
      <el-aside width="200px">
        <Menu/>
      </el-aside>
      <el-main style="width: 100%; padding: 50px 50px 0 50px">
        <contentIndex/>
      </el-main>
      <el-collapse-transition>
        <el-aside width="270px" v-if="settingShow">
          <Setting @close="settingChange"/>
        </el-aside>
      </el-collapse-transition>

    </el-container>
  </div>
</template>


<script>
import Setting from '@/components/setting/index.vue';
import { EventBus } from '@/util/eventBus';
import Menu from '../../components/menu/index';
import contentIndex from '../../components/content/index';

export default {
	name: '',
	props: [ '' ],
	data() {
		return {
			settingShow: false,
		};
	},
	components: {
		contentIndex,
		Menu,
		Setting,
	},
	created() {
		EventBus.$on( 'openSetting', this.settingChange );
	},
	destroyed() {
		EventBus.$off( 'openSetting', this.settingChange );
	},
	computed: {},
	mounted() {
	},
	methods: {
		settingChange() {
			this.settingShow = !this.settingShow;
		},
	},
	watch: {},
};
</script>
<style lang="scss">
@import "./index";
</style>
