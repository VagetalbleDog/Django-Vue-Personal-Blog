<template>
  <BlogHeader/>
  <div style="padding-top: 150px;text-align: center">
    <h1 style="color: darkviolet;padding-top: 100px">您好像走丢了，您可以点击<router-link :to="{name:'Home'}">此处</router-link>或通过导航栏回到主页</h1>
    <p style="font-size: x-large;padding-top: 100px">您也可以通过以下方式联系开发者，提出您宝贵的建议，感谢！</p>
  <h1 style="color: dodgerblue;padding-top: 100px">QQ : 2583243657</h1>
  <h1 style="color: #42b983">Wechat: 18365051200</h1>
</div>
  <BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
export default {
  name: "ErrorPage404",
  components: {BlogFooter, BlogHeader}
}
</script>

<style scoped>

</style>