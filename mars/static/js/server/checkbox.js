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

function getAll() {
    var select_list = [];
    $("input[name='select_id']:checked").each(function () {
        select_list.push(this.value);
    });
    if(select_list.length === 0) {
        swal("Warning","Please select the target", "error");
    } else {
        alert(select_list)
    }
}