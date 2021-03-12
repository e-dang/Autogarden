function successCb(data) {
    window.location = data.url;
}

function failCb(data) {
    $(configs.formContainerSelector).html(data.html);
    addAjaxFormHandler(configs.formSelector, successCb, failCb);
    addCropImageHandler(configs);
}

function tokenSuccessCb(data) {
    $('#id_uuid').val(data.html);
}

getModalDataAjax(configs.deleteUrl);
addAjaxFormHandler(configs.formSelector, successCb, failCb);
addAjaxFormHandler('#tokenForm', tokenSuccessCb, () => null);
addCropImageHandler(configs);
