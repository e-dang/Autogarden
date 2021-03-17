import {getModalDataAjax} from './utils/utils.js';
import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';

const configs = JSON.parse(document.getElementById('configs').textContent);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.url).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
