<template>
  <div class="contents">
    <!-- Prompt Messages Container - Modify the height according to your need -->
    <div class="flex overflow-y-auto w-full flex-col half-screen-height" ref="chatContentDiv">
      <!-- Prompt Messages -->
      <div
        class="flex-1 space-y-6  rounded-xl bg-slate-200 p-4 text-sm leading-6 text-slate-900 shadow-sm dark:bg-slate-900 dark:text-slate-300 sm:text-base sm:leading-7"
      >
        <div
          :class="
            'flex ' + (item.role === 'user' ? 'flex-row-reverse' : '') + ' items-start'
          "
          v-for="item in messageList"
        >
          <img class="mr-2 h-8 w-8 rounded-full" :src="imgInfo[item.role]"/>
          <div
            class="flex rounded-b-xl rounded-tr-xl bg-slate-50 p-4 dark:bg-slate-800 sm:max-w-md md:max-w-2xl markdown-body"
          >
            <p class="text-sm ">
<!--              <span v-if="!item.keyName">{{item.content}}</span>-->
              <vue-markdown :key="item.keyName" v-highlight :source="item.content"></vue-markdown>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Prompt message input -->
    <promptInput @done="chatRespDone" :chat_type="chat_type"  @chatChangeId="chatChangeId" :chat_id="chat_id" @send="send" @chatResp="chatResp"/>
  </div>
</template>

<script>
import { EventBus } from '@/util/eventBus';
import { queryChatRecord } from '@/api/chat';
import VueMarkdown from 'vue-markdown';
import promptInput from '../proment-input/index.vue';


// 你可以选择其他样式
export default {
	components: { promptInput, VueMarkdown },
	name: 'Index',
	data() {
		return {
			imgInfo: {
				user: require( '@/assets/userAvatar.png' ),
				assistant: require( '@/assets/aiAvatar.png' ),
			},
			formData: {},
			messageList: [],
			chat_id: '',
			chat_type: 'text',
		};
	},
	created() {
		EventBus.$on( 'changeChat', this.changeChat );
		EventBus.$on( 'createChat', this.createChat );
	},
	destroyed() {
		EventBus.$off( 'changeChat', this.changeChat );
		EventBus.$off( 'createChat', this.createChat );
	},
	watch: {
		chat_id( newVal ) {
			if ( newVal ) {
				this.queryChatRecord();
			}
		},
	},
	methods: {
		createChat( chatData ) {
			this.chat_type = chatData.chat_type;
			this.messageList = [];
			this.chat_id = '';
		},
		changeChat( chatInfo ) {
			this.chat_id = chatInfo.id;
			this.chat_type = chatInfo.chart_type;
		},
		queryChatRecord() {
			queryChatRecord( this.chat_id ).then( ( res ) => {
				res.data.forEach( ( item ) => {
					item.keyName = Math.random();
				} );
				this.messageList = res.data;
				this.scrollToBottom();
			} );
		},
		send( content ) {
			this.messageList.push( {
				content,
				role: 'user',
			} );
			this.scrollToBottom();
		},
		chatChangeId( chatId ) {
			console.log( chatId, 'chatChangeId' );
			if ( this.chat_id != chatId ) {
				this.chat_id = chatId;
				EventBus.$emit( 'changeChatList' );
			}
		},
		chatRespDone( id ) {
		},
		chatResp( text, id ) {
			if ( this.messageList.filter( item => item.id === id ).length === 0 ) {
				this.messageList.push( {
					id,
					content: text,
					role: 'assistant',
				} );
				return;
			}
			this.messageList.forEach( ( item ) => {
				if ( item.id === id ) {
					item.content = text;
				}
			} );
			this.scrollToBottom();
		},
		scrollToBottom() {
			console.log( '666' );
			this.$nextTick( () => {
				const { chatContentDiv } = this.$refs;
				chatContentDiv.scrollTo( { // 滚动动画
					top: chatContentDiv.scrollHeight,
					behavior: 'smooth',
				} );
			} );
		},


		// Your component methods go here
	},
	mounted() {
		// Code to run when the component is mounted goes here
	},
};

</script>
<style scoped lang="scss">

.half-screen-height {
  height: 65vh;
}

</style>
