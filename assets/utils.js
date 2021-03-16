import $ from 'jquery';

function goToUrl({url}) {
    window.location = url;
}

function getModalDataAjax(url) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: 'get',
            url: url,
            success: (data) => {
                $('.modal-body').html(data.html);
                resolve(data);
            },
            error: (data) => {
                reject(data);
            },
        });
    });
}

function addAjaxFormHandler(formId, successCb, failCb, getFormData = (form) => new FormData(form)) {
    $(formId).on('submit', (event) => {
        const fd = getFormData(event.target);
        event.preventDefault();
        $.ajax({
            type: $(formId).attr('method'),
            url: $(formId).attr('action'),
            data: fd,
            contentType: false,
            processData: false,
            success: (data) => {
                if (data.success) {
                    successCb(data);
                } else {
                    failCb(data);
                }
            },
        });
    });
}

export {getModalDataAjax, addAjaxFormHandler, goToUrl};
