
$(function(){
    // 加载用户信息
    $.ajax({
        url: HOU_PATH + '/user/geren',
        type: 'get',
        dataType: 'json',
        headers: {
                'authorization': window.localStorage.getItem('token')
            },
        success: function(data){
           if(data.code == 200){
               user = data.data
                html = '<tr>'
                html += '<td>QQ：'+user.qq+'</td>'
                html += '<td>我的职业：'+user.my_occ+'</td>'
                html += '<td>收藏的职业：'+user.coll_occ+'</td>'
                html += '</tr>'
                html += '<tr>'
                html += '<td class="user-xin-list">姓名：'+user.name+'</td>'
                html += '<td>我的系列：'+user.my_cour_series+'</td>'
                html += '<td>收藏的系列：'+user.coll_cour_series+'</td>'
                html += ' </tr>'
                html += '<tr>'
                html += '<td class="user-xin-list">性别：'+user.age+'</td>'
                html += '<td>我的课程：'+user.my_cour+'</td>'
                html += ' <td>收藏的课程：'+user.coll_cour+'</td>'
                html += '</tr>'
                html += ' <tr>'
                html += '<td>年龄：'+user.nian+'</td>'
                html += '<td>我的资源：'+user.my_res+'</td>'
                html += '<td>收藏的资源：'+user.coll_res+'</td>'
                html += '</tr>'
                html += '<tr>'
                html += '<td class="user-xin-list">生日：'+user.birth_date+'</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '</tr>'
                $('#tbody').html(html)
                $('#portrait').attr('src', HOU_PATH+'/media/'+user.portrait)
           }else if(data.code == 10106){
                location.href = data.data
           }else{
               alert(data.error)
           }
        }
    })

    //  获取用户资源
    $.ajax({
        url: HOU_PATH + '/res/user/res',
        type: 'get',
        dataType: 'json',
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                data = data.data
                occs = data.occ
                cour_seriess = data.cour_series
                cours = data.cour
                ress = data.res
                coll_occ = data.coll_occ
                coll_course = data.coll_course
                coll_cour = data.coll_cour
                coll_res = data.coll_res

                // 职业信息
                html = ''
                $.each(occs, function(i, occ){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+occ.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+occ.synopsys+'</div>'
                    html += '<div class="panel-footer">'
                    html += '<a class="btn btn-success" href="'+QIAN_PATH+'/res/occ/'+occ.id+'">进入</a>'
                    html += '<a class="btn btn-info pull-right" href="'+QIAN_PATH+'/occ/admin/'+occ.id+'">管理</a>'
                    html += '</div></div></li>'
                })
                $('#my_occ>ul').append(html)

                // 课程系列信息
                html = ''
                $.each(cour_seriess, function(i, cour_series){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+cour_series.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+cour_series.synopsys+'</div>'
                    html += '<div class="panel-footer">'
                    html += '<a class="btn btn-success" href="'+QIAN_PATH+'/res/cos/'+cour_series.id+'">进入</a>'
                    html += '<a class="btn btn-info pull-right" href="'+QIAN_PATH+'/courseries/admin/'+cour_series.id+'">管理</a>'
                    html += '</div></div></li>'
                })
                $('#my_cour_series>ul').append(html)

                // 课程信息
                html = ''
                $.each(cours, function(i, cour){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+cour.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+cour.synopsys+'</div>'
                    html += '<div class="panel-footer">'
                    html += '<a class="btn btn-success" href="'+QIAN_PATH+'/res/cou/'+cour.id+'">进入</a>'
                    html += '<a class="btn btn-info pull-right" href="'+QIAN_PATH+'/cour/admin/'+cour.id+'">管理</a>'
                    html += '</div></div></li>'
                })
                $('#my_cour>ul').append(html)

                // 资源信息
                html = ''
                $.each(ress, function(i, res){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+res.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+res.synopsys+'</div>'
                    html += '<div class="panel-footer">'
                    html += '<a class="btn btn-success" href="'+QIAN_PATH+'/res/res/'+res.id+'">进入</a>'
                    html += '<a class="btn btn-info pull-right" href="'+QIAN_PATH+'/res/admin/'+res.id+'">管理</a>'
                    html += '</div></div></li>'
                })
                $('#my_reso>ul').append(html)

                 // 收藏职业信息
                 html = ''
                $.each(coll_occ, function(i, occ){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+occ.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+occ.synopsys+'</div>'
                    html += '<div class="panel-footer han">'
                    html += '<a class="btn btn-success pull-right" href="'+QIAN_PATH+'/res/occ/'+occ.id+'">进入</a>'
                    html += '</div></div></li>'
                })
                $('#coll_occ>ul').append(html)

                // 收藏的课程系列信息
                html = ''
                $.each(coll_course, function(i, cour_series){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+cour_series.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+cour_series.synopsys+'</div>'
                    html += '<div class="panel-footer han">'
                    html += '<a class="btn btn-success pull-right" href="'+QIAN_PATH+'/res/cos/'+cour_series.id+'">进入</a>'
                    html += '</div></div></li>'
                })
                $('#coll_cour_series>ul').append(html)

                 // 收藏的课程信息
                 html = ''
                $.each(coll_cour, function(i, cour){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+cour.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+cour.synopsys+'</div>'
                    html += '<div class="panel-footer han">'
                    html += '<a class="btn btn-success pull-right" href="'+QIAN_PATH+'/res/cou/'+cour.id+'">进入</a>'
                    html += '</div></div></li>'
                })
                $('#coll_cour>ul').append(html)

                // 资源信息
                html = ''
                $.each(coll_res, function(i, res){
                    html += '<li>'
                    html += '<div class="panel panel-primary">'
                    html += '<div class="panel-heading">'
                    html += '<h3 class="panel-title">'+res.title+'</h3>'
                    html += '</div>'
                    html += '<div class="panel-body panel-du">'+res.synopsys+'</div>'
                    html += '<div class="panel-footer han">'
                    html += '<a class="btn btn-success pull-right" href="'+QIAN_PATH+'/res/res/'+res.id+'">进入</a>'
                    html += '</div></div></li>'
                })
                $('#coll_reso>ul').append(html)
            }else if(data.code == 10106){
                location.href = data.data
            }else{
                alert(data.error)
            }
        }
    })

    // 用户信息修改
    $('#user-btn-xiu').on('click', function(){
        $('#user-xin-fu>input').remove()
        $('#user-xin-fu').append('<input type="file" id="user-file" style="display: none;">')
        // 头像预览
        $('#user-file').on('change', function(){
            var img_src = URL.createObjectURL($(this)[0].files[0]);
            document.getElementById("user-img1").src=img_src;
            URL.revokeObjectURL(img_src);
        })
        $('#user-mo').modal('show')
        var xin_list  = $('.user-xin-list')
        var name = xin_list[0].innerHTML.split('：')[1]
        var age = xin_list[1].innerHTML.split('：')[1]
        var shen = xin_list[2].innerHTML.split('：')[1]
        var portrait =  $('#portrait').attr('src')
        $('.user-img>img').attr('src', portrait)
        var input_list = $('.user-xin input')
        input_list[0].value  = name
        if(age == '男'){
          $(input_list[2]).prop('checked', 'false')
          $(input_list[1]).prop('checked', 'true')
        }else{
            $(input_list[1]).prop('checked', 'false')
            $(input_list[2]).prop('checked', 'true')
        }
        $(input_list[3]).val(shen)
    })

   // 用户头像上传格式检测
    $('#user-btn').on('click', function(){
        var fileData = document.getElementById('user-file').files[0]
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

    // 创建资源
    $('#create-btn').on('click', function(){
        $('#file-tian>input').remove()
        $('#file-tian').append('<input type="file" id="res-cover" style="display: none;">')
        $('#create-res').modal('show')
        $('#res-img').attr('src', '')

        // 资源封面预览
        $('#res-cover').on('change', function(){
            var img_src = URL.createObjectURL($(this)[0].files[0]);
            document.getElementById("res-img").src=img_src;
            URL.revokeObjectURL(img_src);
        })
    })

    // 资源创建提交
    $('#create-res-btn').on('click', function(){
        var res_type = $('#select-res').val()
        var fileData = document.getElementById('res-cover').files[0]
        if(fileData == undefined){
            return alert('封面不能为空')
        }
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
               var name = $("[placeholder='请输入标题']").val()
               var synopsys = $('#create-synopsys').val()
               if(name == '')return alert('标题不能为空')
               if(synopsys == '')return  alert('简介不能为空')

               var formData = new FormData()
               formData.append('res_type', res_type)
               formData.append('name', name)
               formData.append('synopsys', synopsys)
               formData.append('myFile', fileData)

               $.ajax({
                    url: HOU_PATH+'/res/user/res',
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
            }else {
                alert('上传的图片格式不正确, 当请只支持(jpg, jpeg, gif, png)类型')
                return false
            }
        }
    })
})

//  上传用户修改后的信息
function user_data(fileData){
    var input_list = $('.user-xin input')
    var formData = new FormData()
    var name =$(input_list[0]).val()
    var age
    if($(input_list[1]).prop('checked'))age = 1
    else age = 0
    var shen = $(input_list[3]).val()

    formData.append('name', name)
    formData.append('age', age)
    formData.append('shen', shen)
    formData.append('myFile', fileData)

    $.ajax({
            url: HOU_PATH+'/user/modify',
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
                    location.reload(true)
                }else if(data.code == 10106){
                    location.href = data.data
                }else{
                    alert(data.error)
                }
            }
        })
}

