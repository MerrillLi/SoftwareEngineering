<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="submit"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="序号" width="80">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column label="题目内容" width="500">
        <template slot-scope="scope">
          {{ scope.row.content }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" align="center" width="100">
        <template slot-scope="scope">
          <el-tag :type="scope.row.states | statusFilter">{{ scope.row.states }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time" width="400">
        <template slot-scope="scope">
          <i class="el-icon-time"/>
          <span>{{ scope.row.add_time }}</span>
        </template>
      </el-table-column>

    </el-table>
  </div>
</template>
<script>
  import {getList} from '@/api/table'
  import axios from 'axios'

  export default {
    filters: {
      statusFilter(status) {
        const statusMap = {
          已通过: 'success',
          待审核: 'gray',
          未通过: 'danger'
        }
        return statusMap[status]
      }
    },
    data() {
      return {
        list: null,
        listLoading: true,
        submit: []
      }
    },
    created() {
      this.requestSubmitProblemRecord()
    },
    methods: {
      // 获取出题信息
      requestSubmitProblemRecord(id = 0) {
        axios.post('/api/course/RequestProblem/', {
          data: {
            pk: id
          }

        }).then(res => {
          this.submit = res.data.data
          console.log(res)
          console.log(this.list)
          this.listLoading = false

        }).catch(error => {
          console.log(error)
        })
      },
    }
  }
</script>
