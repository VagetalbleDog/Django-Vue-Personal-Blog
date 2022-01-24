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
import ArticleEdit from "@/composables/ArticleEdit";
import axios from "axios";
import {onMounted, ref} from "vue";
import { useRouter} from "vue-router";
import authorization from "@/utils/authorization";
export default {
  name: "ArticleEdit",
  components: {BlogFooter, BlogHeader},
  setup(){
    const router = useRouter();
    const title = ref('');
    const body = ref('');
    const categories = ref([]);
    const selectedCategory = ref(null);
    const tags = ref(' ');
    const showingDeleteAlert = ref(false);
    const article_id = router.currentRoute.value.params.article_id
    const avatarID = ref(null);
    const avatar = ref(null);
    const getOldData = function (){
      axios
        .get('/api/category/')
        .then(response => categories.value = response.data);
      // 获取旧数据
      axios
        .get('/api/article/' + article_id + '/')
        .then(function (response) {
          const data = response.data;
          title.value = data.title;
          body.value = data.body;
          selectedCategory.value = data.category;
          tags.value = data.tags.join(',');
          avatar.value = data.avatar;
          avatarID.value=data.avatar.id;
        })
    }
    onMounted(getOldData);
    // 一些methods
    const onFileChange = function (e){
      const file = e.target.files[0];
      let formData = new FormData();
      formData.append("content",file);
    // 验证一下权限
      authorization()
          .then(function (response) {
              if (response[0]) {
              console.log('标题图开始上传');
              axios
                  .post('/api/avatar/', formData, {
                      headers:{
                      'Content-Type':'multipart/form-data',
                      'Authorization':'Bearer '+localStorage.getItem('access.myblog')
                    }
                  })
                  .then(response => avatarID.value = response.data.id)
                  .catch(function (error){
                      console.log(error.message);
                      alert('标题图未成功上传，请联系开发人员解决。')
                  })
              } else {
              alert('请登录后再进行操作！');
              router.push({name:'Login'})
          }
        })
    };
    const categoryStyle = function (category) {
      if(selectedCategory.value.id !== null && category.id===selectedCategory.value.id){
        return{
          backgroundColor:'green',
        }
      }
      return {
        backgroundColor: 'lightgrey',
        color:'black',
      }
    };
    const chooseCategory = function (category){
      // 如果点击已选取的分类。则将selectedCategory置空
          if(selectedCategory.value!==null && category.id===selectedCategory.value.id){
            selectedCategory.value = null;
          }
          // 若点击没有被选中的，则选中他
          else {
            selectedCategory.value.id = category.id;
          }
    };
    const {
      submit,
      delete_article
    } = ArticleEdit(title,body,avatarID,selectedCategory,tags,article_id,router);
    return{
      title,
      body,
      categories,
      selectedCategory,
      tags,
      showingDeleteAlert,
      article_id,
      avatarID,
      avatar,
      submit,
      delete_article,
      onFileChange,
      categoryStyle,
      chooseCategory,
    }
  },
  computed:{
    is_superuser(){
      return localStorage.getItem('is_superuser.myblog')
    },
    hasLogin(){
      return (localStorage.getItem('login.myblog') === "1")
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