import {getModalDataAjax, addAjaxFormHandler, getFormData, fitText, getConfigData} from './utils/utils.js';
import {AjaxFormHandler, createAjaxImageFormHandler} from './utils/ajaxFormHandler';
import $ from 'jquery';

function successCb(data) {
    $('#id_uuid').val(data.html);
}

const tokenConfigs = getConfigData('tokenConfigs');
const gardenConfigs = getConfigData('gardenConfigs');
const formHandler = new AjaxFormHandler(tokenConfigs);
formHandler.bind(successCb, undefined);
const imageFormHandler = createAjaxImageFormHandler(gardenConfigs);

getModalDataAjax(gardenConfigs);
imageFormHandler.addFormListeners();
addAjaxFormHandler(formHandler, getFormData);
fitText('#name');
