import {createAjaxImageFormHandler} from './ajaxFormHandler';
import 'bootstrap';

const configs = {
    imgInputSelector: '#id_image',
    cropBtnSelector: '#cropBtn',
    resetBtnSelector: '#resetBtn',
    imgContainerSelector: '#imageContainer',
    formSelector: '#newGardenForm',
    formContainerSelector: '.modal-body',
};

const formHandler = createAjaxImageFormHandler(configs);
formHandler.addFormListeners();
