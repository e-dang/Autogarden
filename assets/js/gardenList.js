import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';

const configs = {
    formSelector: '#newGardenForm',
};

const formHandler = createAjaxImageFormHandler(configs);
formHandler.addFormListeners();
