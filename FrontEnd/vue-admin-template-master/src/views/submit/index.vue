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
      <el-form-item label="题目内容">
        <el-input v-model="form.content" type="textarea"/>
      </el-form-item>
      <el-form-item label="选项A">
        <el-input v-model="form.choice_a"/>
      </el-form-item>
      <el-form-item label="选项B">
        <el-input v-model="form.choice_b"/>
      </el-form-item>
      <el-form-item label="选项C">
        <el-input v-model="form.choice_c"/>
      </el-form-item>
      <el-form-item label="选项D">
        <el-input v-model="form.choice_d"/>
      </el-form-item>
      <el-form-item label="正确答案">
        <el-select v-model="form.answer" placeholder="请选择">
          <el-option
            v-for="item in choices"
            :key="item.value"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="题目解析">
        <el-input v-model="form.note" type="textarea"/>
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
  import {checkExpire} from "../../utils/auth";

  export default {
    data() {
      return {
        choices: [{
          value: 'A',
          label: 'A'
        }, {
          value: 'B',
          label: 'B'
        }, {
          value: 'C',
          label: 'C'
        }, {
          value: 'D',
          label: 'D'
        }]
        ,
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
            content: '页表是什么',
            choice_a: '鬼知道',
            choice_b: '不懂',
            choice_c: '你随便',
            choice_d: '就是页表',
            answer: 'A',
            note: '出错题啦',
          }
        ,
        form: undefined
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
          checkExpire(res);
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

