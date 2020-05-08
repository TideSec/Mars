$(function () {
    // $('#sampleTable').DataTable();

    $('#sampleTable').DataTable();


    $(".task-update").click(function () {
        const taskname_val = $('[name="taskname_val"]').val();
        const task_id = $('[name="task_id"]').val();
        const recursion_val = $('[name="recursion_val"]').val();
        const target_val = $('[name="target_val"]').val();
        if (!taskname_val || !task_id || !target_val) {
            swal("Warning","请检查输入!", "error");
        } else {
            $.post('/task-edit', {
                "taskname_val": taskname_val,
                "task_id": task_id,
                "recursion_val": recursion_val,
                "target_val": target_val,
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "任务更新成功!",
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
                    swal("Error","任务更新出错", "error");
                }
            })
        }
    });
});

function rescan_task(nid){
    const data = {
        "rescan": nid,
    };
    swal({
      title: "需要重新扫描?",
      text: "重新扫描时会清除之前的扫描结果！",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Rescan",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/task-management',
            data: data,
            success: function() {
                location.href = "/task-management";
                },
            error: function(xhr, type) {
            }
        });
    });
}

function task_edit_id(nid){
    const data = {
        "edit": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/task-management',
        data: data,
        dataType: 'json',
        success: function(e) {
            const data  = eval(e);
            const task_name = data.task_name;
            const scan_target_list = data.scan_target;
            $('#scan_target_list').val(scan_target_list);
            $('#task_name').val(task_name);
            $('#task_id').val(nid);
        },
        error: function(xhr, type) {
        }
    });
}

function task_delete(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "是否确定删除任务?",
      text: "",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Delete！",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/task-management',
            data: data,
            success: function() {
                location.href = "/task-management";
                },
            error: function(xhr, type) {
            }
        });
    });
}
