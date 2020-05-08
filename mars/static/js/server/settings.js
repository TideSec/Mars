$(function () {
    $(".update-thread-config").click(function () {
        const poc_thread = $('[id="poc_thread"]').val();
        const discovery_thread = $('[id="discovery_thread"]').val();
        const subdomain_thread = $('[id="subdomain_thread"]').val();
        const port_thread = $('[id="port_thread"]').val();
        const auth_tester_thread = $('[id="auth_tester_thread"]').val();
        const discovery_time = $('[name="discovery_time_val"]').val();
        if (!poc_thread || !discovery_thread || !subdomain_thread || !port_thread || !discovery_time) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "poc_thread": poc_thread,
                "discovery_thread": discovery_thread,
                "subdomain_thread": subdomain_thread,
                "port_thread": port_thread,
                "auth_tester_thread": auth_tester_thread,
                "discovery_time": discovery_time,
                "source": "thread_settings",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".update-subdomain-dict-config").click(function () {
        const subdomain_dict_2 = $('[id="subdomain_dict_2"]').val();
        const subdomain_dict_3 = $('[id="subdomain_dict_3"]').val();
        if (!subdomain_dict_2 || !subdomain_dict_3) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "subdomain_dict_2": subdomain_dict_2,
                "subdomain_dict_3": subdomain_dict_3,
                "source": "subdomain_dict"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Update!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".update-user-passwd").click(function () {
        const username_list = $('[id="username_list"]').val();
        const password_list = $('[id="password_list"]').val();
        if (!username_list || !password_list) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "username_list": username_list,
                "password_list": password_list,
                "source": "auth"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Successfully Update!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

    $(".update-port-config").click(function () {
        const port_list = $('[id="port_list"]').val();
        if (!port_list) {
            swal("Warning","Please check the input!", "error");
        } else {
            $.post('/advanced-option', {
                "port_list": port_list,
                "source": "port_list"
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "Updated Successfully!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/advanced-option";
                    });
                } else {
                    swal("Error","Something wrong", "error");
                }
            })
        }
    });

});
