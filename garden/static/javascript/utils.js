function getModalDataAjax(url, successCb = (data) => null) {
    $(document).ready(() => {
        $.ajax({
            type: 'get',
            url: url,
            success: (data) => {
                $('.modal-body').html(data.html);
                successCb(data);
            },
        });
    });
}

function addAjaxFormHandler(formId, successCb, failCb, getFormData = (form) => new FormData(form)) {
    $(formId).on('submit', (event) => {
        const fd = getFormData(event.target);
        event.preventDefault();
        $.ajax({
            type: $(formId).attr('method'),
            url: $(formId).attr('action'),
            data: fd,
            contentType: false,
            processData: false,
            success: (data) => {
                if (data.success) {
                    successCb(data);
                } else {
                    failCb(data);
                }
            },
        });
    });
}

function addCropImageHandler(configs) {
    const imgInput = $(configs.imgInputSelector);
    const cropBtn = $(configs.cropBtnSelector);
    const resetBtn = $(configs.resetBtnSelector);
    const imgContainer = $(configs.imgContainerSelector);

    imgInput.on('change', (event) => {
        cropBtn.attr('hidden', false);
        resetBtn.attr('hidden', true);

        const imgData = event.target.files[0];
        const url = URL.createObjectURL(imgData);
        imgContainer.html(`<img id="image" class="cropper-photo" src="${url}" alt="">`);

        let img;
        let cropper;
        const resetCropper = () => {
            img = $('#image');
            img.cropper({
                aspectRatio: 1,
                scalable: false,
                zoomable: false,
                dragMode: 'none',
            });
            cropper = img.data('cropper');
        };
        resetCropper();

        cropBtn.on('click', (event) => {
            const width = cropper.getCropBoxData().width;
            const height = cropper.getCropBoxData().height;
            const canvas = cropper.getCroppedCanvas({width: width, height: height});
            imgContainer.html(canvas);
            cropBtn.attr('hidden', true);
            resetBtn.attr('hidden', false);
            $(configs.formSelector).unbind();

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

        resetBtn.on('click', (event) => {
            cropBtn.attr('hidden', false);
            resetBtn.attr('hidden', true);
            cropper.reset();
            imgContainer.html(`<img id="image" class="cropper-photo" src="${url}" alt="">`);
            resetCropper();
        });
    });
}
