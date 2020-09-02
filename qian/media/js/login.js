
$(function(){
    // 完成图片验证
    $('#img-yan').on('click', function(){
        var qq = $('#qq').val()
        var code = $('#img-yan1').val()
        if(code.length == 4){
            img_yan2()
            $.ajax({
            url: HOU_PATH+'/user/img/yan',
            type: 'post',
            data: {'qq': qq, 'code': code},
            dataType: 'json',
            success: function(data){
                $('#img-yan2').button('reset')
                if(data.code == 200){
                    alert(data.data)
                    $('#myModal').modal('hide')
                    $('#tai').button('loading')
                    $('#shu-yan').removeAttr('readonly')
                    var i = 60
                    $('#img-huo').text(60+'秒后再获取')
                    var timeID = setInterval(function(){
                        $('#img-huo').text(--i+'秒后再获取')
                        if (i == 0){
                            clearInterval(timeID)
                            $('#img-huo').text('获得验证码')
                            $('#tai').button('reset')
                        }
                    }, 1000)
                    $('#img-yan').text('验证')
                }else{
                    alert(data.error)
                    $('#img-yan').text('验证')
                }
            }
        })
        }else{
            alert('验证码错误')
        }
    })

    // 显示图片验证框前校验
    $('#img-huo').on('click', function(){
        var qq = $('#qq').val()
        if (qq == ''){
            alert('QQ号不能为空')
        }else{
            if(isNaN(Number(qq))?true:false){
                alert('QQ格式不正确')
            }else{
                 img_yan()
                $('#tai').click()
            }
        }
    })

    // 更换验证码图片
    $('#img-tu').on('click', function(){
        img_yan()
    })

    // 登陆
    $('#btn-login').on('click', function(){
        var qq = $('#qq').val()
        var code = $('#shu-yan').val()
        var zt = 0
        if($('#zhuang-tai').prop('checked')){
            zt = 1
        }else{
            zt = 0
        }
        if (qq == ''){
            alert('QQ号不能为空')
        }else{
            if(isNaN(Number(qq))?true:false){
                alert('QQ号格式不正确')
            }else{
                if(code == ''){
                    alert('验证码不能为空')
                }else{
                    if(code.length == 6){

                        $.ajax({
                            url: HOU_PATH+"/user/login",
                            type: 'post',
                            data: {'qq': qq, 'code': code, 'zt': zt},
                            dataType: 'json',
                            success: function(data){
                                if(data.code == 200){
                                    localStorage.setItem('token', data.data)
                                    location.href = QIAN_PATH+'/user'
                                }else{
                                    alert(data.error)
                                }
                            }
                        })
                    }else{
                        alert('验证码错误')
                    }
                }
            }
        }
    })
})

// 获取图片验证图
function img_yan(){
    var qq = $('#qq').val()
    $.ajax({
        url: HOU_PATH+'/user/yan',
        type: 'get',
        data: 'qq='+qq,
        dataType: 'json',
        success: function(data){
            if(data.code ==200){
                $('#img-tu>img').attr('src', HOU_PATH+'/media/yan/'+data.img_path)
            }else{
                alert(data.error)
            }
        }
    })
}

// 图片验证码提交按钮
function img_yan2(){
    $('#img-yan2').button('loading')
    $('#img-yan').text('')
}
