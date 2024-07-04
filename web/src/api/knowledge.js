import axios from '@/libs/api.request';


// 获取文件列表
export function queryKnowledgePage( params ) {
	return axios.request( {
		url: '/knowledge/query-knowledge-page',
		method: 'get',
		params,
	} );
}

// 查询聊天记录
export function delFile( params ) {
	return axios.request( {
		url: `/knowledge/del-file/${params}`,
		method: 'delete',
	} );
}
