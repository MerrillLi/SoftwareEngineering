<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="题目内容">
        <el-input v-model="form.desc" type="textarea" />
      </el-form-item>
      <el-form-item label="选项A">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="选项B">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="选项C">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="选项D">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="题目类型">
        <el-select v-model="form.region" placeholder="please select">
          <el-option label="Radio" value="Radio" />
          <el-option label="multiple choice" value="multiple choice" />
        </el-select>
      </el-form-item>
      <el-form-item label="答案">
        <el-input v-model="form.desc" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

