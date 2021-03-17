import {getModalDataAjax, addAjaxFormHandler, getFormData} from './utils.js';
import {AjaxFormHandler, createAjaxImageFormHandler} from './ajaxFormHandler';
import $ from 'jquery';
import 'fittextjs';
import 'bootstrap';

function successCb(data) {
    $('#id_uuid').val(data.html);
}

const configs = JSON.parse(document.getElementById('configs').textContent);
const formHandler = new AjaxFormHandler({formSelector: '#tokenForm'});
formHandler.bind(successCb, undefined);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.deleteUrl).then(() => {
    imageFormHandler.addFormListeners();
    addAjaxFormHandler(formHandler, getFormData);
});

$('#name').fitText(0.8, {maxFontSize: 30});
