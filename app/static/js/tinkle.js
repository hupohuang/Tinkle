$(function(){
    /*登陆*/
    $('button#submit').click(function(){
        var $tishi = $('#tishi');
        var $username = $('input[name="username"]').val();
        var $password = $('input[name="password"]').val();
        $.ajax({
            url:'/login',
            data:$('form').serialize(),
            type:'POST',
            dataType:'json'
        }).done(function(data) {
            if (!data.r){
                window.location.reload();
            } else {
                $tishi.show();
                $tishi.html("提示："+ data.error);
            }
        });
    });
    $('.login-modal').on('hide.bs.modal', function() {
        var $tishi = $('#tishi');
        $tishi.hide();
    });

    /*相册*/
    var t;
    $(".xc-p").mouseenter(function(){
        var ac = $(this);
        t = setTimeout(function(){ ac.find(".xc-inf").show(200);},200);
    }).mouseleave(function(){
        clearTimeout(t);
    });
    $(".xc-p").mouseleave(function(){
        $(this).find(".xc-inf").hide(200);
    });
    $('.bianji').click(function(){
        var $zhu = $(this).parent();
        var $shu = $zhu.parent();
        $shu.find(".modal-header .tpname").hide();
        $shu.find(".modal-header .tpwenben").show();
        $shu.find(".modal-body .xinxi").hide();
        $shu.find(".modal-body .wenben").show();
        $(this).hide();
        $zhu.find(".queren").show();
        $zhu.find(".shanchu").hide();
    });
    $('.queren').click(function(){
        var $zhu = $(this).parent();
        var $shu = $zhu.parent();
        $.ajax({
            url:'/edit_tp',
            data:JSON.stringify({
                'id': $shu.parent().parent().attr('id'),
                'body': $shu.find(".modal-body .wenben").val(),
                'tpname': $shu.find(".modal-header .tpwenben").val(),
            }),
            type:'POST',
            dataType:'json'
        }).done(function(data) {
            $shu.find(".modal-body .xinxi").text(data.body);
            $shu.find(".modal-header .tpname").text(data.tpname);
            $shu.find(".modal-header .tpname").show();
            $shu.find(".modal-header .tpwenben").hide();
            $shu.find(".modal-body .xinxi").show();
            $shu.find(".modal-body .wenben").hide();
            $zhu.find(".queren").hide();
            $zhu.find(".bianji").show();
            $zhu.find(".shanchu").show();
            var $ahu = $shu.parent().parent().parent();
            $ahu.find(".btn-toolbar .tpname").text(data.tpname);
            $ahu.find(".zxinxi").text(data.body);
        });

    });
    $('.tp-modal').on('hide.bs.modal', function() {
        var $zhu = $(this).parent();
        var $shu = $zhu.parent();
        $shu.find(".modal-header .tpname").show();
        $shu.find(".modal-header .tpwenben").hide();
        $shu.find(".modal-body .xinxi").show();
        $shu.find(".modal-body .wenben").hide();
        $zhu.find(".queren").hide();
        $zhu.find(".bianji").show();
        $zhu.find(".shanchu").show();
    });
    $('.fm').click(function(){
        var $q = $(this).parent().parent().parent().parent()
        $.ajax({
            url:'/edit_fm',
            data:JSON.stringify({
                'id': $q.find('.modal').attr('id'),
            }),
            type:'POST',
            dataType:'json'
        }).done(function(data){
            if (data.r){
                swal({
                    title:'已更换封面',
                    type:"success",
                },function(){
                    window.location.reload();
                });
            }
        });
    });
    $('.shanchutp').click(function(){
        var $b = $(this).parent().parent().parent().parent();
        swal({
                title:"删除图片",
                text:"删除图片",
                type:"warning",
                showCancelButton:true,
                confirmButtonColor:"#DD6B55",
                confirmButtonText:"删除",
                cancelButtonText:"取消",
                closeOnConfirm:false,
            },
        function(){
            $.ajax({
                type:'POST',
                url:'/delete_tp',
                data:JSON.stringify({
                    'id': $b.attr('id'),
                }),
                dataType:'json',
                success: function(data,status){
                    if(status == 'success'){
                        swal("删除图片","已删除图片","success");
                        $('.modal').modal('hide');
                        $b.parent().parent().hide(200);
                    }
                },
            });
        });
    });

    /*管理相册*/
    $('.shanchuxc').click(function(){
        var $q = $(this).parent().parent();
        swal({
                title:"删除相册",
                text:"删除相册",
                type:"warning",
                showCancelButton:true,
                confirmButtonColor:"#DD6B55",
                confirmButtonText:"删除",
                cancelButtonText:"取消",
                closeOnConfirm:false,
            },
        function(){
            $.ajax({
                type:'POST',
                url:'/delete_xc',
                data:JSON.stringify({
                    'id': $q.attr('id'),
                }),
                dataType:'json',
                success: function(data,status){
                    if(status == 'success'){
                        swal("OK");
                        $q.hide(200);
                    }
                },
            });
        });
    });
});