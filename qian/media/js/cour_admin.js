
var res_id = location.href.split('/')[5]
var DQ = 0

$(function(){
    // 获取系列数据
    $.ajax({
        url: HOU_PATH + '/res/admin',
        type: 'get',
        data: {'res_id': res_id, 'res_type': 'cour'},
        dataType: 'json',
        headers: {
                'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                cour = data.data
                $('#occ-img').attr('src', HOU_PATH + '/media/' + cour.cover)
                $('#occ-title').val(cour.title)
                $('#occ-synopsys').val(cour.synopsys)
                switch(cour.audit){
                    case '未':
                        html = '<span id="occ-zhuang" class="text-muted" style="font-size: 20px;">未审核</span>'
                        html += '<a class="btn btn-warning pull-right" href="javascript:examine();">申请审核</a>'
                        break
                    case '审':
                        html = '<span id="occ-zhuang" class="text-primary" style="font-size: 20px;">审核中</span>'
                        html += '<a class="btn btn-warning pull-right" disabled="disabled">申请审核</a>'
                        break
                    case '通':
                        html = '<span id="occ-zhuang" class="text-success" style="font-size: 20px;">审核通过</span>'
                        html += '<a class="btn btn-warning pull-right" disabled="disabled">申请审核</a>'
                        break
                    case '不':
                        html = '<span id="occ-zhuang" class="text-danger" style="font-size: 20px;">审核未通过</span>'
                        html += '<a class="btn btn-warning pull-right" disabled="disabled">申请审核</a>'
                        break
                }
                $('#occ-zhuang-fu').append(html)
                var occ_gong = $('#occ-gong input')
                if(cour.overt){
                    $(occ_gong[1]).prop('checked', 'true')
                    $(occ_gong[0]).prop('checked', 'false')
                }else{
                    $(occ_gong[0]).prop('checked', 'false')
                    $(occ_gong[1]).prop('checked', 'true')
                }

                html = ''
                $.each(cour.dir, function(i, dir){
                    html += '<div id="mu-'+i+'" class="col-md-12">'
                    html += '<div class="panel panel-default">'
                    html += '<div class="panel-heading bao-han">'
                    html += '<div class="col-lg-4">'
                    html += '<input type="text" class="form-control"'
                    html += ' placeholder="请输入目录名称" value="'+dir.mun+'" maxlength="30">'
                    html += '</div>'
                    html += '<a class="btn btn-danger pull-right cour-a1" href="javascript:delete_mu('+i+');">删除</a>'
                    html += '<a class="btn btn-success pull-right cour-a2" href="javascript:create_jian('+i+');" >添加课件</a>'
                    html += '</div>'
                    html += '<div class="panel-body">'
                    html += '<ul class="list-group bao-li">'
                    $.each(dir.munl, function(j, ke){
                        html += '<li id="mu-'+i+'-'+j+'" class="list-group-item">'
                        html += '<div class="col-lg-4">'
                        html += '<input type="text" class="form-control" '
                        html += 'placeholder="请输入课件名" value="'+ke.ke+'" maxlength="30">'
                        html += '</div>'
                        html += '<div class="col-lg-4">'
                        html += '<input type="text" class="form-control" '
                        html += 'placeholder="请输入课件链接" value="'+ke.kel+'" maxlength="200">'
                        html += '</div>'
                        html += '<a class="btn btn-danger pull-right" href="javascript:delete_jian(0, 0);">删除</a>'
                        html += ' </li>'
                    })
                    html += '</ul></div></div></div>'
                })
                $('#cour-ke').append(html)
            }else if(data.code == 10106){
                location.href = data.data
            }else{
                alert(data.error)
                location.href = QIAN_PATH + '/index'
            }
        }
    })

    // 提交修改之头像格式检测
    $('#btn-submit').on('click', function(){
        if(!confirm("是否提交修改"))return false
        var fileData = document.getElementById('fen-img1').files[0]
        if(fileData == undefined) user_data(fileData)
        else{
            var img_name = fileData.name
            var file_type_list = img_name.split('.')
            file_type = file_type_list[file_type_list.length-1]
            _file_tyoe = ['jpg', 'jpeg', 'gif', 'png']
            var kai = false
            $.each(_file_tyoe, function(i, types){
                if (file_type == types) kai = true
            })
            if(kai){
                // 检测合格，可上传文件
                user_data(fileData)
            }else {
                alert('上传的图片格式不正确, 当请只支持(jpg, jpeg, gif, png)类型')
                return false
            }
        }
    })

    // 头像更改
    $('#fen-img1').remove()
    $('#tou-fu').append('<input type="file" id="fen-img1" style="display:none" >')
    $('#fen-img1').on('change', function(){
        var img_src = URL.createObjectURL($(this)[0].files[0]);
        document.getElementById("occ-img").src=img_src;
        URL.revokeObjectURL(img_src);
    })

    // 删除课程
    $("#delete-res").on('click', function(){
        var occ_str = prompt('下方输入“确定”删除该课程')
        if(occ_str == '确定'){

            $.ajax({
                url: HOU_PATH + '/res/admin',
                type:'delete',
                data: {'res_type': 'cour', 'res_id': res_id},
                dataType: 'json',
                headers: {
                'authorization': window.localStorage.getItem('token')
                },
                success: function(data){
                    if(data.code == 200){
                        location.href = '/user'
                    }else if (data.code == 10106){
                        location.href = data.data
                    }else{
                        alert(data.error)
                    }
                }
            })
        }else if(occ_str == null){
            console.log('删除取消')
        }else{
            alert('输入错误，删除失败')
        }
    })
})

// 上传信息
function user_data(fileData){
    var formData = new FormData()
    var title = $('#occ-title').val()
    if (title == '')return alert('标题不能为空')
    var synopsys  = $('#occ-synopsys').val()
    if(synopsys == '')return alert('简介不能为空')
    var overts = $('#occ-gong input')[0]
    var overt = $(overts).prop('checked')
    var dir = mu_zhuan()
    console.log(dir)

    formData.append('res_type', 'cour')
    formData.append('res_id', res_id)
    formData.append('title', title)
    formData.append('synopsys', synopsys)
    formData.append('overt', overt)
    formData.append('dir', dir)
    formData.append('myFile', fileData)

    $.ajax({
        url: HOU_PATH + '/res/update',
        type: 'post',
        data: formData,
        dataType: 'json',
        processData : false,
        contentType : false,
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                alert(data.data)
                location.reload(true)
            }else if(data.code == 10106){
                location.href = data.data
            }else{
                alert(data.error)
            }
        }
    })
}

// 目录转换
function mu_zhuan(){
    var mu_div = $('#cour-ke>div')
    var mu_lie = '['
    var mu_name
    var ke_list
    var ke_name
    var ke_lian
    $.each(mu_div, function(i, div){
        mu_name  = $(div).find('div>div>div>input').val()
        if(i == 0) mu_lie += '{'
        if(mu_name){
            if(i != 0) mu_lie += ',{'
            mu_name = mu_name.replace(/'/g,' ')
            mu_name = mu_name.replace(/"/g,' ')
            mu_lie += '"mun":"'+mu_name+'","munl":['
            ke_list = $('#mu-'+i+' ul>li')
            $.each(ke_list, function(j, ke){
                ke_name = $(ke).find('input')[0].value
                if(ke_name){
                    if(j == 0) mu_lie += '{'
                    else mu_lie+= ',{'
                    ke_name = ke_name.replace(/\'/g,' ')
                    ke_name = ke_name.replace(/\"/g,' ')
                    ke_lian = $(ke).find('input')[1].value
                    ke_lian = ke_lian.replace(/\'/g,' ')
                    ke_lian = ke_lian.replace(/\"/g,' ')
                    mu_lie += '"ke":"'+ke_name+'","kel":"'+ke_lian+'"}'
                }
            })
            mu_lie += ']}'
        }
    })
    mu_lie += ']'
    return mu_lie
}

// 添加课程目录
function tian(){
    DQ = $('#cour-ke>div').length
    html = '<div id="mu-'+DQ+'" class="col-md-12">'
    html += '<div class="panel panel-default">'
    html += '<div class="panel-heading bao-han">'
    html += '<div class="col-lg-4">'
    html += '<input type="text" class="form-control" placeholder="请输入目录名称" maxlength="30"> '
    html += '</div>'
    html += '<a class="btn btn-danger pull-right cour-a1"  href="javascript:delete_mu('+DQ+');">删除</a>'
    html += '<a class="btn btn-success pull-right cour-a2" href="javascript:create_jian('+DQ+');">添加课程</a>'
    html += '</div>'
    html += '<div class="panel-body">'
    html += '<ul class="list-group bao-li">'
    html += '</ul></div></div></div>'
    $('#cour-ke').append(html)
}

// 删除目录
function delete_mu(i){
    if(confirm("你确定要删除么?")){
        $('#mu-'+i).remove()
        var jies = $('#cour-ke>div')
        var delete_a1 = $('.cour-a1')
        var delete_a2 = $('.cour-a2')
        $.each(jies, function(i, jie){
            $(jie).attr('id', 'mu-'+i)
            $(delete_a1[i]).attr('href', 'javascript:delete_mu('+i+');')
            $(delete_a2[i]).attr('href', 'javascript:create_jian('+i+');')
        })
    }
}

// 添加课件
function create_jian(i){
    var ke = $('#mu-'+i+'>div>div>div>input').val()
    if(ke){
        var j = $('#mu-'+i+' ul>li').length
        html = '<li id="mu-'+i+'-'+j+'" class="list-group-item">'
        html += '<div class="col-lg-4">'
        html += '<input type="text" class="form-control" placeholder="请输入课件名" maxlength="30">'
        html += '</div>'
        html += ' <div class="col-lg-4">'
        html += '<input type="text" class="form-control" placeholder="请输入课件链接" maxlength="200">'
        html += ' </div>'
        html += '<a class="btn btn-danger pull-right" href="javascript:delete_jian('+i+', '+j+');">删除</a>'
        html += '</li>'
        $('#mu-'+i+" ul").append(html)
    }else{
        alert('目录名不能为空')
    }
}

// 删除课件
function delete_jian(i, j){
    if(confirm("你确定要删除么?")){
        $('#mu-'+i+'-'+j).remove()
        var li_list = $('#mu-'+i+' ul>li')
        $.each(li_list, function(k, li){
            $(li).attr('id', 'mu-'+i+'-'+k)
            $(li).find('a').attr('href', 'javascript:delete_jian('+i+', '+k+');')
        })
    }
}

// 审核
function examine(){
    if(confirm('请先保存修改后，在申请审核，是否申请审核')){
        var title = $('#occ-title').val()
        if (title == ''){
            alert('标题不能为空')
            return false
        }
        $.ajax({
            url: HOU_PATH + '/res/apply/examine',
            type: 'post',
            data: {'res_type': 'cou','type_id': res_id, 'title': title},
            dataType: 'json',
            headers: {
                    'authorization': window.localStorage.getItem('token')
            },
            success: function(data){
                if(data.code == 200){
                    alert('审核申请成功')
                    location.href = '/user'
                }else{
                    alert(data.error)
                }
            }
        })
    }
}
