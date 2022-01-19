<template>
    <div id="header">
      <div class="grid">
        <div></div>
        <h1>Personal Blog——Django-Vue</h1>
        <search-button/>
    </div>
      <hr>
      <div v-if="hasLogin" style="text-align: right">
        <div class="dropdown">
          <button class="dropbtn">欢迎，{{ username }}</button>
          <div class="dropdown-content">
            <router-link :to="{name:'UserCenter',params:{username:username}}">用户信息中心</router-link>
            <router-link v-on:click.prevent="logout" to="/">点击注销</router-link>
          </div>
      </div>
      </div>
      <div v-else>
        <div class="login">
          请<router-link to="/login" class="login-link">登录</router-link>---还没有账号？请<router-link to="/signup" class="login-link">注册</router-link>
        </div>
      </div>
      <div style="text-align: left"><h4>欢迎大家批评指正！BestWishes！</h4></div>
    </div>
</template>

<script>
import authorization from "@/utils/authorization";
import SearchButton from "@/components/SearchButton";
export default {
  name: "BlogHeader",
  components: {SearchButton},
  data:function (){
    return{
      username:'',
      hasLogin:false,
    }
  },
  mounted() {
    authorization().then((data)=>[this.hasLogin,this.username]=data);
  },
  methods:{
   logout(){
     localStorage.clear();
     window.location.reload(false);
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
    #header {
        text-align: center;
        margin-top: 20px;
    }
    .grid{
      display: grid;
      grid-template-columns: 1fr 4fr 1fr;
    }
    .login-link {
        color: black;
    }
    .login {
        text-align: right;
        padding-right: 5px;
    }
</style>