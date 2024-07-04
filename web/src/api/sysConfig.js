import axios from '@/libs/api.request';

// 保存配置
export function saveConfig( data ) {
	return axios.request( {
		url: '/sys-config/save-config',
		method: 'post',
		data,
	} );
}

// 查詢配置信息
export function querySysConfig( params ) {
	return axios.request( {
		url: `/sys-config/query-sys-config/${params}`,
		method: 'get',
	} );
}
