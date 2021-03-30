import {getModalDataAjax, getConfigData, fitText} from './utils/utils.js';
import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';
import ImageRotator from './utils/imageRotator';

const configs = getConfigData();
const imageFormHandler = createAjaxImageFormHandler(configs);
new ImageRotator().begin();

getModalDataAjax(configs).then(() => {
    imageFormHandler.addFormListeners();
});

fitText('#name');
