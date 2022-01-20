<template>
<BlogHeader/>
      <div id="signup" style="padding-top: 150px">
        <h3>注册账号</h3>
        <form>
          <div class="form-elem">
            <span>账号：</span>
            <input v-model="signUpName" type="text" placeholder="用户名">
          </div>
          <div class="form-elem">
            <span>密码：</span>
            <input v-model="signUpPwd" type="password" placeholder="密码长度建议在9-16位之间">
          </div>
          <div class="form-elem">
            <span> 重复：</span>
            <input v-model="rePwd" type="password" placeholder="请重新输入密码">
          </div>
          <div class="form-elem">
            <button v-on:click.prevent="signUp">确定</button>
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
  name: "signup",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return{
      signUpName:'',
      signUpPwd:'',
      rePwd:'',
      signUpResponse:null,
    }
  },
  methods:{
    signUp(){
      const that = this;
      if(this.signUpPwd===this.rePwd){
        axios
        .post('api/user/',{
          username:this.signUpName,
          password:this.signUpPwd,
        })
        .then(function (response){
            that.signUpResponse = response.data;
            alert('您已经注册成功了，快去登录看看吧!');
            that.$router.push('/login')
          })
        .catch(function (error){
            if(error.response.status===400){
              alert('此用户名已存在，请重新注册!')
            }
          })
      }
      else {
        alert('两次密码输入不一致，清重新输入！')
      }
    }
  }
}
</script>

<style scoped>
    #grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
    #signup {
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