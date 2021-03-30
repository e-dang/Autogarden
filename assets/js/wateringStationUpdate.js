import {getModalDataAjax, fitText, getConfigData} from './utils/utils.js';
import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';
import ImageRotator from './utils/imageRotator';

new ImageRotator().begin();
const configs = getConfigData();
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
