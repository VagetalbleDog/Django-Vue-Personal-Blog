import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap'

//在原型链的基础上，定义一个append_if_exists后面会用到的
URLSearchParams.prototype.append_if_exists = function (key,value){
    if (value !== null && value !== undefined){
        this.append(key,value)
    }
};
const app = createApp(App)

app.use(router)

app.mount('#app')
