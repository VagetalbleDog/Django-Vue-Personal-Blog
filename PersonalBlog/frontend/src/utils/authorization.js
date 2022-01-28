//   用于处理用户登录和权限认证


import axios from "axios";
//async声明异步方法
async function authorization(){
    const storage = localStorage;
    let username = storage.getItem('username.myblog');

     // 过期时间
    const expiredTime = Number(storage.getItem('expiredTime.myblog'));
    // 当前时间
    const current = (new Date()).getTime();
    // 刷新令牌
    const refreshToken = storage.getItem('refresh.myblog');

    // 初始token还没过期
    if(expiredTime>current){
      storage.setItem('login.myblog',"1")
      console.log('JWT令牌验证成功!');
      console.log("当前用户：",username);
    }
    // 初始token过期
    else if(refreshToken!==null){
        try{
            let response = await axios.post('/api/token/refresh/',{refresh:refreshToken}); //；这里如果没有成功，response对象将会获得await的返回值，rejected

            const nextExpiredTime = Date.parse(response.headers.date)+60000;
            storage.setItem('access.myblog',response.data.access);
            storage.setItem('expiredTime.myblog',nextExpiredTime);
            storage.removeItem('refresh.myblog');

            storage.setItem('login.myblog',"1")
            console.log('令牌已刷新!');
            console.log("当前用户：",username)
        }
        catch (error){
            storage.clear();
            storage.setItem('login.myblog',"0")

            console.log('令牌出错，错误信息：',error.message)
        }
    }
    //无有效Token
    else {
        storage.clear();
        storage.setItem('login.myblog',"0")
        console.log("无有效Token")
    }
    return [username]
}

export default authorization;