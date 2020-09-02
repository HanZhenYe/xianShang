
$(function(){
    $.ajax({
        url: HOU_PATH + '/res/examine',
        type: 'get',
        dataType: 'json',
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            if(data.code == 200){
                occs = data.data.occ
                coss = data.data.cos
                cous = data.data.cou
                ress = data.data.res

                html = ''
                var res_type = "'occ'"
                $.each(occs, function(i, occ){
                    html += '<tr>'
                    html += '<td>'+occ.qq+'</td>'
                    html += '<td>'+occ.title+'</td>'
                    html += '<td>'
                    html += ' <div class="btn-group">'
                    html += '<a class="btn btn-default btn-info" href="'+QIAN_PATH+'/res/occ/'+occ.type_id+'">查看</a>'
                    html += '<a class="btn btn-default btn-success" href="javascript:adopt('+res_type+','+occ.type_id+', 1);">通过</a>'
                    html += '<a class="btn btn-default btn-danger" href="javascript:adopt('+res_type+','+occ.type_id+', 0);">不通过</a>'
                    html += '</div></td></tr>'
                })
                $('#occ-shen>table>tbody').append(html)

                html = ''
                res_type = "'cos'"
                $.each(coss, function(i, cos){
                    html += '<tr>'
                    html += '<td>'+cos.qq+'</td>'
                    html += '<td>'+cos.title+'</td>'
                    html += '<td>'
                    html += ' <div class="btn-group">'
                    html += '<a class="btn btn-default btn-info" href="'+QIAN_PATH+'/res/cos/'+cos.type_id+'">查看</a>'
                    html += '<a class="btn btn-default btn-success" href="javascript:adopt('+res_type+','+cos.type_id+', 1);">通过</a>'
                    html += '<a class="btn btn-default btn-danger" href="javascript:adopt('+res_type+','+cos.type_id+', 0);">不通过</a>'
                    html += '</div></td></tr>'
                })
                $('#xi-shen>table>tbody').append(html)

                html = ''
                res_type = "'cou'"
                $.each(cous, function(i, cou){
                    html += '<tr>'
                    html += '<td>'+cou.qq+'</td>'
                    html += '<td>'+cou.title+'</td>'
                    html += '<td>'
                    html += ' <div class="btn-group">'
                    html += '<a class="btn btn-default btn-info" href="'+QIAN_PATH+'/res/cou/'+cou.type_id+'">查看</a>'
                    html += '<a class="btn btn-default btn-success" href="javascript:adopt('+res_type+','+cou.type_id+', 1);">通过</a>'
                    html += '<a class="btn btn-default btn-danger" href="javascript:adopt('+res_type+','+cou.type_id+', 0);">不通过</a>'
                    html += '</div></td></tr>'
                })
                $('#cour-shen>table>tbody').append(html)

                html = ''
                res_type = "'res'"
                $.each(ress, function(i, res){
                    html += '<tr>'
                    html += '<td>'+res.qq+'</td>'
                    html += '<td>'+res.title+'</td>'
                    html += '<td>'
                    html += ' <div class="btn-group">'
                    html += '<a class="btn btn-default btn-info" href="'+QIAN_PATH+'/res/res/'+res.type_id+'">查看</a>'
                    html += '<a class="btn btn-default btn-success" href="javascript:adopt('+res_type+','+res.type_id+', 1);">通过</a>'
                    html += '<a class="btn btn-default btn-danger" href="javascript:adopt('+res_type+','+res.type_id+', 0);">不通过</a>'
                    html += '</div></td></tr>'
                })
                $('#zi-shen>table>tbody').append(html)
            }else{
                location.href = '/index'
            }
        }
    })
})

// 通过
function adopt(res_type, type_id, cla){
    if(confirm('是否确认该操作')){
        $.ajax({
            url: HOU_PATH + '/res/examine/adopt',
            type: 'post',
            data: {'res_type': res_type, 'type_id': type_id, 'cla': cla},
            dataType: 'json',
            headers: {
                'authorization': window.localStorage.getItem('token')
            },
            success: function(data){
                if(data.code == 200){
                    location.reload(true)
                }else{
                    alert(data.error)
                }
            }
        })
    }
}


