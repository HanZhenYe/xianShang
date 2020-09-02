
var res_id = location.href.split('/')[5]
var DQ = 0

$(function(){
    // 获取系列数据
    $.ajax({
        url: HOU_PATH + '/res/admin',
        type: 'get',
        data: {'res_id': res_id, 'res_type': 'res'},
        dataType: 'json',
        headers: {
                'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                res = data.data
                $('#occ-img').attr('src', HOU_PATH + '/media/' + res.cover)
                $('#occ-title').val(res.title)
                $('#occ-synopsys').val(res.synopsys)
                switch(res.audit){
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
                var res_gong = $('#occ-gong input')
                if(res.overt){
                    $(res_gong[1]).prop('checked', 'true')
                    $(res_gong[0]).prop('checked', 'false')
                }else{
                    $(res_gong[0]).prop('checked', 'false')
                    $(res_gong[1]).prop('checked', 'true')
                }
                $('#res-link input').val(res.link)
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

    // 删除资源
    $("#delete-res").on('click', function(){
        var occ_str = prompt('下方输入“确定”删除该资源')
        if(occ_str == '确定'){

            $.ajax({
                url: HOU_PATH + '/res/admin',
                type:'delete',
                data: {'res_type': 'res', 'res_id': res_id},
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
    var link = $('#res-link input').val()
    if (link == '')return alert('链接地址不能为空')

    formData.append('res_type', 'res')
    formData.append('res_id', res_id)
    formData.append('title', title)
    formData.append('synopsys', synopsys)
    formData.append('overt', overt)
    formData.append('link', link)
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
            data: {'res_type': 'res','type_id': res_id, 'title': title},
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
