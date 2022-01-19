<template>
  <BlogHeader/>
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
    </form>
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
  name: "UserCenter",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return {
      NewUsername:'',
      NewPassword:'',
      RePassword:'',
      token:'',
      oldName:storage.getItem('username.myblog')
    }
  },
  mounted() {
    this.username = storage.getItem('username.myblog');
  },
  methods:{
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
              alert('修改成功！')
              console.log('改变用户信息完成')
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
</style>