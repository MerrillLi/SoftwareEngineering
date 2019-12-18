<template>
  <div class="app-container">
    <el-table
      ref="filterTable"
      v-loading="listLoading"
      :data="submit"
      element-loading-text="Loading"
      @filter-change="filterChange"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>

      <el-table-column label="题目内容" width="250">
        <template slot-scope="scope">
          {{ scope.row.content }}
        </template>
      </el-table-column>

      <el-table-column label="题目选项" width="250">
        <template slot-scope="scope">
          A.{{ scope.row.choice_a }}<br>
          B.{{ scope.row.choice_b }}<br>
          C.{{ scope.row.choice_c }}<br>
          D.{{ scope.row.choice_d }}
        </template>
      </el-table-column>

      <el-table-column label="答案" width="50">
        <template slot-scope="scope">
          {{ scope.row.answer }}
        </template>
      </el-table-column>

      <el-table-column class-name="status-col" label="状态" width="110" align="center"
                       :filters="[{ text: '已通过', value: '审核通过' },
                       { text: '未通过', value: '未通过' },{text:'待审核',value:'待审核'}]"
                       :filter-method="columnFilter"
                       filter-placement="bottom-end"
                       prop='states'>
        <template slot-scope="scope">
          <el-tag :type="scope.row.states | statusFilter">{{ scope.row.states }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column align="center" prop="created_at" label="提交时间" width="125">
        <template slot-scope="scope">
          <i class="el-icon-time"/>
          <span>{{ scope.row.add_time }}</span>
        </template>
      </el-table-column>

      <el-table-column label="审核操作">
        <template slot-scope="scope">
          <el-row>
            <el-button type="success" icon="el-icon-check" circle @click="accept(scope.row.id)"></el-button>
            <el-button type="danger" icon="el-icon-delete" circle @click="reject(scope.row.id)"></el-button>
          </el-row>
        </template>
      </el-table-column>

    </el-table>
  </div>
</template>
<script>
  import axios from 'axios'


  export default {
    filters: {
      statusFilter(status) {
        const statusMap = {
          '审核通过': 'success',
          '待审核': 'gray',
          '未通过': 'danger'
        };
        if (status.length >= 5) {
          return statusMap['未通过']
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
      accept(qid) {
        axios.post('/api/course/judgeItem/', {
          data: {
            q_id: qid,
            flag: '审核通过'
          }

        }).then(res => {
          console.log(res);
          const submitList = this.submit;
          for (let i = 0; i < submitList.length; i++) {
            if (submitList[i].id === qid) {
              submitList[i].states = '审核通过'
            }
          }
          if (res.data.msg === true) {
            this.$notify.success('提交成功!')
          }

        }).catch(error => {
          console.log(error)
        })
      },
      async reject(qid) {
        const reason = await this.getRejectReason();
        console.log(reason);
        axios.post('/api/course/judgeItem/', {
          data: {
            q_id: qid,
            flag: '审核未通过' + '/' + reason
          }
        }).then(res => {
          console.log(res);
          const submitList = this.submit;
          if (res.data.msg === true) {
            this.$notify.success('提交成功!');
            for (let i = 0; i < submitList.length; i++) {
              if (submitList[i].id === qid) {
                submitList[i].states = '审核未通过' + '/' + reason
              }
            }

          }

        }).catch(error => {
          console.log(error)
        })
      },
      // 获取出题信息
      requestSubmitProblemRecord(id = 0) {
        axios.post('/api/course/RequestProblem/', {
          data: {
            pk: id
          }

        }).then(res => {
          this.submit = res.data.data;
          console.log(res);
          console.log(this.list);
          this.listLoading = false

        }).catch(error => {
          console.log(error)
        })
      },
      getRejectReason() {
        return new Promise((resolve, reject) => {
          this.$prompt('请输入不通过原因', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
          }).then(({value}) => {
            resolve(value)
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '取消输入'
            });
          });
        })
      },
      columnFilter(value, row) {
        if (row.states.length >= 5) {
          return row.states.substring(0, 5) === '审核未通过'
        }
        return row.states === value
      },
      filterChange(filterObj) {
        console.log(filterObj)
      }

    }
  }
</script>
