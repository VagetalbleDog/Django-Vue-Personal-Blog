<template>
  <br>
  <p>已有 {{ comments.length }} 条评论</p>
  <hr>
  <!-- 渲染所有评论内容 -->
  <div
       v-for="comment in comments"
       :key="comment.id"
       >
    <div class="comments">
      <div>
        <span class="username">
          {{ comment.author.username }}
        </span>
        于
        <span class="created">
          {{ formatted_time(comment.created) }}
        </span>
        <span>
          对
          <span v-if="comment.parent_comments">
          <span class="parent">
            {{ comment.parent_comments.author.username }} 的评论——
          </span>
          <span class="parent" style="color: darkgreen">
            “{{ comment.parent_comments.body }}”
          </span>
          </span>
        <span v-else class="parent">
          &nbsp;作者
        </span>
        评论：
       </span>
      </div>
      <div class="content">
        {{ comment.body }}
      </div>
      <div>
        <button class="btn btn-primary" @click="replyTo(comment)">回复</button>
      </div>
    </div>
    <hr>
  </div>
  <div style="text-align: center">
  <h3>发布评论</h3>
<!--  评论文本输入空间-->
  <textarea v-model="message" :placeholder="placeholder" name="comment" id="comment-area" cols="80" rows="2"></textarea>
  <div>
    <button @click="submit" class="btn btn-primary">发布</button>
  </div>
   </div>
</template>

<script>
import authorization from "@/utils/authorization";
import axios from "axios";

export default {
  name: "Comments",
  props:{ article : Object },
  data:function (){
    return{
      comments:[],
      message:'',
      placeholder:'作者写的这么辛苦，来说点话鼓励一下呀...',
      parentID:null
    }
  },
  // 监听article对象，实时更新评论
  watch:{
    article(){
      this.comments = this.article !== null ? this.article.comments:[]
    }
  },
  methods:{
    //提交评论
    submit(){
      const that = this;
      authorization()
      .then(function (response){
        if(response[0]){
          const data={
            body:that.message,
            article_id:that.article.id,
            parent_comments_id:that.parentID,
          };
          console.log(data);
          axios
          .post('/api/comment/', data,{
            headers:{Authorization:'Bearer '+localStorage.getItem('access.myblog')}
              })
          .then(function (response){
            that.comments.unshift(response.data);
            //将message置空
            that.message = '';
            alert('评论成功！')
          })
          .catch(function (error){
            console.log(error.message);
            alert('似乎遇到了一些问题，众所周知，90%的问题可以通过刷新和重启解决，当然，您也可以联络开发人员');
          })
        }
        else {
          alert('请登录后再进行操作！');
          that.$router.push({name:'Login'})
        }
      })
    },
    //二级评论方法
    replyTo(comment){
      this.parentID = comment.id;
      this.placeholder = '对' +comment.author.username + '回复:'
    },
    //修改日期显示格式
    formatted_time:function (iso_date_string){
            const date = new Date(iso_date_string);
            return date.toLocaleDateString() + ' '+date.toLocaleTimeString()
    },
  }
}
</script>

<style scoped>
  button {
    cursor: pointer;
    border: none;
    outline: none;
    color: whitesmoke;
    border-radius: 5px;
  }
  .comments {
    padding-top: 10px;
  }
  .username {
    font-weight: bold;
    color: darkorange;
  }
  .created {
    font-weight: bold;
    color: darkblue;
  }
  .parent {
    font-weight: bold;
    color: orangered;
  }
  .content {
    font-size: large;
    padding: 15px;
  }
</style>