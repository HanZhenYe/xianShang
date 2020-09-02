
var cla = ''
var res_type = ''

$(function(){
    var path = location.href
    var get_res = path.split('res_type=')[1]
    if(get_res == 'occ'){
        res_type = 'occ'
    }else if(get_res == 'cos'){
        res_type = 'cos'
    }else if(get_res == 'cou'){
        res_type = 'cou'
    }else if(get_res == 'res'){
        res_type = 'res'
    }else if(!get_res){
        res_type = 'occ'
    }
    cla = 'coll'

    $.ajax({
        url: HOU_PATH + '/res/user/type',
        type: 'get',
        dataType: 'json',
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                if (data.data){
                    html = '<li><a href="javascript:quit();"><span class="glyphicon glyphicon-log-out"></span> 退出</a></li>'
                    $('#user-state').append(html)
                }else{
                    html = '<li><a href="javascript:login();"><span class="glyphicon glyphicon-log-in"></span> 登陆</a></li>'
                    $('#user-state').append(html)
                }
            }
        }
    })

    qie(1, 0)
    res(res_type, 0)
    gets_res(cla, res_type, 1)
})

// 排序方式
function qie(i, j){
    if(i){
        cla = 'coll'
        $('#newe').removeClass('active')
        $('#coll').addClass('active')
    }else{
        cla = 'newe'
        $('#coll').removeClass('active')
        $('#newe').addClass('active')
    }
    if (j)gets_res(cla, res_type, 1)
}

// 资源类型
function res(res_tyoe, i){
    html = '<span class="caret"></span>'
    res_type = res_tyoe
    var res_name = ''
    if (res_tyoe == 'occ'){
        res_name = '职业'
    }else if(res_tyoe == 'cos'){
        res_name = '系列'
    }else if(res_tyoe == 'cou'){
        res_name = '课程'
    }else{
        res_name = '资源'
    }
    $('#res').html(res_name+html)
    if(i){
        gets_res(cla, res_tyoe, 1)
    }
}

// 获取资源
function gets_res(cla_i,res_type_i, ye){
    $.ajax({
        url: HOU_PATH + '/res/area',
        type: 'get',
        data: {'cla': cla_i, 'res_type': res_type_i, 'ye': ye},
        dataType: 'json',
        success: function(data){
            if(data.code == 200){
                res_list = data.data
                $('.ul-ziyuan>li').remove()
                html = ''
                $.each(res_list, function(i, re){
                    html += '<li>'
                    html += '<a href="'+QIAN_PATH+'/res/'+res_type_i+'/'+re.id+'">'
                    html += '<div class="panel panel-default">'
                    html += '<div class="panel-heading">'+re.title+'</div>'
                    html += '<div class="panel-body ziyuan-img">'
                    html += '<img src="'+HOU_PATH+'/media/'+re.cover+'"> '
                    html += '</div>'
                    html += '<div class="panel-footer">'
                    html += '<div>'
                    html += '<span class="glyphicon glyphicon-star"></span> '+ re.collection
                    html += '</div> <div>'
                    html += '<span class="glyphicon glyphicon-user"></span>' + re.name
                    html += '</div></div></div></a> </li>'
                })
                $('.ul-ziyuan').append(html)

                paging = data.paging
                $('#paging>li').remove()
                if (paging.q == paging.z){
                    html = '<li class="disabled"><a href="#;">上一页</a></li>'
                }else{
                    html = '<li><a href="javascript:pagingfun('+(paging.z-1)+');">上一页</a></li>'
                }
                for (var i=paging.q; i<=paging.h; i++){
                    if(i == paging.z){
                        html += '<li class="active"><a href="#">'+i+'</a></li>'
                    }
                    else{
                        html += '<li><a href="javascript:pagingfun('+i+');">'+i+'</a></li>'
                    }
                }
                if (paging.h == paging.z){
                    html += '<li class="disabled"><a href="#">下一页</a></li>'
                }else{
                    html += '<li><a href="javascript:pagingfun('+(paging.z+1)+');">下一页</a></li>'
                }
                $('#paging').append(html)
            }else{
                location.href = '/res/area'
            }
        }
    })
}

// 分页点击
function pagingfun(z){
    gets_res(cla, res_type, z)
}
