<script>
import {httpGet, httpPost} from "@/plugins/axios";
import {router} from "@/plugins/router";
import Cookies from 'js-cookie'
import {ElMessage} from "element-plus";

export default {
    name: "login",
    data() {
        return {
            login_input_style: {
                'margin': '40px 10% 4px',
                'width': '80%'
            },
            login_info: {
                account: '',
                password: '',
                type: 'student'
            }
        }
    },
    methods: {
        async login() {
            let login = false
            await httpGet.get('/token')

            await httpPost.post('/login', {type: this.login_info.type, account: this.login_info.account, password: this.login_info.password})
                .then(() => {
                    login = true;
                })
                .catch(err => {
                    console.log(err)
                    ElMessage.error(err.response.data)
                })

            if (login) {
                Cookies.set('type', this.login_info.type)
                Cookies.set('account', this.login_info.account)
                Cookies.set('password', this.login_info.password)
                await router.push({name: this.login_info.type})
            }
        }
    }
}
</script>

<template>
    <div class="login">
        <div class="login_text">
            <el-text size="large" tag="b">欢迎来到机房管理系统</el-text>
        </div>
        <div class="login_input">
            <el-radio-group v-model="login_info.type" mode="horizontal" style="margin-left: 110px; margin-top: 20px">
                <el-radio label="student">学生</el-radio>
                <el-radio label="administrator">管理员</el-radio>
            </el-radio-group>
            <el-input placeholder="请输入账号" :style="login_input_style" v-model="login_info.account"></el-input>
            <el-input placeholder="请输入密码" type="password" show-password :style="login_input_style"
                      v-model="login_info.password"></el-input>
        </div>
        <div class="login_button">
            <el-button type="primary" round @click="login">{{ login_info.type === 'student' ? '登录/快速注册' : '登录' }}</el-button>
        </div>
    </div>
</template>

<style scoped>
.login {
    border: 1px #CDD0D6 solid;
    border-radius: 50px;
    height: 400px;
    width: 360px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    box-shadow: black 10px 5px 5px;
}

.login_text {
    text-align: center;
    margin-top: 60px;
    user-select: none;
}

.login_input {
    align-items: center;
}

.login_button {
    text-align: center;
    margin-top: 40px;
}
</style>