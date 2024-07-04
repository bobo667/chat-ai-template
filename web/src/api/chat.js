import axios from '@/libs/api.request';


// 获取聊天列表
export function queryChatList( params ) {
	return axios.request( {
		url: '/query-chat-list',
		method: 'get',
		params,
	} );
}

// 查询聊天记录
export function queryChatRecord( params ) {
	return axios.request( {
		url: `/query-chat-record/${params}`,
		method: 'get',
	} );
}
// 查询最后一个ai聊天记录
export function queryChatLastAiRecord( params ) {
	return axios.request( {
		url: `/query-chat-last-ai-record/${params}`,
		method: 'get',
	} );
}

// 查询聊天记录
export function deleteChat( params ) {
	return axios.request( {
		url: `/query-chat-record/${params}`,
		method: 'delete',
	} );
}

// 发送聊天
export function sendMessage( data ) {
	return axios.request( {
		// url: '/send-message',
		url: '/chunked',
		method: 'post',
		data,
		responseType: 'stream',
	} );
}
