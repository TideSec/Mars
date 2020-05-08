$(function () {
    var demo1 = $('select[name="service_list"]').bootstrapDualListbox();

    $("#newAuth").click(function () {
        const task_name = $('[name="task_name"]').val();
        const target_list = $('[name="target_list"]').val();
        const service_list = $('[name="service_list"]').val().join(",");
        const username_list = $('[name="username_list"]').val();
        const password_list = $('[name="password_list"]').val();
        const args = $('[name="args"]').val();
        const recursion = $('[name="recursion"]').val();
        if (!task_name || !target_list || !service_list|| !username_list|| !password_list || !recursion) {
            swal("Warning","请检查输入是否完整!", "error");
        } else {
            $.post('/auth-tester', {
                "task_name": task_name,
                "target_list": target_list,
                "service_list": service_list,
                "username_list": username_list,
                "password_list": password_list,
                "args": args,
                "recursion": recursion,
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "任务添加成功!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/auth-tester-tasks";
                    });
                } else {
                    swal("Warning","创建任务失败!", "error");
                }
            })
        }
    });
});