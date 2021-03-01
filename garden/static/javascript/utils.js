function formAjaxSubmit(formId) {
    $(formId).on('submit', (event) => {
        const fd = new FormData(event.target);
        event.preventDefault();
        $.ajax({
            type: $(formId).attr('method'),
            url: $(formId).attr('action'),
            data: fd,
            contentType: false,
            processData: false,
            success: (data) => {
                if (data.success) {
                    window.location = data.url;
                } else {
                    $('.modal-body').html(data.html);
                    formAjaxSubmit(formId);
                }
            },
        });
    });
}

function getModalDataAjax(url) {
    $(document).ready(() => {
        $.ajax({
            type: 'get',
            url: url,
            success: (data) => {
                $('.modal-body').html(data.html);
            },
        });
    });
}
