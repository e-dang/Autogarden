import $ from 'jquery';
import 'fittextjs';

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

function getFormData(form) {
    return new FormData(form);
}

function addAjaxFormHandler(formHandler, extractFormData) {
    $(formHandler.formSelector).on('submit', (event) => {
        formHandler.handle(event, extractFormData);
    });
}

function createAddFormListeners(formHandler, cropper) {
    return () => {
        addAjaxFormHandler(formHandler, getFormData);
        cropper.init(formHandler);
    };
}

function fitText(id) {
    $(id).fitText(0.8, {maxFontSize: 30});
}

function getConfigData(id = 'configs') {
    return JSON.parse(document.getElementById(id).textContent);
}

export {getModalDataAjax, addAjaxFormHandler, goToUrl, getFormData, createAddFormListeners, fitText, getConfigData};
