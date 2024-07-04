<template>
  <div>
    <el-dialog
      title="知识库"
      :visible.sync="dialogVisible"
      width="80%"
      :before-close="handleClose">
      <div>
        <div class="tableOp mb-2">
          <file-btn
            @uploadSuccess="restQuery"
            btnName="上传文件" />
        </div>
        <el-table
          :data="tableData"
          style="width: 100%">
          <el-table-column
            fixed
            prop="id"
            label="ID"
            width="200">
          </el-table-column>
          <el-table-column
            prop="file_name"
            label="文件名">
          </el-table-column>
          <el-table-column
            prop="file_path"
            label="保存路径">
          </el-table-column>
          <el-table-column
            prop="city"
            label="文档块数量"
            width="100">
            <template slot-scope="scope">
              <el-tag >{{ JSON.parse(scope.row.vector_ids).length}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="120">
            <template slot-scope="scope">
              <el-popconfirm
                title="确认要删除吗？"
                @confirm="deleteRow( scope.row)"
              >
                <el-button
                  type="text"
                  slot="reference"
                  size="small">
                  删除
                </el-button>
              </el-popconfirm>

            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-pagination
        background
        style="float: right"
        layout="prev, pager, next"
        :page-size="searchData.size"
        :current-page="searchData.page"
        @current-change="changePage"
        :total="count">
      </el-pagination>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { EventBus } from '@/util/eventBus';
import { queryKnowledgePage, delFile } from '@/api/knowledge';
import FileBtn from '@/components/fileUpload/fileBtn.vue';

export default {
	components: { FileBtn },
	data() {
		return {
			searchData: {
				page: 1,
				size: 10,
			},
			count: 0,
			tableData: [],
			dialogVisible: false,
		};
	},
	created() {
		EventBus.$on( 'openKnowledgeBase', this.open );
	},
	destroyed() {
		EventBus.$off( 'openKnowledgeBase', this.open );
	},
	methods: {
		open() {
			this.dialogVisible = true;
			this.queryKnowledgePage();
		},
		deleteRow( row ) {
			delFile( row.id ).then( ( res ) => {
				this.$message.success( '删除成功' );
				this.queryKnowledgePage();
			} );
		},
		restQuery() {
			this.searchData.page = 1;
			this.queryKnowledgePage();
		},
		changePage( page ) {
			this.searchData.page = page;
			this.queryKnowledgePage();
		},
		queryKnowledgePage() {
			queryKnowledgePage( this.searchData ).then( ( res ) => {
				this.total = res.data.total;
				this.tableData = res.data.rows;
				console.log( res.data, '666' );
			} );
		},
		handleClose( done ) {
			this.$confirm( '确认关闭？' )
				.then( ( _ ) => {
					done();
				} )
				.catch( ( _ ) => {
				} );
		},
	},
};
</script>
<style scoped>

</style>
