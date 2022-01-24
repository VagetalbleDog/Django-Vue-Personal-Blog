import axios from "axios";
import {onMounted,watch} from "vue";

export default function getMyArticle(info,route,author_name){
    const getData = async () => {
        let url = '/api/article';
        let params = new URLSearchParams();
        params.append_if_exists('page',route.query.page);
        const paramsString = params.toString();
        url += '/?' + '&search=' + author_name + '&' + paramsString
        // 确保获取数据后再进行后续操作
        const response = await axios.get(url);
        info.value = response.data;
    };
    onMounted(getData);
    watch(route,getData);// route是监听对象，get_article_data是回调函数
}