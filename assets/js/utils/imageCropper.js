import $ from 'jquery';
import 'jquery-cropper';
import {addAjaxFormHandler} from './utils';

class ImageCropper {
    constructor({
        width = 200,
        height = 200,
        imgInputSelector = '#id_image',
        imgContainerSelector = 'div.photo-container',
        cropBtnSelector = 'input[name="crop"]',
        resetBtnSelector = 'input[name="reset"]',
    }) {
        this.width = width;
        this.height = height;
        this.imgInputSelector = imgInputSelector;
        this.imgContainerSelector = imgContainerSelector;
        this.cropBtnSelector = cropBtnSelector;
        this.resetBtnSelector = resetBtnSelector;
        this.imgClass = 'cropper-photo';
        this.cropper = null;
    }

    init(formHandler) {
        this._getElements();

        this.imgInput.on('change', (event) => {
            this.cropBtn.attr('hidden', false);
            this.resetBtn.attr('hidden', true);

            this.imgContainer.html(this._getImageTag(event));
            this._resetCropper();

            this._handleCrop(formHandler);
            this._handleReset(event);
        });
    }

    _getElements() {
        this.imgInput = $(this.imgInputSelector);
        this.imgContainer = $(this.imgContainerSelector);
        this.cropBtn = $(this.cropBtnSelector);
        this.resetBtn = $(this.resetBtnSelector);
    }

    _toggleCropResetBtns() {
        this.cropBtn.attr('hidden', !this.cropBtn.attr('hidden'));
        this.resetBtn.attr('hidden', !this.resetBtn.attr('hidden'));
    }

    _getImageTag(event) {
        const imgData = event.target.files[0];
        const url = URL.createObjectURL(imgData);
        return `<img class="${this.imgClass}" src="${url}">`;
    }

    _resetCropper() {
        const img = $(`img.${this.imgClass}`);
        img.cropper({
            aspectRatio: 1,
            scalable: false,
            zoomable: false,
            dragMode: 'none',
        });
        this.cropper = img.data('cropper');
    }

    _handleCrop(formHandler) {
        this.cropBtn.on('click', (event) => {
            const canvas = this.cropper.getCroppedCanvas({
                width: this.width,
                height: this.height,
                imageSmoothingQuality: 'high',
            });
            this.imgContainer.html(canvas);
            this._toggleCropResetBtns();
            $(formHandler.formSelector).off();

            canvas.toBlob((blob) => {
                addAjaxFormHandler(formHandler, (form) => this._getImageFormData(form, blob));
            });
        });
    }

    _getImageFormData(form, blob) {
        const fd = new FormData(form);
        const filename = $(`#script-${this.imgInputSelector.substring(1)}`)
            .parent()
            .children('.custom-file-label')
            .text();
        fd.append('image', blob, filename);
        return fd;
    }

    _handleReset(imgChangeEvent) {
        this.resetBtn.on('click', (event) => {
            this._toggleCropResetBtns();
            this.imgContainer.html(this._getImageTag(imgChangeEvent));
            this._resetCropper();
        });
    }
}

export default ImageCropper;
