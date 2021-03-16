import {addCropImageHandler, addAjaxFormHandler} from './utils.js';
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
    addCropImageHandler(configs, successCb, failCb);
}

addAjaxFormHandler(configs.formSelector, successCb, failCb);
addCropImageHandler(configs, successCb, failCb);
