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
          <el-button @click="func" icon="el-icon-edit" type="primary">开始练习</el-button>
        </div>
      </div>
    </el-row>

    <div class="qa" v-if="!flag">
      <el-card>
        <el-card shadow="hover">
          {{current.描述}}
        </el-card>
        <el-card shadow="hover">
          <el-row>
            <el-col :span="12" :offset="6">
              <el-card>
                <el-radio-group v-model="choice">
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="A">{{current.选项A}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="B">{{current.选项B}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">
                      <span><el-radio label="C">{{current.选项C}}</el-radio></span>
                    </el-card>
                  </el-row>
                  <el-row>
                    <el-card shadow="hover">

                      <span><el-radio label="D">{{current.选项D}}</el-radio></span>
                    </el-card>
                  </el-row>
                </el-radio-group>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
        <el-card shadow="hover">
          <el-row>
            <el-col :span="5" offset="3">
              <el-button :disabled="!finished">
                查看解析
              </el-button>
            </el-col>
            <el-col :span="5" offset="3">
              <el-button @click="submit" :disabled="choice==null">
                提交
              </el-button>
            </el-col>
            <el-col :span="5" offset="3">
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
        current: {
          '选项A': '这是选项A',
          '选项B': '这是选项B',
          '选项C': '这是选项C',
          '选项D': '这是选项D',
          '描述': '这是题目的描述信息'
        }

      }
    },
    methods: {
      func() {
        this.flag = false
      },
      submit() {
        axios.post('', {}).then(res => {
          console.log(res)
        }).catch(err => {
          console.log(err)
        })
      },
      next() {
        axios.get('', {}).then(res => {
          console.log(res)

        }).catch(err => {
          console.log(err)

        })
      }

    }
  }
</script>

<style scoped>
  .select{
    text-align:center;
    position:relative;
    top:150%;
  }
  .button{
    text-align:center;
    position:relative;
    top:180%;
  }

  .pagination {
    padding: 10px 20px;
    text-align: right;
  }
</style>
