
var res_id = location.href.split('/')[5]
$(function(){
    // 初始化
    $.ajax({
        url: HOU_PATH + '/res/',
        type: 'get',
        data: {'res_type': 'occ', 'res_id': res_id},
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

                occ = data.data
                $('#occ-title').text(occ.title)
                $('#occ-synopsys').text(occ.synopsys)
                $('#occ-name').text(occ.name)
                $('#occ-collection').text(occ.collection)
                if (occ.shou == 0)
                    $('#shou').append('<span id="k" class="glyphicon glyphicon-star-empty pull-right" style="font-size: 25px;"></span>')
                else
                    $('#shou').append('<span id="s" class="glyphicon glyphicon-star pull-right" style="font-size: 25px;"></span>')

                html = ''
                $.each(occ.route, function(i, cours){
                    html += '<div class="col-md-12">'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+cours.jie+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body">'
                    html += '<ul class="ul-ziyuan">'
                    $.each(cours.cour_list, function(j, cour){
                        html += '<li>'
                        html += '<a href="'+QIAN_PATH+'/res/cou/'+cour.id+'">'
                        html += '<div class="panel panel-default">'
                        html += '<div class="panel-heading">'+cour.title+'</div>'
                        html += '<div class="panel-body ziyuan-img">'
                        html += '<img src="'+HOU_PATH+'/media/'+cour.cover+'">'
                        html += ' </div>'
                        html += '<div class="panel-footer">'
                        html += '<div>'
                        html += '<span class="glyphicon glyphicon-star"></span>'+cour.collection+''
                        html += '</div>'
                        html += '<div>'
                        html += '<span class="glyphicon glyphicon-user"></span> '+occ.name+''
                        html += '</div></div></div></a> </li>  '
                    })
                    html += '</ul></div></div></div>'
                })
                $('#body').append(html)
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

// 收藏
function shou(st){
    $.ajax({
        url: HOU_PATH + '/res/shou',
        type: 'post',
        data: {'st': st, 'res_id': res_id, 'res_type': 'occ'},
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
