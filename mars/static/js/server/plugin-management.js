function delete_plugin(nid){
    const data = {
        "delete": nid,
    };
    swal({
            title: "确定删除?",
            text: "确定删除后POC将被永久性删除",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Delete",
            closeOnConfirm: false
        },
        function(){
        $.ajax({
            type: 'GET',
            url: '/plugin-management',
            data: data,
            success: function() {
                location.href = "/plugin-management";
                },
            error: function(xhr, type) {}
        });
    });
}

function plugin_info(nid){
    const data = {
        "info": nid,
    };
    $.ajax({
        type: 'GET',
        url: '/plugin-management',
        data: data,
        dataType: 'json',
        success: function(result) {
            var html = filterXSS(JSON.stringify(result, null, 4));
            $('#plugin_info').html(html);
        },
        error: function(xhr, type) {

        }
    });
}

$('#sampleTable').DataTable();
Dropzone.autoDiscover = false;

$(".dropzone").dropzone({
    url: "plugin-upload",
    init: function() {
            this.on("complete", function (data) {
                const res = eval('(' + data.xhr.responseText + ')');
                // Don't delete it, it has magical power
                // for(var t = Date.now();Date.now() - t <= 2500;);
                if (res.result === "success") {
                    swal({
                            title: "上传完成",
                            text: "批量上传可能需要多等待一会儿",
                            type: "success",
                            confirmButtonColor: "#DD6B55",
                            confirmButtonText: "OK",
                            closeOnConfirm: false
                        },
                        function(){
                        location.href = "/plugin-management";
                    });
                } else {
                    swal({
                            title: "上传失败",
                            text: "<p>POC开发指南: <a href=\"https://github.com/knownsec/Pocsuite/blob/master/docs/CODING.md\" target=\"view_window\">Pocsuite PoC </a></p>",
                            html: true,
                            type: "error",
                            confirmButtonColor: "#DD6B55",
                            confirmButtonText: "OK",
                            closeOnConfirm: false
                        },
                        function(){
                        location.href = "/plugin-management";
                    });
                }
            });
        }
    });

function selectAll()
{
    var allPlugins = document.getElementsByName("allSelect")[0];
    var plugins = document.getElementsByName("select_id");
    if(allPlugins.checked)
    {
        for(var i = 0; i < plugins.length; ++i)
        {
            plugins[i].checked = true;
        }
    }
    else
    {
        for(var i = 0; i < plugins.length; ++i)
        {
            plugins[i].checked = false;
        }
    }
}

function showDelete(){
    var content_html = "<a class='btn btn-primary' href='#' onclick='deleteSelect()' title='Delete Select'></i>Delete Select</a><br><br>";
    document.getElementById("showDeleteDiv").innerHTML = content_html;
}

function deleteSelect(){
    var select_list = [];
    $("input[name='select_id']:checked").each(function () {
        select_list.push(this.value);
    });
    if(select_list.length === 0) {
        swal("Warning","请选择删除目标", "error");
    } else {
        swal({
            title: "确定删除?",
            text: "确定删除后POC将被永久性删除",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Delete",
            closeOnConfirm: false
        },
        function(){
            $.post('/plugin-management', {
                "plugins_list": select_list.join(","),
                "source": "delete_select",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "删除成功",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/plugin-management";
                    });
                } else {
                    swal("Warning","删除失败!", "error");
                }
            })
        });
        }
}