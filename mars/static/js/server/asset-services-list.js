$(function () {
    $('#sampleTable').DataTable();
    var demo1 = $('select[name="plugin_list"]').bootstrapDualListbox();
    $("#server-scan").click(function () {
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
});

function server_info(nid){
    const data = {
        "info": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/asset-services',
        data: data,
        dataType: 'json',
        success: function(result) {
            $('#server_info').html(JSON.stringify(result, null, 4));
        },
        error: function(xhr, type) {

        }
    });
}

function selectAll()
{
    var allMails = document.getElementsByName("allSelect")[0];
    var mails = document.getElementsByName("select_id");
    if(allMails.checked)
    {
        for(var i = 0; i < mails.length; ++i)
        {
            mails[i].checked = true;
        }
    }
    else
        {
            for(var i = 0; i < mails.length; ++i)
            {
                mails[i].checked = false;
            }
        }
}

function newScan() {
    var select_list = [];
    $("input[name='select_id']:checked").each(function () {
        select_list.push(this.value);
    });
    if(select_list.length === 0) {
        swal("Warning","Please select the target", "error");
    } else {
        get_server_host(select_list)
    }
}

function get_server_host(server_list){
    $.post('/asset-services', {
        "server_list": server_list.join(","),
        "source": "server_scan"
    }, function (e) {
        $('#scan_target_list').val(e);
    });
}