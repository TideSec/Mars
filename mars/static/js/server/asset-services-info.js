
function server_info111(info){
    console.log(info);
    $('#server_info').html('xxxxx');
}


function server_info(id_port){
    console.log(id_port);
    const data = {
        "port": id_port,
    };
    $.ajax({
        type: 'GET',
        url: '/asset-info',
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