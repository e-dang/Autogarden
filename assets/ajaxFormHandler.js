import $ from 'jquery';
import ImageCropper from './imageCropper';
import {goToUrl, createAddFormListeners} from './utils';

class AjaxFormHandler {
    constructor({formContainerSelector, formSelector}) {
        this.formSelector = formSelector;
        this.formContainerSelector = formContainerSelector;
    }

    bind(successCb, failCb) {
        this.successCb = successCb;
        this.failCb = failCb;
    }

    handle(event, extractFormData) {
        const fd = extractFormData(event.target);
        event.preventDefault();
        $.ajax({
            type: $(this.formSelector).attr('method'),
            url: $(this.formSelector).attr('action'),
            data: fd,
            contentType: false,
            processData: false,
            success: this.ajaxResponseHandler.bind(this),
        });
    }

    ajaxResponseHandler(data) {
        if (data.success) {
            this.successCb(data);
        } else {
            $(this.formContainerSelector).html(data.html);
            this.failCb(data);
        }
    }
}

class AjaxImageFormHandler extends AjaxFormHandler {
    addFormListeners() {
        this.failCb();
    }
}

function createAjaxImageFormHandler(configs) {
    const imageFormHandler = new AjaxImageFormHandler(configs);
    const addFormListeners = createAddFormListeners(imageFormHandler, new ImageCropper());
    imageFormHandler.bind(goToUrl, addFormListeners);
    return imageFormHandler;
}

export {AjaxFormHandler, createAjaxImageFormHandler, AjaxImageFormHandler};
