<template>
  <BlogHeader :welcome-name="welcomeName"/>
  <div v-if="hasLogin">
    <div id="user-center">
    <h3>更新用户资料</h3>
    <form>
      <div class="form-elem">
        <h4>当前用户名：{{oldName}}</h4>
        <span>新用户名：</span>
        <input v-model="NewUsername" placeholder="新的用户名">
      </div>
      <div class="form-elem">
        <span>新密码：</span>
        <input v-model="NewPassword" type="password" placeholder="新的密码">
      </div>
      <div class="form-elem">
        <span>重复密码：</span>
        <input v-model="RePassword" type="password" placeholder="重复密码">
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="changeInfo">更新</button>
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="showingDeleteAlert = true" class="delete-btn">点击删除用户</button>
        <div :class="{shake:showingDeleteAlert}">
          <button v-if="showingDeleteAlert" class="confirm-btn" @click.prevent="confirmDelete">确定？</button>
        </div>
      </div>
    </form>
  </div>
  </div>
  <div v-else>
    <p style="text-align: center">抱歉，您还未登录！请<router-link to="/login" class="login-link">登录</router-link>后再进行相关操作.</p>
    <p style="text-align: center"><router-link to="{name:'Home'}">您可以点击这里回到主页</router-link></p>
  </div>
  <BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";

import axios from "axios";
import authorization from "@/utils/authorization";
const storage = localStorage;
export default {
  computed:{
    hasLogin(){
      return (localStorage.getItem('login.myblog') === "1")
    }
  },
  name: "UserCenter",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return {
      NewUsername:'',
      NewPassword:'',
      RePassword:'',
      welcomeName:'',
      token:'',
      showingDeleteAlert:false,
      oldName:storage.getItem('username.myblog')
    }
  },
  mounted() {
    this.username = storage.getItem('username.myblog');
    this.welcomeName = storage.getItem('username.myblog');
  },
  methods:{
    confirmDelete(){
      const that = this;
      authorization()
        .then(function (response){
          // 检查登录状态,若登录状态已经过期则不执行后续操作
          if(!response[0]){
            alert('登录已过期，请重新登录!')
            return
          }
          if (response[0]){
            console.log('删除用户信息进程开始')
            // 获取令牌
            that.token = storage.getItem('access.myblog');
            axios
              .delete('/api/user/'+that.username+'/',{
                headers:{Authorization:'Bearer '+that.token}
              })
              .then(function (){
                storage.clear();
                console.log('删除用户信息进程完成')
                alert("该用户已删除，将跳转回主页，期待与您的下次见面！")
                //回到主页
                that.$router.push({name:'Home'});
              })
              .catch(function (error){
                alert("我似乎没办法帮你删除，试试看联系开发人员报告bug？谢谢您的帮助！")
                console.log(error.message)
              })
          }
        })
    },
    changeInfo(){
      const that = this;
      // 验证登录状态
      authorization()
      .then(function (response){
        // 检查登录状态,若登录状态已经过期则不执行后续操作
        if(!response[0]){
          alert('登录已过期，请重新登录!')
          return
        }
        console.log('改变用户信息进程开始')
        //密码大于9位小于16位
        if(that.NewPassword.length<9 || that.NewPassword.length>16){
          alert('密码长度不符合要求!');
          return;
        }
        // 使用原username向后端服务器发送请求
        const oldName = storage.getItem('username.myblog');
        // V-model获取表单信息
        let data = {};
        if(that.NewPassword === that.RePassword){
          if(that.NewUsername!==''){
            data.username = that.NewUsername
          }
          data.password = that.NewPassword
        }else {
          alert('两次输入密码不一致！请重新输入!')
          return;
        }
        that.token = storage.getItem('access.myblog');
        // 发送请求，更改用户信息
        axios
            .patch('/api/user/'+oldName+'/',
                data,
                {
              headers:{Authorization: 'Bearer '+that.token } //注意Bearer后面的空格阿，坑苦我了
            })
            .then(function (response){
              const name = response.data.username;
              storage.setItem('username.myblog',name);
              alert('修改成功！');
              that.welcomeName = name;
              console.log('改变用户信息完成');
              that.$router.push({name:'UserCenter',params:{username:name}});
        })
            .catch(function (error){
              console.log(error.message);
              if(error.response.status===400){
                alert('此用户名已存在，请重新输入！');
              }
            })
      })
    }
  }
}
</script>

<style scoped>
    #user-center {
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
        width: 200px;
    }
    .confirm-btn {
        width: 80px;
        background-color: darkorange;
    }
    .delete-btn {
        background-color: darkred;
        margin-bottom: 10px;
    }
    .shake {
        animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
        transform: translate3d(0, 0, 0);
        backface-visibility: hidden;
        perspective: 1000px;
    }
    @keyframes shake {
        10%,
        90% {
            transform: translate3d(-1px, 0, 0);
        }
        20%,
        80% {
            transform: translate3d(2px, 0, 0);
        }
        30%,
        50%,
        70% {
            transform: translate3d(-4px, 0, 0);
        }
        40%,
        60% {
            transform: translate3d(4px, 0, 0);
        }
    }
</style>