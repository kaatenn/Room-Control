<script>
import {httpDelete, httpGet, httpPost} from "@/plugins/axios";
import Cookies from "js-cookie";
import {ElMessage} from "element-plus";
import {router} from "@/plugins/router";

export default {
  name: 'administer',
  data() {
    return {
      menu_index: '1',
      form: {},
      rooms_info: [],
      loading: false,
      edit_self: false,
      computers: []
    }
  },
  mounted() {
    this.get_administer_info()
  },
  methods: {
    get_administer_info() {
      this.loading = true
      httpGet.get('/administrator_info?account=' + Cookies.get('account'))
          .then(res => {
            this.form = res.data.info
            this.rooms_info = res.data.rooms
          })
      this.loading = false
    },
    async edit_name() {
      if (!this.edit_self) {
        this.edit_self = true
      } else {
        await httpGet.get('token')

        await httpPost.post('/administrator_update_info', {id: Cookies.get('account'), name: this.form.name})
            .then(res => {
              ElMessage.success(res.data)
              this.edit_self = false
            })
            .catch(() => {
              ElMessage.error('保存失败！')
            })

        await this.get_user_info()
      }
    },
    async sign_off() {
      Cookies.remove('type')
      Cookies.remove('account')
      Cookies.remove('password')
      await router.push({name: 'login'})
    },
    async add_computer(index) {
      this.loading = true
      await httpGet.get('/token')
      await httpPost.post('/add_computer', {room_id: this.rooms_info[index].room_id})
          .then(res => {
            ElMessage.success(res.data)
          })
          .catch(() => {
            ElMessage.error('添加失败！')
          })
      await this.get_administer_info()
      this.loading = false
    },
    async delete_computer(index) {
      this.loading = true
      await httpGet.get('/token')
      let params = new URLSearchParams(this.rooms_info[index].room_id)
      params.append('room_id', this.rooms_info[index].room_id)
      await httpDelete.delete('/delete_computer', {data: params})
          .then(res => {
            ElMessage.success(res.data)
          })
          .catch(() => {
            ElMessage.error('删除失败！')
          })
      await this.get_administer_info()
      this.loading = false
    }
  }
}
</script>

<template>
  <el-row>
    <el-col :span="4">
      <el-menu default-active="1" @select="index => this.menu_index = index">
        <el-menu-item index="1">
          机房管理
        </el-menu-item>
        <el-menu-item index="2">
          个人中心
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="1"/>
    <el-col :span="19">
      <div v-if="menu_index === '1'">
        <div>
          <el-table :data="rooms_info" stripe width="100%" v-loading="loading">
            <el-table-column prop="room_id" label="房间编号"></el-table-column>
            <el-table-column prop="com_count" label="机位数"></el-table-column>
            <el-table-column prop="room_amount" label="今日收入"></el-table-column>
            <el-table-column label="更改机位">
              <template #default="scope">
                <el-button type="primary" @click="add_computer(scope.$index)">添加</el-button>
                <el-button type="danger" @click="delete_computer(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div v-if="menu_index === '2'">
        <el-form :model="form" label-width="120px" style="margin-top: 20px">
          <el-form-item label="昵称">
            <el-input v-model="form.name" :disabled="!edit_self" style="width: 320px"></el-input>
          </el-form-item>
          <el-form-item label="今日收费">
            ￥{{ form.ad_amount }}
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="edit_name">{{ !edit_self ? '修改' : '保存' }}</el-button>
            <el-button type="danger" @click="sign_off">注销</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>