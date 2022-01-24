export default function imageIfExists(article){
    if(article.avatar){
        return article.avatar.content
    }
}