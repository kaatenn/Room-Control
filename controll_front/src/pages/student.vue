<script>
import {ref} from "vue";
import {httpGet, httpPost} from "@/plugins/axios";
import {ElMessage} from "element-plus";
import Cookies from "js-cookie";
import {router} from "@/plugins/router";

export default {
  name: 'student',
  data() {
    return {
      loading: false,
      menu_index: "1",
      allowed_start_time: (new Date().getHours() + 1) + ":00",
      select_time: ref(''),
      select_date: ref(''),
      breadcrumb: [{path: '/'}],
      editable_tabs: ref([{}]),
      activate_room: null,
      rooms: [],
      computers: [],
      disabled_date_rule: function (time) {
        return time.getTime() < Date.now() - 24 * 3600 * 1000 || time.getTime() > Date.now() + 24 * 3600 * 1000 * 2
      },
      form: {name: '', money: 0},
      edit_self: false,
      ordered: []
    }
  },
  watch: {
    async select_date(to) {
      const year = new Date().getFullYear()
      const date = new Date().getDate()
      const month = new Date().getMonth()
      const today = year + '-' + (month / 10 < 1 ? '0' : '') + (month + 1) + '-' + (date / 10 < 1 ? '0' : '') + date
      if (today === to) {
        this.allowed_start_time = new Date().getHours() < 8 ? "8:00" : (new Date().getHours() + 1) + ":00"
      } else {
        this.allowed_start_time = "8:00"
      }
      if (this.activate_room) {
        this.loading = true
        await this.get_computers_list(this.activate_room, to, this.select_time)
      }
    },
    async select_time(to) {
      if (this.activate_room) {
        this.loading = true
        await this.get_computers_list(this.activate_room, this.select_date, to)
      }
    }
  },
  mounted() {
    this.get_user_info()
  },
  methods: {
    async get_user_info() {
      this.loading = true
      httpPost.get('/get_user_info?id=' + Cookies.get('account'),)
          .then(res => {
            this.form.name = res.data.info.name
            this.form.money = res.data.info.money
            this.ordered = res.data.ordered
          })
          .catch(() => {
            this.loading = false
          })
      this.loading = false
    },
    async get_rooms_info() {
      if (this.select_date && this.select_time) {
        this.loading = true
        await httpGet('/student_room_info?date=' + this.select_date + '&time=' + this.select_time)
            .then(res => {
              this.rooms = res.data
            })
            .catch(() => {
              this.loading = false
            })
      } else {
        ElMessage.error('请选择日期和时间')
      }
      this.loading = false
    },
    async handle_table_row_click(row) {
      this.loading = true
      this.activate_room = row.id
      await this.get_computers_list(this.activate_room, this.select_date, this.select_time)
    },
    get_order_param(index, type_id) {
      return {
        record_id: Date.now().toString(),
        date: this.select_date,
        time: this.select_time,
        com_id: this.computers[index].id,
        student_id: Cookies.get('account'),
        type_id: type_id
      }
    },
    async order_computer(index) {
      if (this.form.money < 12) {
        ElMessage.error('余额不足！')
        return
      }
      this.loading = true
      await httpGet.get('/token')

      let param = this.get_order_param(index, 1)

      await httpPost.post('/order_computer', param)
          .then(res => {
            ElMessage.success(res.data)
          })
          .catch(() => {
            ElMessage.error('预约失败，请稍后重试！')
          })

      await this.get_computers_list(this.activate_room, this.select_date, this.select_time)
      await this.get_user_info()
      this.loading = false
    },
    async order_computer_for_class(index) {
      this.loading = true
      await httpGet.get('/token')

      let param = this.get_order_param(index, 2)

      await httpPost.post('/order_computer', param)
          .then(res => {
            ElMessage.success(res.data)
          })
          .catch(() => {
            ElMessage.error('预约失败，请稍后重试！')
          })

      await this.get_computers_list(this.activate_room, this.select_date, this.select_time)
      this.loading = false
    },
    async get_computers_list(room, date, time) {
      await httpGet('/student_room_detail?room_id=' + room + "&date=" + date + '&time=' + time)
          .then(res => {
            this.computers = res.data
            this.loading = false
          })
          .catch(err => {
            console.log(err)
            this.loading = false
          })
    },
    async edit_name() {
      if (!this.edit_self) {
        this.edit_self = true
      } else {
        await httpGet.get('token')

        await httpPost.post('/student_update_info', {id: Cookies.get('account'), name: this.form.name})
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
    async shutdown(index) {
      this.loading = true
      let id = this.ordered[index].record_id
      await httpGet.get('/token')

      await httpPost.post('/shutdown', {record_id: id, student_id: Cookies.get('account')})
          .then(res => {
            ElMessage.success(res.data)
          })
          .catch(() => {
            ElMessage.error('下机失败！')
            this.loading = false
          })

      await this.get_user_info()
      this.loading = false
    },
    async sign_off() {
      Cookies.remove('type')
      Cookies.remove('account')
      Cookies.remove('password')
      await router.push({name: 'login'})
    },
    back() {
      this.activate_room = null
    }
  }
}
</script>

<template>
  <el-row>
    <el-col :span="4">
      <el-menu default-active="1" @select="index => this.menu_index = index">
        <el-menu-item index="1">
          机房预约
        </el-menu-item>
        <el-menu-item index="2">
          个人中心
        </el-menu-item>
        <el-menu-item index="3">
          订单中心
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="1"/>
    <el-col :span="19">
      <div v-if="menu_index === '1'">
        <div class="time-select">
          <el-row>
            <el-date-picker
                v-model="select_date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                :disabled-date="disabled_date_rule"
                style="margin-right: 2%"
            ></el-date-picker>
            <el-time-select
                v-model="select_time"
                :start="allowed_start_time"
                step="01:00"
                end="21:00"
                placeholder="选择起始时间"
            />
            <el-button type="primary" style="margin-left: 2%" @click="get_rooms_info" v-if="!activate_room">查询
            </el-button>
            <el-text size="small" style="margin-left: 2%">注：预约时长为一小时
            </el-text>
          </el-row>
        </div>
        <div v-if="!activate_room">
          <el-table :data="rooms" stripe width="100%" v-loading="loading" @row-click="handle_table_row_click">
            <el-table-column prop="id" label="房间编号"></el-table-column>
            <el-table-column prop="administrator" label="房间管理员"></el-table-column>
            <el-table-column prop="capacity" label="剩余机位数"></el-table-column>
          </el-table>
        </div>
        <div v-if="activate_room">
          <el-button @click="back">返回</el-button>
          <el-table :data="computers" stripe width="100%" v-loading="loading">
            <el-table-column prop="id" label="电脑编号"></el-table-column>
            <el-table-column prop="is_ordered" label="是否空闲"></el-table-column>
            <el-table-column label="预约">
              <template #default="scope">
                <el-button @click="order_computer(scope.$index)"
                           :disabled="computers[scope.$index].is_ordered === '已被预约'">自习预约
                </el-button>
                <el-button @click="order_computer_for_class(scope.$index)"
                           :disabled="computers[scope.$index].is_ordered === '已被预约'" type="primary">教学预约
                </el-button>
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
          <el-form-item label="余额">
            ￥{{ form.money }}
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="edit_name">{{ !edit_self ? '修改' : '保存' }}</el-button>
            <el-button type="danger" @click="sign_off">注销</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div v-if="menu_index === '3'">
        <el-table :data="ordered" stripe width="100%" v-loading="loading">
          <el-table-column prop="record_id" label="订单号"></el-table-column>
          <el-table-column prop="com_id" label="电脑编号"></el-table-column>
          <el-table-column label="预约时间">
            <template #default="scope">
              {{ ordered[scope.$index].date + " " + ordered[scope.$index].time }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="订单状态"></el-table-column>
          <el-table-column label="下机">
            <template #default="scope">
              <el-button v-if="ordered[scope.$index].status === '进行中'" type="danger" @click="shutdown(scope.$index)">下机</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>