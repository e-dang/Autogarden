const configs = {
    imgInputSelector: '#id_image',
    cropBtnSelector: '#cropBtn',
    resetBtnSelector: '#resetBtn',
    imgContainerSelector: '#imageContainer',
    formSelector: '#newGardenForm',
};

function successCb(data) {
    window.location = data.url;
}

function failCb(data) {
    $('.modal-body').html(data.html);
    addAjaxFormHandler(configs.formSelector, successCb, failCb);
    addCropImageHandler(configs);
}

addAjaxFormHandler(configs.formSelector, successCb, failCb);
addCropImageHandler(configs);
