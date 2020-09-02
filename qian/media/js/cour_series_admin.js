var res_id = location.href.split('/')[5]
var DQ = 0

$(function(){
    // 获取系列数据
    $.ajax({
        url: HOU_PATH + '/res/admin',
        type: 'get',
        data: {'res_id': res_id, 'res_type': 'cour_series'},
        dataType: 'json',
        headers: {
                'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                occ = data.data
                $('#occ-img').attr('src', HOU_PATH + '/media/' + occ.cover)
                $('#occ-title').val(occ.title)
                $('#occ-synopsys').val(occ.synopsys)
                switch(occ.audit){
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
                if(occ.overt){
                    $(occ_gong[1]).prop('checked', 'true')
                    $(occ_gong[0]).prop('checked', 'false')
                }else{
                    $(occ_gong[0]).prop('checked', 'false')
                    $(occ_gong[1]).prop('checked', 'true')
                }
                cour_list = data.data.cour_list
                html  = ''
                $.each(cour_list, function(j, cour){
                    html += ' <li id="jd-0-'+j+'">'
                    html += '<input type="hidden" value="'+cour.id+'">'
                    html += '<div class="panel panel-default">'
                    html += '<div class="panel-heading">'+cour.title+'</div>'
                    html += '<div class="panel-body ziyuan-img">'
                    html += '<a href="'+QIAN_PATH+'/res/cou/'+cour.id+'">'
                    html += '<img src="'+HOU_PATH+'/media/'+cour.cover+'">'
                    html += '</a></div>'
                    html += '<div class="panel-footer">'
                    html += '<a class="btn btn-danger pull-right" href="javascript:delete_cour(0,'+j+');">删除</a>'
                    html += '</div></div></li>'
                })
                $('#jd-0 ul').append(html)
            }else if(data.code == 10106){
                location.href = data.data
            }else{
                alert(data.error)
                location.href = QIAN_PATH + '/index'
            }
        }
    })

    // 获取课程
    $('#myModal').on('show.bs.modal', function (){
        $('#myModal ul>li').remove()

        $.ajax({
            url: HOU_PATH+'/res/cour',
            type: 'get',
            dataType: 'json',
            headers: {
                'authorization': window.localStorage.getItem('token')
            },
            success: function(data){
                if(data.code == 200){
                    var cour_list = data.data
                    html = ''
                    $.each(cour_list, function(i, cour){
                        var cover = "'"+cour.cover+"'"
                        var title = "'"+cour.title+"'"
                        html += '<li>'
                        html += '<div class="panel panel-default">'
                        html += '<div class="panel-heading">'
                        html += cour.title
                        html += '</div>'
                        html += '<div class="panel-body ziyuan-img">'
                        html += '<img src="'+HOU_PATH+'/media/'+cour.cover+'">'
                        html += '</div>'
                        html += '<div class="panel-footer">'
                        html += '<a class="btn btn-success pull-right"'
                        html += 'href="javascript:tian_cour('+cour.id+','+cover+', '+title+');">添加</a>'
                        html += '</div> </div></li>'
                    })
                    $('#myModal ul').append(html)
                }else if(data.code == 10106){
                    location.href = data.data
                }else{
                    alert(data.error)
                }
            }
        })
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

    // 删除系列
    $("#delete-res").on('click', function(){
        var occ_str = prompt('下方输入“确定”删除该系列')
        if(occ_str == '确定'){

            $.ajax({
                url: HOU_PATH + '/res/admin',
                type:'delete',
                data: {'res_type': 'cour_series', 'res_id': res_id},
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

// 显示模态框
function show_mo(i){
    DQ = i
    $('#myModal').modal('show')
}

// 添加课程
function tian_cour(id, img_href, title){
    var jd_k = $('#jd-'+DQ+' ul>li').length
    $('#myModal').modal('hide')
    html = '<li id="jd-'+DQ+'-'+jd_k+'">'
    html += '<input type="hidden" value="'+id+'">'
    html += '<div class="panel panel-default">'
    html += '<div class="panel-heading">'
    html += title
    html += '</div>'
    html += '<div class="panel-body ziyuan-img">'
    html += ' <a href="'+QIAN_PATH+'/res/cou/'+id+'">'
    html += '<img src="'+HOU_PATH+'/media/'+img_href+'">'
    html += '</a>'
    html += '</div>'
    html += '<div class="panel-footer">'
    html += '<a class="btn btn-danger pull-right" href="javascript:delete_cour('+DQ+', '+jd_k+');">删除</a>'
    html += '</div></div></li>'
    $('#jd-'+DQ+' ul').append(html)
}

// 删除课程
function delete_cour(i, j){
    if(confirm("你确定要删除么?")){
        $('#jd-'+i+'-'+j).remove()
        var li_list = $('#jd-'+i+' ul>li')
        $.each(li_list, function(j, li){
            $(li).attr('id', 'jd-'+i+'-'+j)
            $(li).find('.panel-footer>a').attr('href', 'javascript:delete_cour('+i+','+j+');')
        })
    }
}

// 上传信息
function user_data(fileData){
    var formData = new FormData()
    var title = $('#occ-title').val()
    if (title == '')return alert('标题不能为空')
    var synopsys  = $('#occ-synopsys').val()
    if(synopsys == '')return alert('简介不能为空')
    var overts = $('#occ-gong input')[0]
    var overt = $(overts).prop('checked')
    var course_list = get_route()

    formData.append('res_type', 'cour_series')
    formData.append('res_id', res_id)
    formData.append('title', title)
    formData.append('synopsys', synopsys)
    formData.append('overt', overt)
    formData.append('course_list', course_list)
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

// 获取路线
function get_route(){
    var cour_list = $('#jd-0 ul>li')
    var id_list = ''
    $.each(cour_list, function(i, cour){
        cour_id = $(cour).children('input').val()
        id_list += cour_id + ','
    })
    return id_list
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
            data: {'res_type': 'cos','type_id': res_id, 'title': title},
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

