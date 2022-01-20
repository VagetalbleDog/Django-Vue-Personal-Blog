<template>
<BlogHeader/>
<div v-if="is_superuser==='true'&&hasLogin" id="article-create">
    <h3>发表文章</h3>
    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input v-model="title" type="text" placeholder="输入文章标题">
      </div>

      <div class="form-elem">
        <span>分类：</span>
        <span v-for="category in categories" :key="category.id">
          <!--样式也可以通过 :style 绑定-->
          <button class="category-btn" :style="categoryStyle(category)" @click.prevent="chooseCategory(category)">
            {{category.title}}
          </button>
        </span>
      </div>

      <div class="form-elem">
        <span>标签：</span>
        <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔">
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="输入正文，推荐使用Markdown语法，让你的文章更有层次感" rows="20" cols="80"></textarea>
      </div>

      <div class="form-elem" style="padding-top:10px;text-align: center">
        <button v-on:click.prevent="submit">提交</button>
      </div>
    </form>
</div>
  <div v-else-if="hasLogin" style="padding-top: 150px;font-size: x-large">
    <p style="text-align: center">抱歉，您的权限暂不支持！请<router-link :to="{name:'RequireAuthorization'}" class="login-link">联系开发者获取权限</router-link>后再进行相关操作.</p>
    <p style="text-align: center"><router-link to="{name:'Home'}">您也可以点击这里回到主页</router-link></p>
  </div>
  <div v-else style="padding-top: 150px;font-size: x-large">
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
export default {
  name: "ArticleCreate",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return{
      title:'',
      body:'',
      categories:[],
      selectedCategory:null,
      tags:'',
    }
  },
  computed:{
    is_superuser(){
      return localStorage.getItem('is_superuser.myblog')
    },
    hasLogin(){
      return (localStorage.getItem('login.myblog') === "1")
    },
  },
  mounted() {
    //页面初始化时获取所有分类
    axios
    .get('/api/category/')
    .then(response => this.categories=response.data)
  },
  methods:{
    // 根据分类是否被选中，按钮的颜色发生变化
    // 这里可以看出Css也是可以被vue所绑定的，肥肠的方便
    categoryStyle(category){
      if(this.selectedCategory!==null && category.id===this.selectedCategory.id){
        return{
          backgroundColor:'green',
        }
      }
      return {
        backgroundColor: 'lightgrey',
        color:'black',
      }
    },
    // 选取分类的方法
    chooseCategory(category){
      // 如果点击已选取的分类。则将selectedCategory置空
      if(this.selectedCategory!==null && category.id===this.selectedCategory.id){
        this.selectedCategory = null;
      }
      // 若点击没有被选中的，则选中他
      else {
        this.selectedCategory = category;
      }
    },
    // 提交方法
    submit(){
      const that = this;
      // 验证一下权限
      authorization()
        .then(function (response){
          if (response[0]){
            let data = {
              title:that.title,
              body:that.body,
            };
            // 添加分类
            if(that.selectedCategory){
              data.category_id = that.selectedCategory.id;
            }
            // 标签预处理
            data.tags = that.tags
                // 逗号分割标签
              .split(/[,.，]/)
                // 剔除标签首位空格
              .map(x=>x.trim())
                // 剔除长度为0的无效标签
              .filter(x=>x.charAt(0)!=='');
            // 获取token
            const token = localStorage.getItem('access.myblog');
            // 发送请求POST
            axios
              .post('/api/article/',data,{
                headers:{Authorization: 'Bearer '+token}
              })
              .then(function (response){
                console.log("新文章提交成功!");
                alert("提交成功！");
                that.$router.push({name:'ArticleDetail',params:{id:response.data.id}});
              })
              .catch(function (error){
                console.log(error.message);
                alert('似乎除了点问题，您可以联系开发者解决.');
              })
          }else {
            alert("登录已过期，请重新登录哦")
            that.$router.push({name:'Login'})
          }
        })
    }
  }
}
</script>

<style scoped>
  .category-btn {
    margin-right: 10px;
    font-size: 13px;
  }
  #article-create {
    text-align: center;
    font-size: large;
  }
  form {
    text-align: left;
    padding-left: 100px;
    padding-right: 10px;
  }
  .form-elem {
    padding: 10px;
  }
  input {
    height: 25px;
    padding-left: 10px;
    width: 50%;
  }
  button {
    height: 35px;
    cursor: pointer;
    border: none;
    outline: none;
    background: steelblue;
    color: whitesmoke;
    border-radius: 5px;
    width: 60px;
  }
</style>