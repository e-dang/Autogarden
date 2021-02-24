function formAjaxSubmit(formId) {
    const form = $(formId);
    form.on('submit', (event) => {
        event.preventDefault();
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: (data) => {
                if (data.success) {
                    window.location = data.url;
                } else {
                    form.html(data.html);
                }
            },
        });
    });
}
