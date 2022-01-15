<template>
  <BlogHeader/>
  <ArticleList/>
  <BlogFooter/>
</template>
<!--前端组件化-->
<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
import ArticleList from "@/components/ArticleList";

export default {
  name:'Home',
  components: {BlogFooter, BlogHeader,ArticleList}
}
</script>

<style>
    #app{
      font-family: Georgia, Arial , sans-serif;
      margin-left: 40px;
      margin-right: 40px;
    }
</style>