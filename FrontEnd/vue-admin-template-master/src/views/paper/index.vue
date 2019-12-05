<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">

      <el-form-item label="所属科目">
        <el-select v-model="form.course_id" placeholder="请选择" @change="updateList">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="考试日期">
        <el-date-picker
          v-model="form.date"
          type="date"
          placeholder="选择日期">
        </el-date-picker>

      </el-form-item>

      <el-form-item label="考试时间">
        <el-time-picker
          v-model="form.start"
          :picker-options="{
      selectableRange: '18:30:00 - 20:30:00'
    }"
          placeholder="任意时间点">
        </el-time-picker>
        <el-time-picker
          arrow-control
          v-model="form.end"
          :picker-options="{
      selectableRange: '18:30:00 - 20:30:00'
    }"
          placeholder="任意时间点">
        </el-time-picker>

      </el-form-item>

      <el-form-item label="试卷名称">
        <el-input v-model="form.content"/>
      </el-form-item>

      <el-form-item label="考试场地">
        <el-input v-model="form.place"/>
      </el-form-item>

      <el-form-item label="考试题目">
        <el-transfer v-model="selected" :data="qset" :titles="['备选试题','已选试题']"></el-transfer>
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
        options: undefined,
        emptyForm:
          {
            course_id: '',
            content: '操作系统期末考试',
            person: '周老师',
            comment: '请不要使用计算器',
            note: '出错题啦',
            place: 'E402',
            start: new Date(),
            end: new Date(),
            date: new Date(),
            CourseID: null
          }
        ,
        form: undefined,
        teachList: undefined,
        selected: [],
        qset: undefined,
      }
    },
    created() {
      this.form = this.emptyForm;
      this.getTeachCourse()
    },
    methods: {
      getTeachCourse() {
        axios.post('/api/course/getTeachCourse/', {
          data: {}
        })
          .then(res => {
            this.teachList = res.data.data;
            this.options = []
            for (let i = 0; i < this.teachList.length; i++) {
              const obj = this.teachList[i]
              this.options.push({
                value: obj.id,
                label: obj.name
              })
            }
          }).catch(err => {
          console.log(err)
        })
      },
      onSubmit() {
        console.log(this.form.start.toISOString());
        console.log(this.selected)

        axios.post('/api/course/creatPaper/', {
          data: {
            proID: this.selected,
            place: this.form.place,
            start: this.form.start.toISOString(),
            end: this.form.end.toISOString(),
            date: this.form.date.toISOString(),
            note: "",
            CourseID: this.form.course_id
          }
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
        });
        this.form = this.emptyForm
      },
      updateList() {
        axios.post('/api/course/getOneCoursePro/', {
          data: {
            courseID: this.form.course_id
          }
        }).then(res => {
          this.qset = []
          var retval = res.data.data
          for (let i = 0; i < retval.length; i++) {
            const obj = retval[i]
            this.qset.push({
              key: obj.id,
              label: obj.content
            })
          }

        }).catch(err => {
        })
      }
    }
  }
</script>

<style scoped>
  .line {
    text-align: center;
  }
</style>

