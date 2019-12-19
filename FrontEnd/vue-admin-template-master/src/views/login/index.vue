<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on"
             label-position="left">

      <div class="title-container">
        <h3 class="title">CAT自适应考试系统</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user"/>
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password"/>
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
                 @click.native.prevent="handleLogin">登陆
      </el-button>

      <el-button type="primary" style="width:100%;margin-bottom:30px;"
                 @click="dialogFormVisible = true">注册
      </el-button>

      <el-dialog title="注册" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="用户名:" :label-width="formLabelWidth">
            <el-input v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码:" :label-width="formLabelWidth">
            <el-input v-model="form.password" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item label="邮箱:" :label-width="formLabelWidth">
            <el-input v-model="form.email" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户身份" :label-width="formLabelWidth">
            <el-radio v-model="form.identity" label="student">学生</el-radio>
            <el-radio v-model="form.identity" label="teacher">教师</el-radio>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleSignIn">确 定</el-button>
        </div>
      </el-dialog>

    </el-form>


  </div>

</template>

<script>
  import {validUsername} from '@/utils/validate'
  import axios from 'axios'
  import {setToken} from "../../utils/auth";
  import Vue from 'vue'
  import router from '@/router'
  import permission from '@/store/permission'

  export default {
    name: 'Login',
    data() {
      const validateUsername = (rule, value, callback) => {
        if (!validUsername(value)) {
          callback(new Error('Please enter the correct user name'))
        } else {
          callback()
        }
      };
      const validatePassword = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error('The password can not be less than 6 digits'))
        } else {
          callback()
        }
      };
      return {
        loginForm: {
          username: '',
          password: ''
        },
        loginRules: {
          username: [{required: true, trigger: 'blur', validator: validateUsername}],
          password: [{required: true, trigger: 'blur', validator: validatePassword}]
        },
        form: {
          username: '',
          password: '',
          email: '',
          identity: ''
        },
        dialogTableVisible: false,
        dialogFormVisible: false,
        loading: false,
        passwordType: 'password',
        redirect: '/profile',
        formLabelWidth: '80px',
        radio: '1',
        identity_: '0'
      }

    },
    watch: {
      $route: {
        handler: function (route) {
          this.redirect = route.query && route.query.redirect
        },
        immediate: true
      }
    },
    methods: {
      showPwd() {
        if (this.passwordType === 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
        this.$nextTick(() => {
          this.$refs.password.focus()
        })
      },
      handleLogin() {
        this.$refs.loginForm.validate(valid => {
          if (valid) {
            this.loading = true;

            axios.post('/api/user/login/', {
              data: {
                username: this.loginForm.username,
                password: this.loginForm.password,
              }
            }).then(res => {
              console.log(res.data);
              setToken(res.data.sessionid);
              localStorage.setItem('role', res.data.identity)

              if ("true" === res.data.msg) {
                this.$router.push({path: '/profile'});
                this.loading = false
              } else {
                this.$notify.error('密码错误');
                this.loading = false
              }

            }).catch(err => {
              this.loading = false;
              console.log(err)
            })

          } else {
            console.log('error submit!!');
            return false
          }
        })
      },
      handleSignIn() {
        console.log(this.form);
        axios.post('/api/user/register/', {
          data: {
            username: this.form.username,
            password: this.form.password,
            email: this.form.email,
            identity: this.form.identity
          }
        }).then(res => {
          console.log(res.data);
          if (res.data.msg === "f_ualready") {
            this.$notify.error('用户已经存在');
          } else if (res.data.msg === 'S_toemail') {
            this.$notify.success('请查阅邮箱注册链接');
          } else if (res.data.msg === 'f_ealready') {
            this.$notify.error('邮箱已经被注册');
          } else if (res.data.msg === 'f_send') {
            this.$notify.error('注册邮件发送失败');
          }
          this.dialogFormVisible = false

        }).catch(err => {
          console.log(err)
          this.$notify.error("注册服务器失败")
        })
      }
    }
  }
</script>

<style lang="scss">

  $bg: #283443;
  $light_gray: #fff;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
      color: $cursor;
    }
  }

  /* reset element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;

      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;

        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }

    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>

<style lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;

  .login-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;
    overflow: hidden;

    .login-form {
      position: relative;
      width: 520px;
      max-width: 100%;
      padding: 160px 35px 0;
      margin: 0 auto;
      overflow: hidden;
    }

    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;

      span {
        &:first-of-type {
          margin-right: 16px;
        }
      }
    }

    .svg-container {
      padding: 6px 5px 6px 15px;
      color: $dark_gray;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
    }

    .title-container {
      position: relative;

      .title {
        font-size: 26px;
        color: $light_gray;
        margin: 0px auto 40px auto;
        text-align: center;
        font-weight: bold;
      }
    }

    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: $dark_gray;
      cursor: pointer;
      user-select: none;
    }
  }
</style>
