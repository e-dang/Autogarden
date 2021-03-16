import {addAjaxFormHandler, goToUrl} from './utils.js';
import ImageCropper from './imageCropper';
import $ from 'jquery';
import 'bootstrap';

const configs = {
    imgInputSelector: '#id_image',
    cropBtnSelector: '#cropBtn',
    resetBtnSelector: '#resetBtn',
    imgContainerSelector: '#imageContainer',
    formSelector: '#newGardenForm',
};

function failCb(data) {
    $('.modal-body').html(data.html);
    addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
    new ImageCropper(goToUrl, failCb).init();
}

addAjaxFormHandler(configs.formSelector, goToUrl, failCb);
new ImageCropper(goToUrl, failCb).init();
