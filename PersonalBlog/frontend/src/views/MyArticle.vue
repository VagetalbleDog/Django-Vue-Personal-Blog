<template>
<BlogHeader/>
<div v-if="is_superuser==='true'&&hasLogin">
  <p style="text-align: left;padding-top: 70px;font-size: x-large">{{author_name}}&nbsp;您好！&nbsp;您创作的文章共{{info.count}}篇，如下：</p>
    <div class="row mt-2" v-for="article in info.results" v-bind:key="article.title">
        <!-- 文章内容 -->
        <div class="col-12" >
        <div class="image-container" style="float: left" v-if="article.avatar">
          <img :src="imageIfExists(article)" alt="" class="image">
        </div>
          <div style="padding-top: 30px">
                <router-link v-if="article.category !== null" class="category" :to="{name:'CategoryDetail',params: {category_name:article.category.title}}">{{article.category.title}}</router-link>
            <!-- 标签 -->
                <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
                  {{ tag }}
                </span>
            </div>
            <!-- 标题 -->
            <h3 style="padding-top: 20px">
                <b>
                    <router-link :to="{ name:'ArticleDetail',params: { id: article.id }}" class="article-title">{{ article.title }}</router-link>
                </b>
            </h3>
            <!-- 摘要 -->
            <!-- 注脚 -->
            <p style="padding-top: 20px">
                <!-- 附加信息 -->
                <span style="color: blue;">
                    {{ formatted_time(article.created) }} 发布&nbsp;&nbsp;&nbsp;
                </span>
                <span style="color: darkred;">
                    {{ formatted_time(article.updated) }} 更新 &nbsp;
                </span>
            </p>
        </div>
      <div>
        <hr>
      </div>
</div>
    <div id="paginator" style="padding-top: 50px">
      <span v-if="is_page_exists('previous')">
        <router-link :to="get_path('previous')" style="color: #42b983">
          上一页
        </router-link>
      </span>
      <span  class="current-page" v-if="get_page_param('current')" style="color: blue">
        第{{ get_page_param('current') }}页
      </span>
      <span  class="current-page" v-if="!get_page_param('current')" style="color: blue">
        第1页
      </span>
      <span v-if="is_page_exists('next')">
        <router-link :to="get_path('next')" style="color: #42b983">
          下一页
        </router-link>
      </span>
    </div>
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
    import axios from 'axios';
    import BlogHeader from "@/components/BlogHeader";
    import BlogFooter from "@/components/BlogFooter";


    export default {
        name: 'App',
      components: {BlogFooter, BlogHeader},
      data: function () {
            return {
                info:'',
              author_name: this.$route.params.author_name,
            }
        },
        computed: {
          is_superuser() {
            return localStorage.getItem('is_superuser.myblog')
          },
          hasLogin() {
            return (localStorage.getItem('login.myblog') === "1")
          },
        },
        mounted() {
            this.get_article_data()
        },
        methods:{
          imageIfExists(article){
            if(article.avatar){
              console.log('yes')
              return article.avatar.content
            }
          },
          formatted_time:function (iso_date_string){
            const date = new Date(iso_date_string);
            return date.toLocaleDateString()
          },
          // 判断页面是否存在
          is_page_exists:function (direction){
            if (direction === 'next'){
              return this.info.next !== null
            }
            return this.info.previous !== null
          },
          get_page_param:function (direction) {
            try {
              let url_string;
              switch (direction) {
                case 'next':
                  url_string = this.info.next;
                  break;
                case 'previous':
                  url_string = this.info.previous;
                  break;
                default:
                  return this.$route.query.page
              }
              const url = new URL(url_string);
              return url.searchParams.get('page')
            } catch (err) {
              console.log(err.message);
            }
          },
          get_article_data:function (){
            let url = '/api/article';
            let params = new URLSearchParams();
            params.append_if_exists('page', this.$route.query.page);
            const paramsString = params.toString();
            url += '/?'+'&search='+this.author_name+'&'+paramsString
            axios
                .get(url)
                .then(response => (this.info = response.data))
                .catch(function (error){
                  console.log(error.message);
                  if(error.response.status===404){
                    alert('您似乎还没有写文章哦')
                  }
                })
          },
          get_path:function (direction){
            let url = '';
            try{
              switch (direction){
                case 'next':
                  if (this.info.next !== undefined){
                    url += (new URL(this.info.next)).search
                  }
                  break;
                case 'previous':
                  if (this.info.previous!== undefined){
                    url += (new URL(this.info.previous)).search
                  }
                  break;
              }
            }
            catch {
              return url
            }
            return url
          }
        },
        watch:{
          $route(){
            this.get_article_data()
          }
        }
    }
</script>

<style scoped>
    .image{
      width: 155px;
      border-radius: 10px;
      box-shadow: darkslategrey 0 0 12px;
    }
    .image-container{
      width: 170px;
    }
    .category{
      padding: 5px 10px 5px 10px;
      margin: 5px 5px 5px 0;
      font-family: Georgia, Arial , sans-serif;
      font-size: small;
      background-color: darkgreen;
      color: whitesmoke;
      border-radius: 15px;
      text-decoration: none;
    }
    .article-title {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }
    .tag{
      padding: 2px 5px 2px 5px;
      margin: 5px 5px 5px 0;
      font-family: Georgia, Arial ,sans-serif;
      font-size:small;
      background-color: dodgerblue;
      color: whitesmoke;
      text-shadow: white;
      border-radius: 5px;
    }
    #paginator{
      text-align: center;
      padding-top: 50px;
    }
    a{
      color: black;
    }
    .current-page{
      font-size: x-large;
      font-weight: bold;
    }
</style>