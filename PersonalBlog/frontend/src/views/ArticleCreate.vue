<template>
<BlogHeader/>
<div v-if="hasLogin" id="article-create">
    <h3>发表文章</h3>
  <form id="image_form">
    <div class="form-elem">
      <span>标题图：</span>
      <input v-on:change="onFileChange" type="file" id="file" style="padding-bottom:3px;opacity: 0.5" accept="image/gif,image/jpeg"/>
    </div>
  </form>
    <form>
      <div class="form-elem">
        <span>标题：</span>
        <input v-model="title" type="text" placeholder="输入文章标题" style="width: 500px">
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
        <input v-model="tags" type="text" placeholder="输入标签，用逗号分隔" style="width: 500px">
      </div>

      <div class="form-elem">
        <span>正文：</span>
        <textarea v-model="body" placeholder="输入正文，推荐使用Markdown语法，让你的文章更有层次感" rows="15" cols="80"></textarea>
      </div>

      <div class="form-elem" style="padding-top:10px;text-align: center">
        <button v-on:click.prevent="submit" style="background-color: blue">提交</button>
      </div>
    </form>
</div>
<BlogFooter/>
</template>

<script>
import BlogHeader from "@/components/BlogHeader";
import BlogFooter from "@/components/BlogFooter";
import axios from "axios";
import authorization from "@/utils/authorization";
import {useRouter} from "vue-router";
import {onMounted, ref} from "vue";
export default {
  name: "ArticleCreate",
  components: {BlogFooter, BlogHeader},
  setup(){
    const title = ref('');
    const body = ref('');
    const categories = ref([]);
    const router = useRouter()
    const selectedCategory = ref(null);
    const tags = ref(' ');
    const avatarID = ref(null);
    const InitCategory = function (){
      axios
          .get('/api/category/')
          .then(response => categories.value=response.data)
      //默认值为1

    }
    onMounted(InitCategory);
    const submit = function (){
      // 验证一下权限
      authorization()
        .then(function (response){
          if (response[0]){
            let data = {
              title:title.value,
              body:body.value,

            };
            data.avatar_id = avatarID.value;
            // 添加分类
            if (!selectedCategory.value){
              alert('您还没选择文章分类呢！');
              return;
            }
            data.category_id = selectedCategory.value.id;
            // 标签预处理
            data.tags = tags.value
                // 逗号分割标签
              .split(/[,.，]/)
                // 剔除标签首位空格
              .map(x=>x.trim())
                // 剔除长度为0的无效标签
              .filter(x=>x.charAt(0)!=='');
            //图片id处理
            // 获取token
            const token = localStorage.getItem('access.myblog');
            console.log(data);
            // 发送请求POST
            axios
              .post('/api/article/',data,{
                headers:{Authorization: 'Bearer '+token}
              })
              .then(function (response){
                console.log("新文章提交成功!");
                alert("提交成功！");
                router.push({name:'ArticleDetail',params:{id:response.data.id}});
              })
              .catch(function (error){
                if(error.response.status===400){
                  alert('您还未填写相关内容呢，心急吃不了热豆腐！')
                }
                else if(error.response.status===403){
                  alert('很抱歉，您没有发表文章的权限,您可以尝试联络开发者获取权限')
                }
                else{
                  alert('似乎除了点问题，您可以联系开发者解决.');
                }
                console.log(error.message);
              })
          }else {
            alert("登录已过期，请重新登录哦")
            router.push({name:'Login'})
          }
        })
    };
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
    return {
      title,
      body,
      categories,
      selectedCategory,
      tags,
      avatarID,
      submit,
      onFileChange
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
  methods:{
    // 根据分类是否被选中，按钮的颜色发生变化
      // 这里可以看出 css 也是可以被 vue 绑定的，很方便
      categoryStyle(category) {
        if (this.selectedCategory !== null && category.id === this.selectedCategory.id) {
          return {
            backgroundColor: 'darkgreen',
          }
        }
        return {
          backgroundColor: 'lightgrey',
          color: 'black',
        }
      },
      // 选取分类的方法
      chooseCategory(category) {
        // 如果点击已选取的分类，则将 selectedCategory 置空
        if (this.selectedCategory !== null && this.selectedCategory.id === category.id) {
          this.selectedCategory = null
        }
        // 如果没选中当前分类，则选中它
        else {
          this.selectedCategory = category;
        }
      },
  }
}
</script>

<style scoped>
  .category-btn {
    width: auto;
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