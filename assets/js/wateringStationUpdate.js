import {getModalDataAjax, fitText, getConfigData} from './utils/utils.js';
import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';

const configs = getConfigData();
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.deleteUrl).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
