<template>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <!-- 导航栏商标 -->
    <div class="navbar-brand" style="text-align: left">
          Personal Blog&nbsp;&nbsp;朱文甫的个人博客
    </div>
    <!-- 导航入口 -->
    <div v-if="hasLogin" style="text-align: right">
      <ul class="navbar-nav">
        <!-- 条目 -->
        <li class="nav-item">
          <div class="dropdown">
          <button class="dropbtn">欢迎，{{ name }}</button>
          <div class="dropdown-content">
            <router-link :to="{name:'UserCenter',params:{username:username}}">用户中心</router-link>
            <router-link v-on:click.prevent="logout" to="/">点击注销</router-link>
          </div>
          </div>
        </li>
        <li class="nav-item" v-if="is_superuser==='true'">
          <router-link :to="{name:'ArticleCreate'}" class="nav-link">点击发表文章</router-link>
        </li>
        <li class="nav-item" v-if="is_superuser==='true'">
          <router-link :to="{name:'MyArticle',params: {author_name:username}}" class="nav-link">我的文章</router-link>
        </li>
        <li class="nav-item" v-else>
          <router-link :to="{name:'RequireAuthorization'}" class="nav-link">发表文章,点击获取权限</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/" class="nav-link">回到主页</router-link>
        </li>
      </ul>
      </div>
    <div v-else>
      <ul class="navbar-nav">
        <!-- 条目 -->
        <li class="nav-item">
          <router-link to="/login" class="nav-link">登录</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/signup" class="nav-link">注册</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/" class="nav-link">回到主页</router-link>
        </li>
      </ul>
    </div>
  </div>
</nav>
</template>

<script>
import authorization from "@/utils/authorization";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
export default {
  //Vue规定camelCase（驼峰命名法）的prop名需要使用其等价的kebab-case（短横线分割命名），所以这里的welcomeName对应welcome-name
  props:['welcomeName'],
  //props 父组件可以向子组件传递数据,但反过来不行
  computed:{
    //计算属性，基于相应式依赖进行缓存，与methods不同的地方在于：只在相应式依赖发生改变时，它们才会重新求值；而每次触发渲染时，methods都会执行函数
    //一般来说，能用computed就尽量用，算是用空间换时间的措施
    name(){
      return(this.welcomeName !== undefined)? this.welcomeName:this.username
    },
    hasLogin(){
      return (localStorage.getItem('login.myblog') === "1")
    },
    is_superuser(){
      return localStorage.getItem('is_superuser.myblog')
    },
  },
  name: "BlogHeader",
  data:function (){
    return{
      username:' ',
    }
  },
  mounted() {
    authorization().then((data)=>[this.username]=data);
  },
  methods:{
     logout(){
       localStorage.clear();
       window.location.reload(false);
    },
    refresh(){
       this.username = localStorage.getItem('username.myblog');
    }
  }
}
</script>

<style scoped>
    /* 样式来源: https://www.runoob.com/css/css-dropdowns.html* /
    /* 下拉按钮样式 */
    .dropbtn {
        background-color: mediumslateblue;
        color: white;
        padding: 8px 8px 30px 8px ;
        font-size: 16px;
        border: none;
        cursor: pointer;
        height: 16px;
        border-radius: 5px;
    }
    /* 容器 <div> - 需要定位下拉内容 */
    .dropdown {
        position: relative;
        display: inline-block;
    }
    /* 下拉内容 (默认隐藏) */
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 120px;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    /* 下拉菜单的链接 */
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    /* 鼠标移上去后修改下拉菜单链接颜色 */
    .dropdown-content a:hover {
        background-color: #f1f1f1
    }
    /* 在鼠标移上去后显示下拉菜单 */
    .dropdown:hover .dropdown-content {
        display: block;
    }
    /* 当下拉内容显示后修改下拉按钮的背景颜色 */
    .dropdown:hover .dropbtn {
        background-color: darkslateblue;
    }
</style>