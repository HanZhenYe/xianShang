
$(function(){
    $('.ul-zi>li>a').attr('target',"t_blank")
    $.ajax({
        url: HOU_PATH + '/res/index',
        type: 'get',
        dataType: 'json',
        headers: {
            'authorization': window.localStorage.getItem('token')
        },
        success: function(data){
            pla = data.data.pla
            if (data.data.if_login){
                html = '<li><a href="javascript:quit();"><span class="glyphicon glyphicon-log-out"></span> 退出</a></li>'
                $('#user-state').append(html)
            }else{
                html = '<li><a href="javascript:login();"><span class="glyphicon glyphicon-log-in"></span> 登陆</a></li>'
                $('#user-state').append(html)
            }

            html = ''
            $.each(pla, function(i, p){
                html += '<li>'
                html += '<a href="'+p.link+'" target="view_window">'
                html += '<div class="panel panel-default">'
                html += '<div class="panel-body zi-img">'
                html += ' <img src="'+HOU_PATH+'/media/'+p.cover+'" alt="页面丢失">'
                html += '</div>'
                html += '<div class="panel-footer">'+p.name+'</div>'
                html += '</div></a></li>'
            })
            $('.ul-zi').append(html)

            occs = data.data.occ
            html = ''
            $.each(occs, function(i, occ){
                html += '<li>'
                html += '<a href="'+QIAN_PATH+'/res/occ/'+occ.id+'">'
                html += '<div class="panel panel-default">'
                html += '<div class="panel-heading">'+occ.title+'</div>'
                html += '<div class="panel-body ziyuan-img">'
                html += '<img src="'+HOU_PATH+'/media/'+occ.cover+'">'
                html += ' </div>'
                html += '<div class="panel-footer">'
                html += '<div>'
                html += '<span class="glyphicon glyphicon-star"></span> '+occ.collection
                html += '</div><div>'
                html += '<span class="glyphicon glyphicon-user"></span> '+ occ.name
                html += '</div></div></div></a></li>'
            })
            $('#occ').append(html)

            coursers = data.data.courser
            html = ''
            $.each(coursers, function(i, courser){
                html += '<li>'
                html += '<a href="'+QIAN_PATH+'/res/cos/'+courser.id+'">'
                html += '<div class="panel panel-default">'
                html += '<div class="panel-heading">'+courser.title+'</div>'
                html += '<div class="panel-body ziyuan-img">'
                html += '<img src="'+HOU_PATH+'/media/'+courser.cover+'">'
                html += ' </div>'
                html += '<div class="panel-footer">'
                html += '<div>'
                html += '<span class="glyphicon glyphicon-star"></span> '+courser.collection
                html += '</div><div>'
                html += '<span class="glyphicon glyphicon-user"></span> '+ courser.name
                html += '</div></div></div></a></li>'
            })
            $('#courser').append(html)

            cours = data.data.cour
            html = ''
            $.each(cours, function(i, cour){
                html += '<li>'
                html += '<a href="'+QIAN_PATH+'/res/cou/'+cour.id+'">'
                html += '<div class="panel panel-default">'
                html += '<div class="panel-heading">'+cour.title+'</div>'
                html += '<div class="panel-body ziyuan-img">'
                html += '<img src="'+HOU_PATH+'/media/'+cour.cover+'">'
                html += ' </div>'
                html += '<div class="panel-footer">'
                html += '<div>'
                html += '<span class="glyphicon glyphicon-star"></span> '+cour.collection
                html += '</div><div>'
                html += '<span class="glyphicon glyphicon-user"></span> '+ cour.name
                html += '</div></div></div></a></li>'
            })
            $('#cour').append(html)

           ress = data.data.res
            html = ''
            $.each(ress, function(i, res){
                html += '<li>'
                html += '<a href="'+QIAN_PATH+'/res/res/'+res.id+'">'
                html += '<div class="panel panel-default">'
                html += '<div class="panel-heading">'+res.title+'</div>'
                html += '<div class="panel-body ziyuan-img">'
                html += '<img src="'+HOU_PATH+'/media/'+res.cover+'">'
                html += ' </div>'
                html += '<div class="panel-footer">'
                html += '<div>'
                html += '<span class="glyphicon glyphicon-star"></span> '+res.collection
                html += '</div><div>'
                html += '<span class="glyphicon glyphicon-user"></span> '+ res.name
                html += '</div></div></div></a></li>'
            })
            $('#res').append(html)
        }
    })
})
