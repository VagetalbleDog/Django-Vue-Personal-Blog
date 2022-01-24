<template>
  <div id="ArticleList">
    <search-button/>
    <p style="text-align: left;font-size: x-large">本博客现存文章共{{info.count}}篇，如下：</p>
    <div class="row mt-2" v-for="article in info.results" v-bind:key="article.title">
        <!-- 文章内容 -->
        <div class="col-12" >
        <div class="image-container" style="float: left" v-if="article.avatar">
          <img :src="image_if_exists(article)" alt="" class="image">
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
                <span style="color: blueviolet;">
                    由&nbsp;{{article.author.username}} 创作
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
</template>

<script>
    import SearchButton from "@/components/SearchButton";
    import {ref} from "vue";
    import {useRoute} from "vue-router";
    import getArticleData from "@/composables/getArticleData";
    import pagination from "@/composables/paginations";
    import imageIfExists from "@/composables/imageIfExists";
    import formattedTime from "@/composables/formattedTime";

    export default {
      name:'ArticleList',
      components: {SearchButton},
      setup(){
        const info = ref('');
          // 创建路由
        const route = useRoute();
        getArticleData(info,route);
        const {
          is_page_exists,
          get_page_param,
          get_path
        } = pagination(info,route);
        const formatted_time = formattedTime;
        const image_if_exists = imageIfExists;
        return{
          info,
          is_page_exists,
          get_page_param,
          get_path,
          image_if_exists,
          formatted_time,
        }
      },
    }
</script>

<style scoped>
    #ArticleList{
      margin-left: 50px;
      margin-right: 50px;
    }
    .image{
      width: 155px;
      border-radius: 10px;
      box-shadow: darkslategrey 0 0 12px;
    }
    .image-container{
      width: 170px;
    }
    .category{
      padding: 7px 10px 7px 10px;
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