<template>
    <el-container>
        <el-container>
        <el-aside width="600px">
            <el-card style="height: 460px;">
                <quill-editor v-model="content" ref="myQuillEditor" style="height: 500px;" :options="editorOption">
                    <!-- 自定义toolar -->
                    <div id="toolbar" slot="toolbar">
                        <!-- Add a bold button -->
                        <button class="ql-bold" title="加粗">Bold</button>
                        <button class="ql-italic" title="斜体">Italic</button>
                        <button class="ql-underline" title="下划线">underline</button>
                        <button class="ql-strike" title="删除线">strike</button>
                        <button class="ql-blockquote" title="引用"></button>
                        <button class="ql-code-block" title="代码"></button>
                        <button class="ql-header" value="1" title="标题1"></button>
                        <button class="ql-header" value="2" title="标题2"></button>
                        <!--Add list -->
                        <button class="ql-list" value="ordered" title="有序列表"></button>
                        <button class="ql-list" value="bullet" title="无序列表"></button>
                    </div>
                </quill-editor>
            </el-card>
        </el-aside>


        <el-container>
            <el-main>
                <div style="margin: 40px;"></div>
                <el-form :label-position="labelPosition" label-width="80px" :model="formLabelAlign">
                    <el-form-item label="题目类型">
                        <el-select v-model="formLabelAlign.region" placeholder="请选择题目类型">
                            <el-option label="智能系统" value="zhineng"></el-option>
                            <el-option label="软件工程" value="ruanjian"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic">
                        <el-form-item
                                v-for="(domain, index) in dynamicValidateForm.domains"
                                :label="'选项' + index"
                                :key="domain.key"
                                :prop="'domains.' + index + '.value'"
                                :rules="{
                                            required: true, message: '选项不能为空', trigger: 'blur'
                                        }"
                        >
                            <el-input v-model="domain.value"></el-input><el-button @click.prevent="removeDomain(domain)">删除</el-button>
                        </el-form-item>
                        <el-form-item>

                            <el-button @click="addDomain">新增选项</el-button>
                            <el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
                        </el-form-item>
                    </el-form>

                    <el-form-item label="答案">
                        <el-input v-model="formLabelAlign.region"></el-input>
                    </el-form-item>
                </el-form>
            </el-main>
        </el-container>


        </el-container>
        <el-footer>
            <el-row :gutter="20">
                <el-col :span="2" :offset="20"><el-button>取消</el-button></el-col>
                <el-col :span="2" :offset="0"><el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button></el-col>
            </el-row>
        </el-footer>
    </el-container>
</template>

<script>
    import {
        Quill,
        quillEditor
    } from 'vue-quill-editor'
    import 'quill/dist/quill.core.css'
    import 'quill/dist/quill.snow.css'
    import 'quill/dist/quill.bubble.css'

    let Size = Quill.import('attributors/style/size')
    Size.whitelist = ['10px', '12px', '14px', '16px', '18px', '20px']
    Quill.register(Size, true)

    // 自定义字体类型
    var fonts = ['SimSun', 'SimHei', 'Microsoft-YaHei', 'KaiTi', 'FangSong', 'Arial', 'Times-New-Roman', 'sans-serif',
        '宋体', '黑体'
    ]
    var Font = Quill.import('formats/font')
    Font.whitelist = fonts
    Quill.register(Font, true)

    export default {
        name: 'FuncFormsEdit',
        components: {
            quillEditor
        },
        data() {
            return {
                dynamicValidateForm: {
                    domains: [{
                        value: ''
                    }],
                    email: ''
                },
                labelPosition: 'right',
                formLabelAlign: {
                    name: '',
                    region: '',
                    type: '',
                    region:''
                },

                content: null,
                editorOption: {
                    placeholder: "请输入",
                    theme: "snow", // or 'bubble'
                    modules: {
                        toolbar: {
                            container: '#toolbar'
                        }
                    }
                }

            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            removeDomain(item) {
                var index = this.dynamicValidateForm.domains.indexOf(item)
                if (index !== -1) {
                    this.dynamicValidateForm.domains.splice(index, 1)
                }
            },
            addDomain() {
                this.dynamicValidateForm.domains.push({
                    value: '',
                    key: Date.now()
                });
            }
        }
    }
</script>

<style lang="less" scoped>
    .el-aside {
        background-color: white;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .el-main {
        background-color: white;
        color: #333;
        text-align: center;
        line-height: 160px;
    }
    .el-header, .el-footer {
        background-color: white;
        color: #333;
        text-align: center;
        line-height: 60px;
    }
    body > .el-container {
        margin-bottom: 40px;
    }

    .el-container:nth-child(5) .el-aside,
    .el-container:nth-child(6) .el-aside {
        line-height: 260px;
    }

    .el-container:nth-child(7) .el-aside {
        line-height: 320px;
    }


    .el-row {
        margin-bottom: 20px;
        &:last-child {
            margin-bottom: 0;
        }
    }
    .el-col {
        border-radius: 4px;
    }
    /*.bg-purple-dark {*/
        /*background: #99a9bf;*/
    /*}*/
    /*.bg-purple {*/
        /*background: #d3dce6;*/
    /*}*/
    /*.bg-purple-light {*/
        /*background: #e5e9f2;*/
    /*}*/
    /*.grid-content {*/
        /*border-radius: 4px;*/
        /*min-height: 36px;*/
    /*}*/
    /*.row-bg {*/
        /*padding: 10px 0;*/
        /*background-color: #f9fafc;*/
    /*}*/

</style>


