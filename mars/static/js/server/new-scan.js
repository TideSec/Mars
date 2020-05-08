$(function () {
    var demo1 = $('select[name="plugin_list"]').bootstrapDualListbox();
    var demo2 = $('select[name="asset_list"]').bootstrapDualListbox();

    $("#showConfig").click(function () {
        const taskname_val = $('[name="taskname_val"]').val();
        const plugin_val = $('[name="plugin_list"]').val().join(",");
        const asset_id_val = $('[name="asset_list"]').val().join(",");
        const recursion_val = $('[name="recursion_val"]').val();
        const target_val = $('[name="target_val"]').val();

        if (!taskname_val || !plugin_val) {
                swal("Warning","请输入poc名称并选择poc!", "error");
        } else if (asset_id_val === '' && target_val === '')  {
                swal("Warning","请选择客户目标或者输入目标地址!", "error");
        }else{
            $.post('/add-task', {
                "taskname_val": taskname_val,
                "plugin_val": plugin_val,
                "recursion_val": recursion_val,
                "target_val": target_val,
                "asset_id_val":asset_id_val,
                "source": "scan_view",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "任务添加成功!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/task-management";
                    });
                } else {
                    swal("Warning","创建任务失败!", "error");
                }
            })
        }
    });
});