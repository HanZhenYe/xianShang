var res_id = location.href.split('/')[5]

$(function(){
    $.ajax({
        url: HOU_PATH + '/res/',
        type: 'get',
        data: {'res_type': 'cour', 'res_id': res_id},
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        dataType: 'json',
        success: function(data){
            if(data.code == 200){
                if (data.data.if_login){
                    html = '<li><a href="javascript:quit();"><span class="glyphicon glyphicon-log-out"></span> 退出</a></li>'
                    $('#user-state').append(html)
                }else{
                    html = '<li><a href="javascript:login();"><span class="glyphicon glyphicon-log-in"></span> 登陆</a></li>'
                    $('#user-state').append(html)
                }
                cour = data.data
                $('#cour-title').text(cour.title)
                $('#cour-synopsys').text(cour.synopsys)
                $('#cour-collection').text(cour.collection)
                $('#cour-name').text(cour.name)
                if (cour.shou == 0)
                    $('#shou').append('<span id="k" class="glyphicon glyphicon-star-empty pull-right" style="font-size: 25px;"></span>')
                else
                    $('#shou').append('<span id="s" class="glyphicon glyphicon-star pull-right" style="font-size: 25px;"></span>')

                html = ''
                $.each(cour.dir, function(i, dir){
                    html += '<div class="panel panel-default ">'
                    html += '<div class="panel-heading mul-list">'+dir.mun+'</div>'
                    html += '<div class="panel-body list-kai">'
                    $.each(dir.munl, function(j, jian){
                        html += '<a href="'+jian.kel+'" class="list-group-item" target="_blank">'+jian.ke+'</a>'
                    })
                    html += '</div></div>'
                })
                $('#cour-ke').append(html)
                init()
            }else if(data.code == 10227){
                location.href = '/index'
            }
        }
    })


    $('#shou').on('click', function(){
        var s_id = $(this).find('span').attr('id')
        if(s_id == 'k'){
            $(this).find('span').attr('id', 's')
            $(this).find('span').removeClass('glyphicon-star-empty')
            $(this).find('span').addClass('glyphicon-star')
            shou('s')
        }else{
            $(this).find('span').attr('id', 'k')
            $(this).find('span').removeClass('glyphicon-star')
            $(this).find('span').addClass('glyphicon-star-empty')
            shou('k')
        }
    })
})

// 初始化
function init(){
     // 隐藏全部元素
     $('.list-kai').hide()

    // 隐藏与显示的切换
    $(".mul-list").on('click', function(){
        $(this).next().slideToggle()
    })
}

// 收藏
function shou(st){
    $.ajax({
        url: HOU_PATH + '/res/shou',
        type: 'post',
        data: {'st': st, 'res_id': res_id, 'res_type': 'cou'},
        dataType: 'json',
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                console.log('操作成功')
            }else if(data.code == 10106){
                alert('请先登陆')
                location.href = data.data
            }else{
                    alert(data.data)
             }
        }
    })

}


