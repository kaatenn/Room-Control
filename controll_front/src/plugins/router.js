import * as VueRouter from 'vue-router'

const login = () => import('../pages/login.vue')
const administer = () => import('../pages/administrator.vue')
const student = () => import('../pages/student.vue')

const routes = [
    {path: '/', redirect: '/page/login'},
    {path: '/page/login', component: login, name: 'login', meta: {title: '登录界面'}},
    {path: '/page/administrator', component: administer, name: 'administrator', meta: {title: '管理员界面'}},
    {path: '/page/student', component: student, name: 'student', meta: {title: '学生界面'}},
]

export const router = VueRouter.createRouter({
    history: VueRouter.createMemoryHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.title) {
        document.title = to.meta.title
    }
    next();
})