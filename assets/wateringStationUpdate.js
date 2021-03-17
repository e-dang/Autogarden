import {getModalDataAjax} from './utils.js';
import {createAjaxImageFormHandler} from './ajaxFormHandler';
import $ from 'jquery';
import 'fittextjs';
import 'bootstrap';

const configs = JSON.parse(document.getElementById('configs').textContent);
const imageFormHandler = createAjaxImageFormHandler(configs);

getModalDataAjax(configs.deleteUrl).then(() => {
    imageFormHandler.addFormListeners();
});

$('#name').fitText(0.8, {maxFontSize: 30});
