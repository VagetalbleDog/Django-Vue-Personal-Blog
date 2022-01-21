<template>
<BlogHeader/>
  <p style="text-align: left;padding-top: 70px;font-size: x-large"><span class="category" style="font-size: large">{{category_name}}</span>&nbsp;分类&nbsp;文章如下：</p>
    <div class="row mt-2" v-for="article in info.results" v-bind:key="article.title">
        <!-- 文章内容 -->
        <div class="col-12" v-if="article.category !== null&&article.category.title===category_name">
                <router-link v-if="article.category !== null" class="category" :to="{name:'CategoryDetail',params: {category_name:article.category.title}}">{{article.category.title}}</router-link>
            <!-- 标签 -->
                <span v-for="tag in article.tags" v-bind:key="tag" class="tag">
                  {{ tag }}
                </span>
            <!-- 标题 -->
            <h3>
                <b>
                    <router-link :to="{ name:'ArticleDetail',params: { id: article.id }}" class="article-title">{{ article.title }}</router-link>
                </b>
            </h3>
            <!-- 摘要 -->
            <!-- 注脚 -->
            <p>
                <!-- 附加信息 -->
                <span style="color: blue;">
                    {{ formatted_time(article.created) }} 发布&nbsp;&nbsp;&nbsp;
                </span>
                <span style="color: darkred;">
                    {{ formatted_time(article.updated) }} 更新
                </span>
            </p>
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
              category_name: this.$route.params.category_name,
            }
        },
        mounted() {
            this.get_article_data()
        },
        methods:{
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
          // 获取页码和搜索参数
          get_page_param:function (direction){
            try{
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
            }
            catch (err){
              console.log(err.message);
            }
          },
          get_article_data:function (){
            let url = '/api/article';
            let params = new URLSearchParams();
            params.append_if_exists('page',this.$route.query.page)
            params.append_if_exists('search',this.$route.query.search)
            const paramsString = params.toString();
            if(paramsString.charAt(0)!==''){
              url += '/?'+paramsString
            }
            axios
                .get(url)
                .then(response => (this.info = response.data))
                .catch(error => console.log(error))
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