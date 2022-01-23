<template>
<BlogHeader/>
  <div v-if="is_superuser==='true'&&hasLogin" id="article-create">
    <h3>更新或删除文章</h3>
    <form id="image_form" v-if="!avatar">
    <div class="form-elem">
      <span>标题图：</span>
      <input v-on:change="onFileChange" type="file" id="file" style="padding-bottom:3px;opacity: 0.5" accept="image/gif,image/jpeg">
    </div>
  </form>
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
      <div style="padding-left: 500px">
      <div class="form-elem" style="padding-top:10px;float: left">
        <button v-on:click.prevent="submit" style="width: auto;background-color: dodgerblue">提交修改</button>
      </div>
      <div class="form-elem" style="padding-top:10px;text-align: left">
        <button v-on:click.prevent="showingDeleteAlert = true" class="delete-btn" style="width: auto">删除文章</button>
        <div :class="{shake:showingDeleteAlert}" style="padding-left: 80px">
          <button v-if="showingDeleteAlert" class="confirm-btn" @click.prevent="delete_article(article_id)" style="width: auto">您确定吗？</button>
        </div>
      </div>
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
  name: "ArticleEdit",
  components: {BlogFooter, BlogHeader},
  data:function (){
    return{
      title:'',
      body:'',
      categories:[],
      selectedCategory:null,
      tags:'',
      showingDeleteAlert:false,
      article_id: this.$route.params.article_id,
      avatarID:null,
      avatar:null,
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
      // 页面初始化时获取所有分类
      axios
        .get('/api/category/')
        .then(response => this.categories = response.data);
      // 获取旧数据
      const that = this;
      axios
        .get('/api/article/' + this.$route.params.article_id + '/')
        .then(function (response) {
          const data = response.data;
          that.title = data.title;
          that.body = data.body;
          that.selectedCategory = data.category;
          that.tags = data.tags.join(',');
          that.articleID = data.id;
          that.avatar = data.avatar;
        })
    },
  methods:{
    onFileChange(e){
      const that = this;
      const file = e.target.files[0];
      let formData = new FormData();
      formData.append("content",file);
      // 验证一下权限
      authorization()
        .then(function (response) {
          if (response[0]) {
            console.log('ssss')
            axios
                .post('/api/avatar/', formData, {
                  headers:{
                    'Content-Type':'multipart/form-data',
                    'Authorization':'Bearer '+localStorage.getItem('access.myblog')
                  }
                })
                .then(response => that.avatarID = response.data.id)
                .catch(function (error){
                  console.log(error.message);
                  alert('标题图未成功上传，请联系开发人员解决。')
                })
          } else {
            alert('请登录后再进行操作！');
            that.$router.push({name:'Login'})
          }
        })
    },
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
    //删除文章方法
    delete_article(article_id){
            //获取token
            const that = this;
            const token = localStorage.getItem('access.myblog');
            authorization()
              .then(function (response){
                if(response[0]){
                  const url = '/api/article/'+article_id;
                  console.log('删除文章进程开始，文章id：',article_id);
                  axios
                    .delete(url,{
                      headers:{Authorization: 'Bearer '+token}
                    })
                    .then(function (){
                      console.log('文章已删除.');
                      alert('文章已删除！');
                      const username = localStorage.getItem('username.myblog')
                      that.$router.push({name:'MyArticle',params:{author_name: username}})
                    })
                    .catch(function (error){
                      console.log(error.message);
                      alert("似乎出了点问题。")
                    })
                }
                else {
                  alert('令牌过期，请重新登录！')
                }
              })
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
            data.avatar_id = that.avatarID;
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
            const url = '/api/article/'+that.article_id+'/';
            // 发送请求POST
            axios
              .put(url,data,{
                headers:{Authorization: 'Bearer '+token}
              })
              .then(function (response){
                console.log("文章修改成功!文章id：",that.article_id);
                alert("文章修改成功！");
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
  .delete-btn {
        background-color: darkred;
        margin-bottom: 10px;
    }
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
  .confirm-btn {
        width: 80px;
        background-color: darkorange;
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