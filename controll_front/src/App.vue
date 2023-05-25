<template>
    <router-view></router-view>
</template>
<script>
import Cookies from "js-cookie";
import {router} from "@/plugins/router";
export default {
    name: 'App',
    mounted() {
        let type = Cookies.get('type')
        if (type) {
            router.push({name: type})
        }
    }
}
</script>