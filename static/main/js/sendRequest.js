let send_data = function (data, url, successFun = function () {}) {
    var fd = new FormData();
    $.each(data, function (key, value) {
        fd.append(key, value);
    });
    $.ajax({
        type: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
        },
        url: url,
        data: fd,
        processData: false,
        contentType: false,
        success: function (response) {
            successFun(response);
        },
    });
};