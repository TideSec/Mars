$(function () {
    $('#sampleTable').DataTable();
});

function get_target_host(nid){
    $.post('/auth-tester-tasks', {
        "task_id": nid,
        "source": "target_info"
            }, function (e) {
        document.getElementById("target_info_data").innerHTML=e;
    })
}

function delete_task(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "确定要删除该任务?",
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
            url: '/auth-tester-tasks',
            data: data,
            success: function() {
                location.href = "/auth-tester-tasks";
                },
            error: function(xhr, type) {
            }
        });
    });
}

function rescan_task(nid){
    const data = {
        "rescan": nid,
    };
    swal({
      title: "是否要重新扫描该任务?",
      text: "重新扫描时会清空之前的扫描结果！",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Rescan",
      closeOnConfirm: false
    },
    function(){
        $.ajax({
            type: 'GET',
            url: '/auth-tester-tasks',
            data: data,
            success: function() {
                location.href = "/auth-tester-tasks";
                },
            error: function(xhr, type) {
            }
        });
    });
}