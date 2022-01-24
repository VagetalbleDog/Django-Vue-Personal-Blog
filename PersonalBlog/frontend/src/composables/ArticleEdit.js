import authorization from "@/utils/authorization";
import axios from "axios";

export default function ArticleEdit(title,body,avatarID,selectedCategory,tags,article_id,router){
    const submit = ()=>{
        return Submit(title,body,avatarID,selectedCategory,tags,article_id,router)
    }
    const delete_article = ()=>{
        return DeleteArticle(article_id,router);
    }
    return{
        submit,delete_article
    }
}
function Submit(title,body,avatarID,selectedCategory,tags,article_id,router){
        authorization()
        .then(function (response){
          if (response[0]){
            let data = {
              title:title.value,
              body:body.value,
            };
            data.avatar_id = avatarID.value;
            // 添加分类
            if(selectedCategory.value){
              data.category_id = selectedCategory.value.id;
            }
            // 标签预处理
            data.tags = tags.value
                // 逗号分割标签
              .split(/[,.，]/)
                // 剔除标签首位空格
              .map(x=>x.trim())
                // 剔除长度为0的无效标签
              .filter(x=>x.charAt(0)!=='');
            // 获取token
            const token = localStorage.getItem('access.myblog');
            const url = '/api/article/'+article_id+'/';
            // 发送请求POST
            axios
              .put(url,data,{
                headers:{Authorization: 'Bearer '+token}
              })
              .then(function (response){
                console.log("文章修改成功!文章id：",article_id);
                alert("文章修改成功！");
                router.push({name:'ArticleDetail',params:{id:response.data.id}});
              })
              .catch(function (error){
                console.log(error.message);
                alert('似乎除了点问题，您可以联系开发者解决.');
              })
          }else {
            alert("登录已过期，请重新登录哦")
            router.push({name:'Login'})
          }
        })
    }
function DeleteArticle(article_id,router){
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
                      router.push({name:'MyArticle',params:{author_name: username}})
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
}