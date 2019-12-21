<template>
  <div class="fillcontain">
    <!--个人信息栏-->
    <div class="info_container">
      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.name" :disabled="modify">
          <template slot="prepend">姓名</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.str_identity" :disabled="modify">
          <template slot="prepend">身份</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.user_id" :disabled="modify">
          <template slot="prepend">学号</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.institution" :disabled="modify">
          <template slot="prepend">院系</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.major" :disabled="modify">
          <template slot="prepend">专业</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <el-input placeholder="请输入内容" v-model="user.email" :disabled="modify">
          <template slot="prepend">邮件</template>
        </el-input>
      </el-row>

      <el-row :gutter="20">
        <div>
          <el-col :span="4" :offset="6">
            <el-button @click="modify = !modify">修改</el-button>
          </el-col>
          <el-col :span="4" :offset="6">
            <el-button @click="submit_profile">提交</el-button>
          </el-col>
        </div>
      </el-row>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import {checkExpire} from "../../utils/auth";

  export default {
    name: 'Profile',
    computed: {
      ...mapGetters([
        'name'
      ])
    },
    data() {
      return {
        user: null,
        modify: true
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
            identity: localStorage.getItem('role')
          }
        }).then(res => {
          console.log(res);
          this.user = res.data;
          this.user.str_identity = this.user.identity === 'student' ? '学生' : '老师';
          this.$store.userInfo = res.data;
          console.log(res.data)
        }).catch(error => {
          console.log(error)
        })
      },
      submit_profile() {
        axios.post('/api/user/update_profile/', {
          data: this.user
        }).then(res => {
          checkExpire(res);
          this.user = res.data;
          this.$store.userInfo = res.data;
        }).catch(error => {
          console.log(error)
        })
      }
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

  .info_container {
    padding: 10%;
  }
</style>
