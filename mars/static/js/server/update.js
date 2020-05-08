$(function () {
    $.ajax({
        type: 'GET',
        url: '/update',
        success: function (response) {
            var html = "<ul class='app-notification dropdown-menu dropdown-menu-right'><li class='app-notification__title'>You have " +response.title.length + " new notifications.</li>";
            for(var i = 0; i < response.title.length; i++)
            {
                html += "<li><a class=\"app-notification__item\" href=" + response.url[i] + " target='_blank'><span class=\"app-notification__icon\"><span class=\"fa-stack fa-lg\">" +
                    "<i class=\"fa fa-circle fa-stack-2x text-primary\"></i><i class=\"fa fa-envelope fa-stack-1x fa-inverse\"></i></span></span><div>" +
                    "<p class=\"app-notification__message\">" + response.title[i] + "</p><p class='app-notification__meta'>" + response.text[i] + "</p></div></a></li>";
            }
            html += "<li class='app-notification__footer'><a href='#'>See all notifications.</a></li></ul>";
            $('#notification_update').html(html);
        },
        error: function() {
            var html = "<ul class='app-notification dropdown-menu dropdown-menu-right'><li class='app-notification__title'>You have 0 new notifications.</li>" +
                "<div class=\"app-notification__content\"><li><a class=\"app-notification__item\" href=\"javascript:;\"><span class=\"app-notification__icon\">" +
                "<span class=\"fa-stack fa-lg\"></span></span><div></div>";
            $('#notification_update').html(html);
        }
    });
});
function readVersion() {
    var reader = new FileReader();
    reader.onload = function(e) {
        var text = reader.result;
    };

reader.readAsText(file, encoding);
}
