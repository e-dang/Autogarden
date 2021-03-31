import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';

const configs = {
    formSelector: '#newGardenForm',
};

$.ready(() => {
    const formHandler = createAjaxImageFormHandler(configs);
    formHandler.addFormListeners();
});
