<template>
<BlogHeader/>
<div style="padding-top: 150px;text-align: center">
  <p style="font-size: x-large">本项目属于个人博客，发表文章属于敏感权限，请通过以下方式联系开发者。确定身份和意图后，将会赋予您发表文章的权限</p>
  <h1 style="color: dodgerblue;padding-top: 100px">QQ : 2583243657</h1>
  <h1 style="color: #42b983">Wechat: 18365051200</h1>
  <p style="font-size: x-large;padding-top: 100px">谢谢您的理解！</p>
</div>
<BlogFooter/>
</template>

<script>
import BlogFooter from "@/components/BlogFooter";
import BlogHeader from "@/components/BlogHeader";

export default {
  name: "RequireAuthorizations",
  components: {BlogFooter, BlogHeader}
}
</script>

<style scoped>

</style>