<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="活动名称">
      <el-input v-model="input" placeholder="请输入用户名"></el-input>
    </el-form-item>
  </el-form>
</template>

<script>
    export default {
      data() {
        return {
          input: ''
        }
      }
    }
</script>

<style scoped>

</style>
