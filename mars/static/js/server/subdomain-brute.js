$(function () {
    $('#sampleTable').DataTable();
    var demo1 = $('select[name="plugin_list"]').bootstrapDualListbox();

    $("#new_domain").click(function () {
        const domain_name_val = $('[name="domain_name_val"]').val();
        const domain_val = $('[name="domain_val"]').val();
        const third_domain = $("input[type='checkbox']").is(':checked');
        if (!domain_name_val || !domain_val) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/subdomain-brute', {
                "domain_name_val": domain_name_val,
                "domain_val": domain_val,
                "third_domain": third_domain,
                "source": "new_domain",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Created!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/subdomain-brute";
                    });
                } else {
                    swal("Warning","Failed to create task!", "error");
                }
            })
        }
    });

    $("#domain-scan").click(function () {
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
                "source": "subdomain",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Created!",
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

    $("#awvs-scan").click(function () {
        const task_name = $('[name="awvs_task_name"]').val();
        const target_addr = $('[name="awvs_target"]').val();
        const scan_type = $('[name="awvs_scan_type"]').val();
        const description_val = $('[name="awvs_desc_val"]').val();
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
                            title: "Task added successfully!",
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

function delete_domain(nid){
    const data = {
        "delete": nid,
    };
    swal({
            title: "Are you sure you want to delete?",
            text: "If you delete an item, it will be permanently lost",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Delete！",
            closeOnConfirm: false
        },
        function(){
        $.ajax({
            type: 'GET',
            url: '/subdomain-brute',
            data: data,
            success: function() {
                location.href = "/subdomain-brute";
                },
            error: function(xhr, type) {}
        });
    });
}

function get_domain_host(nid){
    const data = {
        "subdomain": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/subdomain-list',
        data: data,
        success: function(respond) {
            $('#scan_target_list').val(respond);
        },
        error: function(xhr, type) {
        }
    });
}

function get_domain_awvs(nid){
    const data = {
        "subdomain": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/subdomain-list',
        data: data,
        success: function(respond) {
            $('#awvs_target').val(respond);
        },
        error: function(xhr, type) {
        }
    });
}