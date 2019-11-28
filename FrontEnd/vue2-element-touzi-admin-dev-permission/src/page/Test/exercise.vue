<template>
    <div class="contain">
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
                <el-button @click="func" type="primary" icon="el-icon-edit" circle>开始练习</el-button>
            </div>
        </div>
    </div>
</template>

<script>
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
                flag: true
            }
        },
        methods: {
            func() {
                this.flag = false
            }
        }
    }
</script>

<style lang="less" scoped>
    .selector {
        width: 500px;
        height: 500px;
        margin: 100px;
    }

    .button {
        /*height:100px;*/
        position: relative;
        top: 130px;
        left: 300px;

    }

    .select {
        /*height:100px;*/
        position: relative;
        top: 100px;
        left: 280px;
    }

    .el-button--mini, .el-button--mini.is-round {
        width: 150px;
        height: 150px;
    }

    .el-input--mini .el-input__inner {
        height: 40px;
        width: 150px;
        line-height: 28px;
    }

    .pagination {
        padding: 10px 20px;
        text-align: right;
    }
</style>



