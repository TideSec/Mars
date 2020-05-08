$(function () {
    $('#sampleTable').DataTable();
});

function delete_result(nid){
    const data = {
        "delete": nid,
    };
    swal({
      title: "确定要删除该结果?",
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
            url: '/week-passwd-list',
            data: data,
            success: function() {
                location.href = "/week-passwd-list";
                },
            error: function(xhr, type) {
            }
        });
    });
}