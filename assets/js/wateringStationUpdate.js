import {getModalDataAjax, fitText} from './utils/utils.js';
import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';

const configs = JSON.parse(document.getElementById('configs').textContent);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.deleteUrl).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
