import {createWebHistory,createRouter} from "vue-router";
import Home from "@/views/Home.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";
import login from "@/views/login";
import signup from "@/views/signup";
import UserCenter from "@/views/UserCenter";

const routes = [
    {
        path:'/',
        name:"Home",
        component:Home,
    },
    {
        path: '/api/article/:id',
        name: "ArticleDetail",
        component: ArticleDetail
    },
    {
        path: '/login',
        name:"Login",
        component: login
    },
    {
        path: '/signup',
        name: "signup",
        component: signup
    },
    {
        path: '/user/:username',
        name: "UserCenter",
        component: UserCenter
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
