$(function () {
    $("img.lazy").lazyload();
});

$(function () {
    $('#create-report-update').submit(function () {
        var form = $('#create-report-update');
        var form_inputs = $('#create-report-update :input');
        var form_errors = form.find('.error-container');
        var action = form.data('action');

        $.ajax({
            url: action,
            type: 'POST',
            data: form.serialize(),
            beforeSend: function () {
                form_inputs.prop('disabled', true);
                form_errors.empty();
            },
            success: function (data) {
                form_inputs.prop('disabled', true);
                document.location = "#";
                window.location.reload();
            },
            error: function (xhr) {
                form_inputs.prop('disabled', false);
                errors = $.parseJSON(xhr.responseText).errors;
                console.log(errors);
                for (var error in errors) {
                    form.find('.error-container').prepend(
                        '<div class="alert alert-dismissible alert-danger" role="alert">' + errors[error] + '</div>'
                    )
                }
            },
            complete: function (data) {
            }
        });
        return false;
    })

});

/**
 * Other functions to run on pageload;
 */
$(function () {
    /**
     * Language switch.
     */
    $(".lang-choose").click(function () {
        var lang = $(this).find('a').data('lang');
        var next = $('#no-lang-path').data('next');
        var csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: '/i18n/setlang/',
            data: {language: lang, next: next},
            headers: {
                "X-CSRFToken": csrftoken
            }
        }).done(function (result) {
            console.log(result);
            location.href = '/' + lang + next;
        });
    });

    /**
     * When user clicks on report row anywhere on all reports page, go to problem page.
     */
    $('.all-reports-table').mousedown(function (e) {
        switch (e.which) {
            case 1:
                window.location = $(this).find('a').attr('href');
                break;
        }
        return true;
    });


    /**
     * Monitor modal clicks on homepage to close modal automatically after city is clicked.
     */
    $('#city-boxes li').each(function () {
        $(this).click(function () {
            $('#changecityModal').modal('hide');
        });
    });

    /**
     * Blue line animation on top.
     */
    $(function () {
        $('#cut').animate({
            width: 830 + 'px',
            marginLeft: -415 + 'px'
        }, 1400);
    });


    /**
     * Home round box onclick
     */
    $(function () {
        $('.home-round-inner').click(function () {
            window.location.href = $(this).find('a')[0]['href'];
        })
    })
});

/**
 * Animates blue cut on top of the page
 */
window.onbeforeunload = function () {
    $('#cut').animate({
        width: 10 + 'px',
        marginLeft: -20 + 'px'
    }, 400);
};


$(function () {
    $('#contact-page').css({
        'min-height': window.innerHeight
    });
});


$(function () {
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd'
    });
});


function FMS() {
    if (arguments.callee._singletonInstance)
        return arguments.callee._singletonInstance;
    arguments.callee._singletonInstance = this;

    this.current_lang = '/' + window.location.href.split('/')[3];
    this.is_authenticated = false;

};

fms = new FMS();