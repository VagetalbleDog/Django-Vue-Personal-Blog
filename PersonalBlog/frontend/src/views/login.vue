<template>
  <BlogHeader/>
      <div id="signin" style="padding-top: 100px">
        <h3>登录</h3>
        <form>
          <div class="form-elem">
            <span>账号：</span>
            <input v-model="signInName" type="text" placeholder="用户名">
          </div>
          <div class="form-elem">
            <span>密码：</span>
            <input v-model="signInPwd" type="password" placeholder="密码">
          </div>
          <div class="form-elem">
            <button v-on:click.prevent="signIn">确定</button>
          </div>
        </form>
      </div>
  <BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
import axios from "axios";
export default {
  name: "login",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return{
      signInName:'',
      signInPwd:'',
    }
  },
  methods:{
    signIn(){
      const that = this;
      axios
          .post('/api/token/',{
            username:that.signInName,
            password:that.signInPwd,
          })
          .then(function (response){
            const storage = localStorage;
            //Token被设置为5分钟
            const expiredTime = Date.parse(response.headers.date) + 60000*5;
            //设置localStorage

            storage.setItem('access.myblog',response.data.access);
            storage.setItem('refresh.myblog',response.data.refresh);
            storage.setItem('expiredTime.myblog',expiredTime);
            storage.setItem('username.myblog',that.signInName);
            //写入登录状态
            storage.setItem('login.myblog',"1")
            //路由跳转
            that.$router.push({name:'Home'});
            //登录成功后回到博客首页
          })
          .catch(function (error){
            if(error.response.status===401){
              alert("账号或密码错误！")
            }
            console.log(error.message)
          })
      axios
          .get('/api/user/'+that.signInName+'/')
          .then(function (response){
            localStorage.setItem('is_superuser.myblog',response.data.is_superuser);
            if(localStorage.getItem('is_superuser.myblog')==="true"){
              console.log('当前用户为管理员。')
            }
          })
          .catch(function (error) {
            console.log(error.message)
            alert('貌似除了点问题，不能加载您的权限信息，请尝试联系管理员？谢谢您的反馈!')
          })
    }
    }
}
</script>

<style scoped>
    #signin{
      text-align: center;
    }
    .form-elem {
        padding: 10px;
    }
    input {
        height: 25px;
        padding-left: 10px;
    }
    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>