import {getModalDataAjax, addAjaxFormHandler, goToUrl} from './utils.js';
import ImageCropper from './imageCropper';
import $ from 'jquery';
import 'fittextjs';
import 'bootstrap';

const configs = JSON.parse(document.getElementById('configs').textContent);
const cropper = new ImageCropper();

function failCb(data) {
    $(configs.formContainerSelector).html(data.html);
    addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
    cropper.init(goToUrl, failCb);
}

function tokenSuccessCb(data) {
    $('#id_uuid').val(data.html);
}

getModalDataAjax(configs.deleteUrl).then(() => {
    addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
    addAjaxFormHandler('#tokenForm', tokenSuccessCb, () => null);
    cropper.init(goToUrl, failCb);
});

$('#name').fitText(0.8, {maxFontSize: 30});
