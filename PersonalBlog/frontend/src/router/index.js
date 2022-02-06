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
import ErrorPage404 from "@/views/ErrorPage404";

const routes = [
    {
        path:'/',
        name:"Home",
        component:Home,
        meta:{title:'朱文甫的个人博客'}
    },
    {
        path: '/api/article/:id',
        name: "ArticleDetail",
        component: ArticleDetail,
        meta: {title: '文章详情'}
    },
    {
        path: '/login',
        name:"Login",
        component: login,
        meta: {title: '登录'}
    },
    {
        path: '/signup',
        name: "signup",
        component: signup,
        meta: {title: '注册'}
    },
    {
        path: '/user/:username',
        name: "UserCenter",
        component: UserCenter,
        meta: {title: '用户中心'}
    },
    {
        path: '/article/create',
        name:"ArticleCreate",
        component: ArticleCreate,
        meta: {title: '发表文章'}
    },
    {
        path: '/require/authorization',
        name:"RequireAuthorization",
        component: RequireAuthorizations,
        meta: {title: '获取权限'}
    },
    {
        path: '/category/:category_name',
        name:"CategoryDetail",
        component: CategoryDetail,
        meta: {title: '分类详情'}
    },
    {
        path: '/article/edit/:article_id',
        name:"ArticleEdit",
        component: ArticleEdit,
        meta: {title: '更新或删除文章'}
    },
    {
        path: '/myarticle/:author_name',
        name:'MyArticle',
        component: MyArticle,
        meta: {title: '我发表的文章'}
    },
    {
        path: '/:pathMatch(.*)',
        name:'error404',
        component: ErrorPage404,
        meta: {title: '您好像走丢了'}
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})
router.beforeEach((to,from,next)=>{
    to.meta.title && (document.title = to.meta.title);
    next()
});
export default router;
