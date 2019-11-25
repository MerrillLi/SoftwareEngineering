<template>
    <div>
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
        <div>
            <div class="contain">
                <el-carousel>
                    <el-carousel-item>
                        <div class="table_container1">
                            <el-table
                                    v-loading="loading"
                                    :data="tableData"
                                    border
                                    stripe
                                    highlight-current-row
                                    header-cell-class-name="table-header-class"
                                    style="width:100%">
                                <el-table-column label="练习记录" header-align="center" align="center">
                                    <el-table-column
                                            label="序号"
                                            width="60"
                                            align='center'>
                                        <template slot-scope="scope">
                                            <span>{{scope.$index+(paginations.pageIndex - 1) * paginations.pageSize + 1}} </span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                            property="username"
                                            label="提交时间"
                                            width="80"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="email"
                                            label="练习科目"
                                            width="180"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="address"
                                            label="练习结果"
                                            align='center'>
                                    </el-table-column>
                                </el-table-column>
                            </el-table>
                            <el-row>
                                <el-col :span="24">
                                    <div class="pagination">
                                        <el-pagination
                                                v-if='paginations.total > 0'
                                                :page-size="paginations.pageSize"
                                                :layout="paginations.layout"
                                                :total="paginations.total"
                                                :current-page='paginations.pageIndex'
                                                @current-change='handleCurrentChange'
                                                @size-change='handleSizeChange'>
                                        </el-pagination>
                                    </div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-carousel-item>
                    <el-carousel-item>
                        <div class="table_container2">
                            <el-table
                                    v-loading="loading"
                                    :data="tableData"
                                    border
                                    stripe
                                    highlight-current-row
                                    header-cell-class-name="table-header-class"
                                    style="width:100%">
                                <el-table-column label="考试记录" header-align="center" align="center">
                                    <el-table-column
                                            label="序号"
                                            width="60"
                                            align='center'>
                                        <template slot-scope="scope">
                                            <span>{{scope.$index+(paginations.pageIndex - 1) * paginations.pageSize + 1}} </span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                            property="username"
                                            label="提交时间"
                                            width="80"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="email"
                                            label="练习科目"
                                            width="180"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="address"
                                            label="考试结果"
                                            align='center'>
                                    </el-table-column>
                                </el-table-column>
                            </el-table>
                            <el-row>
                                <el-col :span="24">
                                    <div class="pagination">
                                        <el-pagination
                                                v-if='paginations.total > 0'
                                                :page-size="paginations.pageSize"
                                                :layout="paginations.layout"
                                                :total="paginations.total"
                                                :current-page='paginations.pageIndex'
                                                @current-change='handleCurrentChange'
                                                @size-change='handleSizeChange'>
                                        </el-pagination>
                                    </div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-carousel-item>
                    <el-carousel-item>
                        <div class="table_container3">
                            <el-table
                                    v-loading="loading"
                                    :data="tableData"
                                    border
                                    stripe
                                    highlight-current-row
                                    header-cell-class-name="table-header-class"
                                    style="width:100%">
                                <el-table-column label="出题记录" header-align="center" align="center">
                                    <el-table-column
                                            label="序号"
                                            width="60"
                                            align='center'>
                                        <template slot-scope="scope">
                                            <span>{{scope.$index+(paginations.pageIndex - 1) * paginations.pageSize + 1}} </span>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                            property="username"
                                            label="提交时间"
                                            width="80"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="email"
                                            label="试题简介"
                                            width="180"
                                            align='center'>
                                    </el-table-column>
                                    <el-table-column
                                            property="address"
                                            label="是否通过审核"
                                            align='center'>
                                    </el-table-column>
                                </el-table-column>
                            </el-table>
                            <el-row>
                                <el-col :span="24">
                                    <div class="pagination">
                                        <el-pagination
                                                v-if='paginations.total > 0'
                                                :page-size="paginations.pageSize"
                                                :layout="paginations.layout"
                                                :total="paginations.total"
                                                :current-page='paginations.pageIndex'
                                                @current-change='handleCurrentChange'
                                                @size-change='handleSizeChange'>
                                        </el-pagination>
                                    </div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-carousel-item>
                </el-carousel>
            </div>
        </div>
    </div>
</template>

<script>
    import {getUserList} from "@/api/user";
    import axios from 'axios'
    import auth from '@/utils/auth'

    export default {
        data() {
            return {
                tableData: [],
                loading: true,
                //需要给分页组件传的信息
                paginations: {
                    total: 0,        // 总数
                    pageIndex: 1,  // 当前位于哪页
                    pageSize: 5,   // 1页显示多少条
                    layout: "total, sizes, prev, pager, next, jumper"   // 翻页属性
                },
                user: {
                    "姓名": "Meryl",
                    "学号": 2017124033,
                    "用户身份": "学生",
                    "学院": "工学院"
                },
                exercise: {},
                submit: {},
                exam: {}

            }
        },
        created() {
        },
        mounted() {
            this.getUserList();
        },
        methods: {
            getUserList() {
                let para = {
                    limit: this.paginations.pageSize,
                    page: this.paginations.pageIndex
                }
                getUserList(para).then(res => {
                    this.loading = false;
                    this.paginations.total = res.data.total;
                    this.tableData = res.data.userList;
                })
            },
            // 每页多少条切换
            handleSizeChange(pageSize) {
                this.paginations.pageSize = pageSize;
                this.getUserList();
            },
            // 上下分页
            handleCurrentChange(page) {
                this.paginations.pageIndex = page;
                this.getUserList();
            },
            // 获取用户信息
            getUserInfo() {
                axios.get('http://localhost:8000/userinfo', {
                    data: {
                        sessionid: this.$store.token
                    }
                }).then(res => {
                    this.data.user = res.data
                    this.$store.userInfo = res.data
                    console.log(res.data)
                }).catch(error => {
                    console.log(error)
                })
            },
            // 获取出题信息
            requestSubmitProblemRecord() {
                axios.get('https://localhost:8000/api/v1/sumbitrecord', {
                    params: {
                        userid: this.user.学号,
                        sessionid: this.$store.token
                    }

                }).then(res => {
                    this.submit = res.data
                }).catch(error => {
                    console.log(error)
                })
            },

            // 获取练习记录
            requestExerciseRecord() {
                axios.get('https://localhost:8000/api/v1/exerciserecord', {
                    params: {
                        userid: this.user.学号,
                        sessionid: this.$store.token
                    }
                }).then(res => {
                    this.exercise = res.data
                }).catch(error => {
                    console.log(error)
                })
            }


        },
    }
</script>

<style lang="less" scoped>
    .info_container {
        width: 25%;
        float: left;
        padding: 10px;
        background: #fff;
        overflow: auto;
    }

    .row {
        margin: 20px;
    }

    .info_row {
        .area {
            width: 200px;
            border: 1px solid #dfdfdf;
            height: auto;
            overflow: hidden;

            .namearea {
                padding: 10px;
                margin-bottom: 20px;
                font-size: 14px;

                p {
                    line-height: 60px;
                }

                .awards {
                    text-align: center;
                    width: 100%;
                    height: 30px;
                    line-height: 30px;
                    cursor: pointer;
                    background-color: #3bc5ff;
                    border: 1px solid #3bc5ff;
                    color: white;
                    display: block;
                }

                .awards:hover {
                    background-color: #f9c855;
                    border: 1px solid #f9c855;
                }
            }

            .moneyarea {
                padding: 10px;
                float: left;

                .title {
                    font-size: 15px;
                    font-weight: bolder;
                    line-height: 50px;

                    .money {
                        color: #c10000;
                        margin-right: 5px;
                    }

                    .yuan {
                        font-weight: 100;
                        font-size: 13px;
                    }
                }

            }

            .dataarea {
                padding: 10px;
                text-align: center;
                font-size: 14px;

                .gtitle {
                    width: 100%;
                    height: 30px;
                    line-height: 30px;
                    cursor: pointer;
                    background-color: #3bc5ff;
                    color: white;
                    display: block;
                }

                .gdataarea {
                    padding-left: 25px;

                    p {
                        line-height: 38px;
                    }

                    .num {
                        font-weight: bolder;
                        color: #c10000;
                    }

                    .title {
                        color: #3bc5ff;
                    }

                    .gdata {
                        margin: 10px;
                    }
                }

                .morearea {
                    a {
                        color: #3bc5ff;
                    }
                }
            }
        }
    }

    .data_row {
        font-size: 18px;

        .area {
            border: 1px solid #dfdfdf;
            height: 200px;
            overflow: hidden;
            padding: 10px;
            text-align: center;
            font-weight: bolder;

            .symbol {
                font-size: 16px;
                font-style: italic;
                font-family: "microsoft yahei";
                margin-right: 10px;
                color: #232323;
                font-weight: 100;
            }

            p {
                line-height: 70px;
            }

            .num {
                color: #c10000;
            }

            .detail {
                margin-top: 5px;
                font-size: 14px;
                text-align: center;
                width: 100%;
                height: 30px;
                line-height: 30px;
                cursor: pointer;
                color: white;
                display: block;
                border: 1px solid #3bc5ff;
            }

            .dbgcolor {
                background-color: #3bc5ff;
            }

            .zbgcolor {
                color: #3bc5ff;
            }

            .dbgcolor:hover {
                background-color: #fff;
                color: #3bc5ff
            }

            .zbgcolor:hover {
                background-color: #3bc5ff;
                color: #fff;
            }
        }
    }

    .ban_row {
        .banarea {
            width: 100%;
            display: flex;
            justify-content: space-between;

            li {
                a {
                    background: url(../../assets/img/pro_map.gif?v=1.0) no-repeat;
                    width: 200px;
                    height: 50px;
                    display: block;
                }
            }
        }
    }
</style>
<style lang="less" scoped>
    .fillcontain {
        padding-bottom: 0;
    }

    .table_container1 {
        padding-bottom: 40px;
    }

    .table_container2 {
        padding-bottom: 40px;
    }

    .table_container3 {
        padding-bottom: 40px;
    }

    .contain {
        width: 70%;
        float: right;
        background: #fff;
        padding: 10px;
    }

    .pagination {
        padding: 10px 20px;
        text-align: right;
    }
</style>


