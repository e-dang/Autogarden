import {getModalDataAjax, addAjaxFormHandler, getFormData, fitText, getConfigData} from './utils/utils.js';
import {AjaxFormHandler, createAjaxImageFormHandler} from './utils/ajaxFormHandler';

function successCb(data) {
    $('#id_uuid').val(data.html);
}

const configs = getConfigData();
const formHandler = new AjaxFormHandler({formSelector: '#tokenForm'});
formHandler.bind(successCb, undefined);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs).then(() => {
    imageFormHandler.addFormListeners();
    addAjaxFormHandler(formHandler, getFormData);
});

fitText('#name');
