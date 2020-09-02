var HOU_PATH = 'http://134.175.108.84'
var QIAN_PATH = 'http://106.53.8.216'

function login(){
    location.href = '/user/login'
}

function quit(){
    if(confirm("是否退出?")){
        localStorage.removeItem('token')
        location.reload(true)
    }
}
