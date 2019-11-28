<template>
  <div class="fillcontain">
    <!--个人信息栏-->
    <div class="info_container">
      <el-row class="info_row" :gutter="10">

        <el-col :span="5">
          <div class="area">
            <div class="namearea">
              <p>姓名：{{user.姓名}}</p>
              <p>学号：{{user.学号}}</p>
              <p>身份：{{user.用户身份}}</p>
              <p>院系：{{user.学院}}</p>
              <p class="awards"><i class="el-icon-date el-icon--left"></i>编辑个人信息</p>
            </div>
          </div>
        </el-col>

      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  data() {
    return {
      tableData: [],
      loading: true,
      user: undefined,
      exercise: {},
      submit: {},
      exam: {}
    }
  },
  created() {
  },
  // mounted() {
  //   this.getUserInfo();
  // },
  // methods:{
  //   // 获取用户信息
  //   getUserInfo() {
  //     axios.post('/api/user/get_profile/', {
  //       data: {
  //         //sessionid: "bb02k87gr4989xxwpm0jzykifmeq5dxr",
  //         sessionid: this.$store.token,
  //         identity: 1
  //       }
  //     }).then(res => {
  //       this.user = res.data;
  //       this.$store.userInfo = res.data;
  //       console.log(res.data)
  //     }).catch(error => {
  //       console.log(error)
  //     })
  //   }
  // }
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
