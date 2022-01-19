//   用于处理用户登录和权限认证


import axios from "axios";
//异步方法
async function authorization(){
    const storage = localStorage;

    let hasLogin = false;
    let username = storage.getItem('username.myblog');

     // 过期时间
    const expiredTime = Number(storage.getItem('expiredTime.myblog'));
    // 当前时间
    const current = (new Date()).getTime();
    // 刷新令牌
    const refreshToken = storage.getItem('refresh.myblog');

    // 初始token还没过期
    if(expiredTime>current){
      hasLogin = true;
      console.log('JWT令牌验证成功!');
      console.log("当前用户：",username);
    }
    // 初始token过期
    else if(refreshToken!==null){
        try{
            let response = await axios.post('/api/token/refresh/',{refresh:refreshToken}); //；这里如果没有成功，response对象将会获得await的返回值，rejected

            const nextExpiredTime = Date.parse(response.headers.date)+60000*5;
            storage.setItem('access.myblog',response.data.access);
            storage.setItem('expiredTime.myblog',nextExpiredTime);
            storage.removeItem('refresh.myblog');

            hasLogin = true;
            console.log('令牌已刷新!');
            console.log("当前用户：",username)
        }
        catch (error){
            storage.clear();
            hasLogin = false;

            console.log('令牌出错，错误信息：',error.message)
        }
    }
    //无有效Token
    else {
        storage.clear();
        hasLogin = false;
        console.log("无有效Token")
    }
    return [hasLogin,username]
}

export default authorization;