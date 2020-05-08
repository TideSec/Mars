$(function () {
    $("#newAsset").click(function () {
        // const asset_name = $('[name="asset_name"]').val();
        const asset_host = $('[name="asset_host"]').val();
        const asset_cus_id = $('[name="asset_cus_id"]').val();
        const admin_name = $('[name="admin_name"]').val();
        const asset_scan_zhouqi= $('[name="asset_scan_zhouqi"]').val();
        const discover_option = $("input[name='enable_check']").is(':checked');
        const domain_fast_port_scan = $("input[name='domain_fast_port_scan']").is(':checked');
        const c_scan = $("input[name='c_scan']").is(':checked');
        const c_fast_port_scan = $("input[name='c_fast_port_scan']").is(':checked');
        // const discover_option = $("input[type='checkbox']").is(':checked');
        if (!asset_cus_id || !asset_host || !admin_name) {
            swal("Warning","请输入资产及所属客户!", "error");
        } else {
            $.post('/new-asset', {
                // "asset_name": asset_name,
                "asset_host": asset_host,
                "asset_cus_id": asset_cus_id,
                "admin_name": admin_name,
                "discover_option": discover_option,
                "asset_scan_zhouqi":asset_scan_zhouqi,
                "domain_fast_port_scan":domain_fast_port_scan,
                "c_scan":c_scan,
                "c_fast_port_scan":c_fast_port_scan,
                // "split_asset_option":split_asset_option,
                "source": "new_asset",
            }, function (e) {
                if (e === 'success') {
                    swal({
                      title: "添加资产成功!",
                      text: "",
                      type: "success",
                      confirmButtonColor: "#41b883",
                      confirmButtonText: "ok",
                      closeOnConfirm: false
                    },
                    function(){
                      location.href = "/asset-management";
                    });
                } else {
                    swal("Warning","添加资产失败!", "error");
                }
            })
        }
    });
});