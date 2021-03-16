import {addAjaxFormHandler} from './utils.js';
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

function successCb(data) {
    window.location = data.url;
}

function failCb(data) {
    $('.modal-body').html(data.html);
    addAjaxFormHandler(configs.formSelector, successCb, failCb);
    new ImageCropper(successCb, failCb).init();
}

addAjaxFormHandler(configs.formSelector, successCb, failCb);
new ImageCropper(successCb, failCb).init();
