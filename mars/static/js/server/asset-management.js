$(function () {
    $('#sampleTable').DataTable();

    var demo1 = $('select[name="plugin_list"]').bootstrapDualListbox();
    var demo2 = $('select[name="auth_service_list"]').bootstrapDualListbox();

    $(".asset-update").click(function () {
        // const asset_name = $('[name="asset_name_edit"]').val();
        const asset_id = $('[name="asset_id_edit"]').val();
        // const host_val = $('[name="asset_host_edit"]').val();
        // const dept_name = $('[name="dept_name_edit"]').val();
        // const admin_name = $('[name="admin_name_edit"]').val();
        const task_state = $("input[name='asset_state_edit']").is(':checked');
        // alert(window.location.href);
        if (!asset_id ) {
            // || !host_val || !dept_name
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/asset-management', {
                // "asset_name": asset_name,
                "asset_id": asset_id,
                // "host_val": host_val,
                // "dept_name": dept_name,
                // "admin_name": admin_name,
                // "discover_option": discover_option,
                "task_state": task_state,
                "source": "asset_update"
            }, function (e) {
                if (e === 'success') {
                    swal({
                            title: "更新资产任务成功!",
                            text: "",
                            type: "success",
                            confirmButtonColor: "#41b883",
                            confirmButtonText: "ok",
                            closeOnConfirm: false
                        },
                        function(){
                        location.href = window.location.href;
                    });
                } else {
                    swal("Error","更新资产任务失败", "error");
                }
            })
        }
    });

    $("#asset-scan").click(function () {
        const taskname_val = $('[name="taskname_val"]').val();
        const plugin_val = $('[name="plugin_list"]').val().join(",");
        const recursion_val = $('[name="recursion_val"]').val();
        const target_val = $('[name="target_val"]').val();
        if (!taskname_val || !plugin_val || !target_val) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/add-task', {
                "taskname_val": taskname_val,
                "plugin_val": plugin_val,
                "recursion_val": recursion_val,
                "target_val": target_val,
                "source": "asset",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Task added successfully!",
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
                    swal("Warning","Failed to create task!", "error");
                }
            })
        }
    });

    $("#asset-auth-tasks").click(function () {
        const task_name = $('[name="auth_task_name"]').val();
        const target_list = $('[name="auth_target_list"]').val();
        const service_list = $('[name="auth_service_list"]').val().join(",");
        const username_list = $('[name="auth_username_list"]').val();
        const password_list = $('[name="auth_password_list"]').val();
        const args = $('[name="auth_args"]').val();
        const recursion = $('[name="auth_recursion"]').val();
        if (!task_name || !target_list || !service_list|| !username_list|| !password_list || !recursion) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/auth-tester', {
                "task_name": task_name,
                "target_list": target_list,
                "service_list": service_list,
                "username_list": username_list,
                "password_list": password_list,
                "args": args,
                "recursion": recursion,
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Task added successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/auth-tester-tasks";
                    });
                } else {
                    swal("Warning","Failed to create task!", "error");
                }
            })
        }
    });
});

function delete_asset(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "确定要删除任务?",
      text: "该操作会删除该任务的所有资产！",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Delete！",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/asset-management',
            data: data,
            success: function() {
                location.href = "/asset-management";
                },
            error: function(xhr, type) {
            }
        });
    });
}

function asset_info(nid){
    const data = {
        "edit": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/asset-management',
        data: data,
        dataType: 'json',
        success: function(respond) {
            const data  = eval(respond);
            const asset_name = data.asset_name;
            const task_state = data.task_state;
            const admin_name = data.admin_name;
            const asset_cus_id = data.asset_cus_id;
            const asset_cus_name = data.asset_cus_name;
            const discover_option = data.discover_option;
            const asset_host = data.asset_host;
            const asset_scan_zhouqi = data.asset_scan_zhouqi;

            $('#asset_name_edit').val(asset_name);
            $('#asset_cus_edit').val(asset_cus_name);
            $('#asset_cus_id_edit').val(asset_cus_id);
            $('#asset_host_edit').val(asset_host);
            $('#asset_discover_option_edit').val(discover_option);
            $('#asset_admin_edit').val(admin_name);
            $('#asset_state_edit').val(task_state);
            $('#asset_scan_zhouqi_edit').val(asset_scan_zhouqi);
            $('#asset_id_edit').val(nid);
        },
        error: function(xhr, type) {
        }
    });
}

function get_asset_host(nid){
    const data = {
        "scan": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/asset-management',
        data: data,
        dataType: 'json',
        success: function(respond) {
            const data  = eval(respond);
            const asset_host = data.asset_host;
            $('#scan_target_list').val(asset_host);
            $('#auth_target_list').val(asset_host);
        },
        error: function(xhr, type) {
        }
    });
}

