import axios from "axios";
import {onMounted,watch} from "vue";

export default function getArticleData(info,route){
    const getData = async () => {
        let url = '/api/article';
        let params = new URLSearchParams();
        params.append_if_exists('page',route.query.page);
        params.append_if_exists('search',route.query.search);
        const paramsString = params.toString();
        if(paramsString.charAt(0)!==''){
            url += '/?'+paramsString
        }
        // 确保获取数据后再进行后续操作
        const response = await axios.get(url);
        info.value = response.data;
    };
    onMounted(getData);
    watch(route,getData);// route是监听对象，get_article_data是回调函数
}