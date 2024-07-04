<template>
  <div>
    <form
      class="flex w-full items-center rounded-b-md border-t border-slate-300 bg-slate-200 p-2 dark:border-slate-700 dark:bg-slate-900"
    >
      <div class="w-full max-w-12xl rounded-lg bg-slate-200 dark:bg-slate-900">
        <div
          class="rounded-lg rounded-b-none border border-slate-300 bg-slate-50 px-2 py-2 dark:border-slate-700 dark:bg-slate-800"
        >
          <label for="prompt-input" class="sr-only">Enter your prompt</label>
          <textarea
            id="prompt-input"
            v-model="formData.chat_content"
            rows="3"
            class="w-full border-0 bg-slate-50 px-0 text-base text-slate-900 focus:outline-none dark:bg-slate-800 dark:text-slate-200 dark:placeholder-slate-400"
            placeholder="Enter your prompt"
            required
          ></textarea>
        </div>
        <div class="flex items-center justify-between px-2 py-2">
          <el-button type="primary" :loading="sendLoading" @click="send"
                     class="mr-1 inline-flex text-white items-center gap-x-2 rounded-lg bg-blue-600 px-4 py-2.5 text-center text-sm font-medium text-slate-50 hover:bg-blue-800 focus:ring-4 focus:ring-blue-200 dark:focus:ring-blue-900 sm:text-base">
            send
          </el-button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { queryChatLastAiRecord } from '@/api/chat';

export default {
	name: 'PromentInput',
	data() {
		return {
			formData: {
				chat_content: '',
				chat_id: '',
				chat_type: '',
			},
			sendLoading: false,
			streamedContent: '',
		};
	},
	props: {
		chat_id: {
			type: String,
			default: '',
		},
		chat_type: {
			type: String,
			default: 'text',
		},
	},
	watch: {
		chat_id: {
			handler( val ) {
				this.formData.chat_id = val;
			},
			immediate: true,
		},
		chat_type: {
			handler( val ) {
				this.formData.chat_type = val;
			},
			immediate: true,
		},
	},
	methods: {
		send() {
			if ( !this.formData.chat_content ) {
				this.$message.warning( 'Please enter your prompt' );
				return;
			}
			const _this = this;
			this.$emit( 'send', this.formData.chat_content );
			this.sendLoading = true;
			const id = new Date().getTime();
			// 用来终止fetch请求
			window.controller = new AbortController();
			let chatStr = '';
			let chatId = '';

			fetch( '/api/send-message', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify( this.formData ),
			} )
				.then( ( response ) => {
					const reader = response.body.getReader();
					const decoder = new TextDecoder( 'utf-8' );

					function processStreamResult( result ) {
						const chunk = decoder.decode( result.value, { stream: !result.done } );
						if ( result.done ) {
							_this.sendLoading = false;
							_this.$emit( 'done', id );
							_this.formData.chat_content = '';
						}
						if ( chunk === '' ) {
							chatStr += '\n';
						}
						// 逐条解析后端返回数据
						const lines = chunk.split( '\n\n' );

						lines.forEach( ( line ) => {
							if ( line.trim().length > 0 ) {
								if ( line.match( /^data*/gi ) ) {
									const str = line.slice( 5 );
									if ( str === '' ) {
										chatStr += '\n';
									} else if ( str.indexOf( '#startId:' ) >= 0 ) {
										chatId = str.split( '#startId:' )[1];
										_this.$emit( 'chatChangeId', chatId );
									} else if ( str.indexOf( '#end:' ) >= 0 ) {
										queryChatLastAiRecord( chatId ).then( ( res ) => {
											_this.$emit( 'chatResp', res.data.chat_content, id );
										} );
									} else {
										chatStr += str;
									}
									_this.$emit( 'chatResp', chatStr, id );
									// 将结果赋值给你需要展示输出结果的地方
									console.log( chatStr );
								}

								// if ( line.match( /^meta*/gi ) ) {
								// 	// 此条消息输出结束，添加你的逻辑代码
								// }
							}
						} );
						if ( !result.done ) {
							return reader.read().then( processStreamResult );
						}
					}

					return reader.read().then( processStreamResult );
				} )
				.catch( ( error ) => {
					console.error( 'Error:', error );
				} );

			// 在需要中断fetch请求的地方调用
			window.controller.abort();
		},
		queryChatLastAiRecord( chatId ) {
			return queryChatLastAiRecord( chatId );
		},
	},
	mounted() {
		// Code to run when the component is mounted goes here
	},
};
</script>

<style scoped>
/* Your component's CSS styles go here */
</style>
