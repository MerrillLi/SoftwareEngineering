<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">

      <el-form-item label="所属科目">

        <el-select v-model="form.course_id" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="考试日期">
        <el-calendar v-model="date">
        </el-calendar>

      </el-form-item>

      <el-form-item label="考试时间">
        <el-time-picker
          v-model="start"
          :picker-options="{
      selectableRange: '18:30:00 - 20:30:00'
    }"
          placeholder="任意时间点">
        </el-time-picker>
        <el-time-picker
          arrow-control
          v-model="end"
          :picker-options="{
      selectableRange: '18:30:00 - 20:30:00'
    }"
          placeholder="任意时间点">
        </el-time-picker>

      </el-form-item>

      <el-form-item label="试卷名称">
        <el-input v-model="form.content"/>
      </el-form-item>


      <el-form-item label="出题人">
        <el-input v-model="form.person">
        </el-input>
      </el-form-item>

      <el-form-item label="备注">
        <el-input v-model="form.comment" type="textarea">
        </el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        options:
          [{
            value: '选项1',
            label: '人工智能'
          }, {
            value: '选项2',
            label: '操作系统'
          }, {
            value: '选项3',
            label: '计算机组织与体系结构'
          }, {
            value: '选项4',
            label: '电工电子'
          }, {
            value: '选项5',
            label: '计算方法'
          }],
        emptyForm:
          {
            course_id: '操作系统',
            content: '操作系统期末考试',
            person: '周老师',
            comment: '请不要使用计算器',
            note: '出错题啦',
          }
        ,
        form: undefined,
        start: new Date(),
        end: new Date(),
        date: new Date()
      }
    },
    created() {
      this.form = this.emptyForm
    },
    methods: {
      onSubmit() {
        axios.post('/api/course/submitproblem/', {
          data: this.form
        }).then(res => {
          console.log(res);
          this.$notify.success('提交成功');
          this.form = this.emptyForm
        }).catch(err => {
          console.log(err)
        })

      },
      onCancel() {
        this.$message({
          message: 'Reset!',
          type: 'warning'
        })
        this.form = this.emptyForm
      }
    }
  }
</script>

<style scoped>
  .line {
    text-align: center;
  }
</style>

