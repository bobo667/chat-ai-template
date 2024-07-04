<template>
  <el-upload
    ref="fileUpload"
    :action="action"
    :limit="1"
    :on-success="uploadSuccess"
    :on-error="uploadError"
    :file-list="fileList">
    <el-button size="small" type="primary">{{ btnName }}</el-button>
  </el-upload>
</template>
<script>
export default {
	data() {
		return {
			fileList: [],
		};
	},
	props: {
		action: {
			type: String,
			default: '/api/knowledge/save-file',
		},
		btnName: {
			type: String,
			default: '上传文件',
		},
	},
	methods: {
		uploadSuccess( response, file, fileList ) {
			this.$emit( 'uploadSuccess', response );
			this.$refs.fileUpload.clearFiles();
		},
		uploadError( err, file, fileList ) {
			this.$message.error( '上传失败' );
			this.$emit( 'uploadError', err );
		},
	},
};
</script>
<style scoped>

</style>
