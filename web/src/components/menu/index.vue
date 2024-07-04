<template>
  <div>
    <!-- Sidebar -->
    <aside class="flex menu">
      <div
        class="flex h-[100svh] w-60 flex-col overflow-y-auto bg-slate-50 pt-8 dark:border-slate-700 dark:bg-slate-900 sm:h-[100vh] sm:w-64"
      >
        <div class="flex px-4">
          <!-- Logo -->
          <logo-icon/>
          <h2 class="px-3 text-lg font-medium text-slate-800 dark:text-slate-200">
            ChatAi
            <span class="mx-2 rounded-full bg-blue-600 px-2 py-1 text-xs text-slate-200"
            >{{ chatList.length }}</span
            >
          </h2>
        </div>
        <div class="mx-2 mt-8">
          <el-popover
            placement="right"
            trigger="click">
            <el-radio-group v-model="chatData.chat_type">
              <el-radio label="text">聊天</el-radio>
              <el-radio label="rag">Rag</el-radio>
            </el-radio-group>
            <div class="mt-3" style="text-align: right">
              <el-button type="primary" size="mini" @click="addChat">确定</el-button>
            </div>
            <button
              slot="reference"
              class="flex w-full gap-x-4 rounded-lg border border-slate-300 p-4 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              <add-icon/>
              New Chat
            </button>
          </el-popover>

        </div>
        <!-- Previous chats container -->
        <div
          class="h-2/3 space-y-4 overflow-y-auto border-b border-slate-300 px-2 py-4 dark:border-slate-700"
        >
          <button
            v-for="item in chatList"
            style="background-color: #f8f8f8;"
            @click="changeChat(item)"
            class="flex w-full flex-col gap-y-2 rounded-lg px-3 py-2 text-left transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:hover:bg-slate-800"
          >
            <h1 class="text-sm font-medium capitalize text-slate-700 dark:text-slate-200">
              {{ item.chat_name }}
            </h1>
            <p class="text-xs text-slate-500 dark:text-slate-400"> {{ item.create_time }}</p>
          </button>
        </div>
        <div class="mt-3 w-full space-y-4 px-2 py-4">
          <button
            @click="openKnowledgeBase"
            class="flex w-full gap-x-2 rounded-lg px-3 py-2 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <user-logo/>
            知识库
          </button>
          <button
            @click="openSetting"
            class="flex w-full gap-x-2 rounded-lg px-3 py-2 text-left text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-200 focus:outline-none dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <setting-icon/>
            配置
          </button>
        </div>
      </div>
    </aside>
  </div>
</template>

<script>
import UserLogo from '@/components/icon/user-icon.vue';
import SettingIcon from '@/components/icon/setting-icon.vue';
import AddIcon from '@/components/icon/add-icon.vue';
import LogoIcon from '@/components/icon/logo-icon.vue';
import { EventBus } from '@/util/eventBus';
import { queryChatList } from '@/api/chat';

export default {
	name: 'Menu',
	components: {
		LogoIcon, AddIcon, UserLogo, SettingIcon,
	},
	data() {
		return {
			chatList: [],
			chatData: {
				chat_type: 'text',
			},
			// Your data properties here
		};
	},
	created() {
		EventBus.$on( 'changeChatList', this.queryChatList );
	},
	destroyed() {
		EventBus.$off( 'changeChatList', this.queryChatList );
	},
	methods: {
		addChat() {
			EventBus.$emit( 'createChat', this.chatData );
		},
		openSetting() {
			EventBus.$emit( 'openSetting' );
		},
		openKnowledgeBase() {
			console.log( '6666' );
			EventBus.$emit( 'openKnowledgeBase' );
		},
		queryChatList() {
			queryChatList().then( ( res ) => {
				this.chatList = res.data;
				if ( res.data && res.data.length == 0 ) {
					EventBus.$emit( 'createChat', this.chatData );
				} else {
					EventBus.$emit( 'changeChat', res.data[0] );
				}
			} );
		},
		changeChat( item ) {
			EventBus.$emit( 'changeChat', item );
		},
		// Your methods here
	},
	mounted() {
		this.queryChatList();
	},

};
</script>

<style scoped>
/* Your CSS styles here */
.menu {
  height: 100vh;
}
</style>
