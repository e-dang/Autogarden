import $ from 'jquery';
import 'jquery-cropper';
import {addAjaxFormHandler} from './utils';

class ImageCropper {
    constructor(
        imgInputSelector = '#id_image',
        imgContainerSelector = '#imageContainer',
        cropBtnSelector = '#cropBtn',
        resetBtnSelector = '#resetBtn',
    ) {
        this.imgInputSelector = imgInputSelector;
        this.imgContainerSelector = imgContainerSelector;
        this.cropBtnSelector = cropBtnSelector;
        this.resetBtnSelector = resetBtnSelector;
        this.imgClass = 'cropper-photo';
        this.cropper = null;
    }

    init(successCb, failCb) {
        this._getElements();

        this.imgInput.on('change', (event) => {
            this.cropBtn.attr('hidden', false);
            this.resetBtn.attr('hidden', true);

            this.imgContainer.html(this._getImageTag(event));
            this._resetCropper();

            this._handleCrop(successCb, failCb);
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

    _handleCrop(successCb, failCb) {
        this.cropBtn.on('click', (event) => {
            const canvas = this.cropper.getCroppedCanvas({width: 200, height: 200});
            this.imgContainer.html(canvas);
            this._toggleCropResetBtns();

            canvas.toBlob((blob) => {
                addAjaxFormHandler(configs.formSelector, successCb, failCb, (form) => {
                    const filename = $(`#script-${configs.imgInputSelector.substring(1)}`)
                        .parent()
                        .children('.custom-file-label')
                        .text();
                    const fd = new FormData(form);
                    fd.append('image', blob, filename);
                    return fd;
                });
            });
        });
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
