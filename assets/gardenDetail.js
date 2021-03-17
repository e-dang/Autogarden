import {getModalDataAjax} from './utils.js';
import {createAjaxImageFormHandler} from './ajaxFormHandler';

const configs = JSON.parse(document.getElementById('configs').textContent);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.url).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
