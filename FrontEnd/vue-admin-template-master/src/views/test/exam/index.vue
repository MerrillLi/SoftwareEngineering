<template>
  <div class="contain">
    <el-row type="flex" class="row-bg" justify="center">
      <div class="selector" v-if="flag">
        <div class="select">
          <el-select v-model="value" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
        <div class="button">
          <el-button @click="start" icon="el-icon-edit" type="primary">开始考试</el-button>
        </div>
      </div>
    </el-row>

    <div class="qa" v-if="!flag">
      <el-card>
        <el-card shadow="hover">
          {{current.content}}
        </el-card>
        <el-card shadow="hover">
          <el-row>
            <el-col :span="12" :offset="6">
              <el-card>
                <el-radio-group v-model="choice">
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="A">{{current.choice_a}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="B">{{current.choice_b}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="C">{{current.choice_c}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="D">{{current.choice_d}}</el-radio></span>
                    </el-card>
                  </el-row>
                </el-radio-group>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
        <el-card shadow="hover">
          <el-row>
            <el-col :span="5" :offset="3">
              <el-button :disabled="!finished">
                查看解析
              </el-button>
            </el-col>
            <el-col :span="5" :offset="3">
              <el-button @click="submit" :disabled="choice==null">
                提交
              </el-button>
            </el-col>
            <el-col :span="5" :offset="3">
              <el-button @click="next">
                下一题
              </el-button>
            </el-col>
          </el-row>
        </el-card>
      </el-card>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        options: [{
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
        value: '',
        flag: true,
        choice: null,
        finished: false,
        turnID: undefined,
        score: 3,
        record: [{}],
        current: {}

      }
    },
    methods: {
      // 开始联系
      start() {
        this.flag = false
        axios.post('/api/course/startExercise/').then(res => {
          console.log(res);
          this.turnID = res.data.turnID;
          this.next();
        }).catch(err => {
          console.log(err)
        })
      },

      // 提交题目
      submit() {
        axios.post('/api/course/submitAnswer/', {
          data: {
            answer: this.choice,
            proID: this.current.id,
            turnID: this.turnID
          }
        }).then(res => {
          console.log(res);
          if (res.data.state == 'true') {
            this.$notify.success('回答正确!')
          } else {
            this.$notify.error('正确答案是' + res.data.answer)
          }

          //this.current = res.data.data;

        }).catch(err => {
          console.log(err)

        })
      },

      //获取下一道题
      next() {
        //参数
        // history : 答题历史
        // score   : 用户评分
        axios.post('/api/course/requestNext/', {
          data: {
            record: this.record,
            score: this.score
          }
        }).then(res => {
          console.log(res);
          this.current = res.data.data;
          this.finished = false
          this.choice = null

        }).catch(err => {
          console.log(err)

        })
      }

    }
  }
</script>

<style scoped>
  .select {
    text-align: center;
    position: relative;
    top: 150%;
  }

  .button {
    text-align: center;
    position: relative;
    top: 180%;
  }

  .pagination {
    padding: 10px 20px;
    text-align: right;
  }
</style>
