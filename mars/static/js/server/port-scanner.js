$(function () {
    $('#sampleTable').DataTable();
    setTimeout('reflush()',5000);

    $(".port-update").click(function () {
        const port_list = $('[name="edit_port_val"]').val();
        if (!port_list) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "port_list": port_list,
                "source": "port_scan"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/port-scanner";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".new-scan").click(function () {
        const target_val = $('[name="target_val"]').val();
        const arguments_val = $('[name="arguments_val"]').val();
        const port_val = $('[name="port_val"]').val();
        if (!target_val) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/port-scanner', {
                "target_val": target_val,
                "arguments_val": arguments_val,
                "port_val": port_val,
                "source": "new_scan"
            }, function (e) {
                if (e.result === 'success') {
                    swal({
                      title: "Added Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/port-scanner?scan_id=" + e.scan_id;

                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });
});

function reflush() {
    var url = location.search;
    var pre_result = document.getElementById('pre_result').innerHTML;
    var url_re = url.indexOf("scan_id");
    var pre_re = pre_result.indexOf("nmap");
    if (url_re !== -1) {
        if (pre_re === -1) {
            window.location.reload();
        }
    }
}

function port_result(nid){
    const data = {
        "result": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/port-scanner',
        data: data,
        success: function(result) {
            $('#port_result').html(result);
        },
        error: function(xhr, type) {

        }
    });
}

function result_delete(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "Are you sure you want to delete?",
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
            url: '/port-scanner',
            data: data,
            success: function() {
                location.href = "/port-scanner";
                },
            error: function(xhr, type) {
            }
        });
    });
}