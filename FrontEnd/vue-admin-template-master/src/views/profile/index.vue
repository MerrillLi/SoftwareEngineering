<template>
  <div class="fillcontain">
    <!--个人信息栏-->
    <div class="info_container">
      <el-row :gutter="20">
        <el-col :span="6">姓名：
        </el-col>
        <el-col :span="6">
          <el-input
            placeholder="请输入内容"
            prefix-icon="el-icon-search"
            v-model="user.name">
          </el-input>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6">身份：
        </el-col>
        <el-col :span="6">
          <el-input
            placeholder="请输入内容"
            prefix-icon="el-icon-search"
            v-model="user.identity">
          </el-input>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6">学号：
        </el-col>
        <el-col :span="6">
          <el-input
            placeholder="请输入内容"
            prefix-icon="el-icon-search"
            v-model="user.user_id">
          </el-input>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6">院系：
        </el-col>
        <el-col :span="6">
          <el-input
            placeholder="请输入内容"
            prefix-icon="el-icon-search"
            v-model="user.institution">
          </el-input>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'

  export default {
    name: 'Profile',
    computed: {
      ...mapGetters([
        'name'
      ])
    },
    data() {
      return {
        user: null

      }
    },
    mounted() {
      this.getUserInfo();
    },
    methods: {
      // 获取用户信息
      getUserInfo() {
        axios.post('/api/user/get_profile/', {
          data: {
            identity: 1
          }
        }).then(res => {
          console.log(res)
          this.user = res.data;
          this.$store.userInfo = res.data;
          console.log(res.data)
        }).catch(error => {
          console.log(error)
        })
      },


    }
  }
</script>

<style lang="scss" scoped>
  .dashboard {
    &-container {
      margin: 30px;
    }

    &-text {
      font-size: 30px;
      line-height: 46px;
    }
  }
</style>
