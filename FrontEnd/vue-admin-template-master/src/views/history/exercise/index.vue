<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="exercise"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID">
        <template slot-scope="scope">
          {{ scope.$index + 1}}
        </template>
      </el-table-column>
      <el-table-column label="答题者">
        <template slot-scope="scope">
          {{ scope.row.student_id }}
        </template>
      </el-table-column>
      <el-table-column label="答题编号" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time">
        <template slot-scope="scope">
          <i class="el-icon-time"/>
          <span>{{ scope.row.e_time }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
  import {getList} from '@/api/table'
  import axios from 'axios'
  import {checkExpire} from "../../../utils/auth";

  export default {
    filters: {

    },
    data() {
      return {
        list: null,
        listLoading: true,
        exercise: []
      }
    },
    created() {
      this.requestExerciseRecord()
    },
    methods: {
      // 获取练习记录
      requestExerciseRecord(id = 0) {

        axios.post('/api/course/requestExerciseRecord/', {
          data: {
            identity: 1,
            pk: id
          }
        }).then(res => {
          checkExpire(res);
          this.exercise = res.data.data;
          this.listLoading = false;
          console.log(res)
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
