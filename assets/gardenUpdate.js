import {getModalDataAjax, addAjaxFormHandler} from './utils.js';
import ImageCropper from './imageCropper';
import $ from 'jquery';
import 'fittextjs';
import 'bootstrap';

const configs = JSON.parse(document.getElementById('configs').textContent);

function successCb(data) {
    window.location = data.url;
}

function failCb(data) {
    $(configs.formContainerSelector).html(data.html);
    addAjaxFormHandler(configs.formSelector, successCb, failCb);
    new ImageCropper(successCb, failCb).init();
}

function tokenSuccessCb(data) {
    $('#id_uuid').val(data.html);
}

getModalDataAjax(configs.deleteUrl);
addAjaxFormHandler(configs.formSelector, successCb, failCb);
addAjaxFormHandler('#tokenForm', tokenSuccessCb, () => null);
new ImageCropper(successCb, failCb).init();

$('#name').fitText(0.8, {maxFontSize: 30});
