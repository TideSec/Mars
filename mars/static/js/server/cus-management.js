$(function () {
    // $('#sampleTable').DataTable();

    $('#sampleTable').DataTable();


    $(".cus-update").click(function () {
        const cus_name = $('[name="cus_name"]').val();
        const cus_id = $('[name="cus_id"]').val();
        const cus_contact = $('[name="cus_contact"]').val();
        const cus_phone = $('[name="cus_phone"]').val();
        const cus_email = $('[name="cus_email"]').val();
        const cus_zhouqi_start = $('[name="cus_zhouqi_start"]').val();
        const cus_zhouqi_end = $('[name="cus_zhouqi_end"]').val();
        const cus_serv_type = $('[name="cus_serv_type"]').val();
        const cus_other = $('[name="cus_other"]').val();

        if (!cus_name) {
            swal("Warning","请输入客户名称！", "error");
        } else {
            $.post('/cus-edit', {
                "cus_name": cus_name,
                "cus_id":cus_id,
                "cus_contact": cus_contact,
                "cus_phone": cus_phone,
                "cus_email": cus_email,
                "cus_zhouqi_start": cus_zhouqi_start,
                "cus_zhouqi_end":cus_zhouqi_end,
                "cus_serv_type": cus_serv_type,
                "cus_other": cus_other,
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "更新客户信息成功!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/cus-management";
                    });
                } else {
                    swal("Error","更新客户信息失败", "error");
                }
            })
        }
    });
});

function rescan_asset(nid){
    const data = {
        "rescan": nid,
    };
    swal({
      title: "确定要重新扫描?",
      text: "该操作会重新扫描该客户的所有资产！",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "重新扫描",
      cancelButtonText: "取消",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/cus-management',
            data: data,
            success: function() {
                location.href = "/cus-management";
                },
            error: function(xhr, type) {
            }
        });
    });
}

function cus_edit_id(nid){
    const data = {
        "edit": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/cus-management',
        data: data,
        dataType: 'json',
        success: function(e) {
            const data  = eval(e);
            const cus_name = data.cus_name;
            const cus_contact = data.cus_contact;
            const cus_phone = data.cus_phone;
            const cus_email = data.cus_email;
            const cus_zhouqi_start = data.cus_zhouqi_start;
            const cus_zhouqi_end = data.cus_zhouqi_end;
            const cus_serv_type = data.cus_serv_type;
            const cus_other = data.cus_other;
            $('#cus_name').val(cus_name);
            $('#cus_contact').val(cus_contact);
            $('#cus_phone').val(cus_phone);
            $('#cus_email').val(cus_email);
            $('#cus_zhouqi_start').val(cus_zhouqi_start);
            $('#cus_zhouqi_end').val(cus_zhouqi_end);
            $('#cus_serv_type').val(cus_serv_type);
            $('#cus_other').val(cus_other);
            $('#cus_id').val(nid);
        },
        error: function(xhr, type) {
        }
    });
}

function cus_delete(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "确定要删除客户?",
      text: "该操作会删除该客户的所有任务和资产！",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "删除！",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/cus-management',
            data: data,
            success: function() {
                location.href = "/cus-management";
                },
            error: function(xhr, type) {
            }
        });
    });
}
