$(function () {
    $('#sampleTable').DataTable();
    $(".new-scan").click(function () {
        const task_name = $('[name="task_name"]').val();
        const target_addr = $('[name="target_addr"]').val();
        const scan_type = $('[name="scan_type"]').val();
        const description_val = $('[name="description_val"]').val();
        if (!task_name || !target_addr || !scan_type) {
            swal("Warning", "Please check the input!", "error");
        } else {
            $.post('/vul-scanner', {
                "task_name": task_name,
                "target_addr": target_addr,
                "scan_type": scan_type,
                "description_val": description_val,
                "source": "new_scan"
            }, function (e) {
                if (e === 'success') {
                    swal({
                            title: "扫描任务创建成功!",
                            text: "",
                            type: "success",
                            confirmButtonColor: "#41b883",
                            confirmButtonText: "ok",
                            closeOnConfirm: false
                        },
                        function () {
                            location.href = "/vul-scanner";
                        });
                } else {
                    swal("Error", "Something wrong", "error");
                }
            })
        }
    });
});

function delete_scan(nid){
    swal({
      title: "是否删除该扫描?",
      text: "",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Delete！",
      closeOnConfirm: false
    },
    function() {
        $.post('/vul-tasks', {
            "delete": nid,
            "source": 'delete_scan',
        }, function (e) {
            if (e === 'success') {
                swal({
                        title: "任务删除成功",
                        text: "",
                        type: "success",
                        confirmButtonColor: "#41b883",
                        confirmButtonText: "ok",
                        closeOnConfirm: false
                    },
                    function () {
                        location.href = "/vul-tasks";
                    });
            } else {
                swal("Error", "删除出错", "error");
            }
        })
    })
}

function report_url(nid){
    $.post('/vul-tasks', {
        "scan_id": nid,
        "source": 'report',
    }, function (e) {
        if (e !== 'warning') {
            document.getElementById("report_download_html").innerHTML="<a href=\"static/download/" + e['html_url'] + "\" target=\"view_window\"><button class=\"btn btn-primary btn-block\" type=\"button\">HTML</button></a>";
            document.getElementById("report_download_pdf").innerHTML="<a href=\"static/download/" + e['pdf_url'] + "\" target=\"view_window\"><button class=\"btn btn-primary btn-block\" type=\"button\">PDF</button></a>";
        }
    })
}

function delete_task(nid){
    swal({
      title: "是否删除该任务?",
      text: "",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Delete！",
      closeOnConfirm: false
    },
    function() {
        $.post('/vul-scanner', {
            "delete": nid,
            "source": 'delete_task',
        }, function (e) {
            if (e === 'success') {
                swal({
                        title: "任务删除成功",
                        text: "",
                        type: "success",
                        confirmButtonColor: "#41b883",
                        confirmButtonText: "ok",
                        closeOnConfirm: false
                    },
                    function () {
                        location.href = "/vul-scanner";
                    });
            } else {
                swal("Error", "删除出错", "error");
            }
        })
    })
}

function down_report(nid){
    $.post('/vul-scanner', {
        "task_id": nid,
        "source": 'download_report',
    }, function (e) {
        if (e !== 'warning') {
            document.getElementById("report_download_html").innerHTML="<a href=\"static/download/" + e['html_url'] + "\" target=\"view_window\"><button class=\"btn btn-primary btn-block\" type=\"button\">HTML</button></a>";
            document.getElementById("report_download_pdf").innerHTML="<a href=\"static/download/" + e['pdf_url'] + "\" target=\"view_window\"><button class=\"btn btn-primary btn-block\" type=\"button\">PDF</button></a>";
        }
    })
}