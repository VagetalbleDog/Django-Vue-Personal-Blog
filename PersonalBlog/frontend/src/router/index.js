import {createWebHistory,createRouter} from "vue-router";
import Home from "@/views/Home.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";
import login from "@/views/login";
import signup from "@/views/signup";
import UserCenter from "@/views/UserCenter";
import ArticleCreate from "@/views/ArticleCreate";
import RequireAuthorizations from "@/views/RequireAuthorizations";
import CategoryDetail from "@/views/CategoryDetail";
import ArticleEdit from "@/views/ArticleEdit";
import MyArticle from "@/views/MyArticle";

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
    },
    {
        path: '/article/create',
        name:"ArticleCreate",
        component: ArticleCreate
    },
    {
        path: '/require/authorization',
        name:"RequireAuthorization",
        component: RequireAuthorizations
    },
    {
        path: '/category/:category_name',
        name:"CategoryDetail",
        component: CategoryDetail
    },
    {
        path: '/article/edit/:article_id',
        name:"ArticleEdit",
        component: ArticleEdit
    },
    {
        path: '/myarticle/:author_name',
        name:'MyArticle',
        component: MyArticle
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
