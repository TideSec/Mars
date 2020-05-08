$(function () {

    $("#showConfig").click(function () {
        const cus_name = $('[name="cus_name"]').val();
        const cus_contact = $('[name="cus_contact"]').val();
        const cus_phone = $('[name="cus_phone"]').val();
        const cus_email = $('[name="cus_email"]').val();
        const cus_zhouqi_start = $('[name="cus_zhouqi_start"]').val();
        const cus_zhouqi_end = $('[name="cus_zhouqi_end"]').val();
        const cus_serv_type = $('[name="cus_serv_type"]').val();
        // const cus_serv_zhouqi = $('[name="cus_serv_zhouqi"]').val();
        const cus_other = $('[name="cus_other"]').val();

        if (!cus_name) {
            swal("Warning","请输入客户名称！", "error");
        } else {
            $.post('/add-customer', {
                "cus_name": cus_name,
                "cus_contact": cus_contact,
                "cus_phone": cus_phone,
                "cus_email": cus_email,
                "cus_zhouqi_start": cus_zhouqi_start,
                "cus_zhouqi_end":cus_zhouqi_end,
                "cus_serv_type": cus_serv_type,
                // "cus_serv_zhouqi": cus_serv_zhouqi,
                "cus_other": cus_other,
                "source":"add_cus",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "添加客户成功",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/cus-management";
                    });
                } else if (e === 'repeat') {
                    swal("Warning","客户名称已存在", "error")}
                else {
                    swal("Warning","添加客户信息失败", "error");
                }
            })
        }});
});