import {createAjaxImageFormHandler} from './utils/ajaxFormHandler';
import ImageRotator from './utils/imageRotator';

const configs = {
    formSelector: '#newGardenForm',
};
new ImageRotator().begin();

const formHandler = createAjaxImageFormHandler(configs);
formHandler.addFormListeners();
