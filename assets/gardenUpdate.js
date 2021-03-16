import {getModalDataAjax, addAjaxFormHandler, goToUrl} from './utils.js';
import ImageCropper from './imageCropper';
import $ from 'jquery';
import 'fittextjs';
import 'bootstrap';

const configs = JSON.parse(document.getElementById('configs').textContent);

function failCb(data) {
    $(configs.formContainerSelector).html(data.html);
    addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
    new ImageCropper(goToUrl, failCb).init();
}

function tokenSuccessCb(data) {
    $('#id_uuid').val(data.html);
}

getModalDataAjax(configs.deleteUrl).then(() => {
    addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
    addAjaxFormHandler('#tokenForm', tokenSuccessCb, () => null);
    new ImageCropper(goToUrl, failCb).init();
});

$('#name').fitText(0.8, {maxFontSize: 30});
