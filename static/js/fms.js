var FMS = (function () {
    'use strict';
    var pub = {};

    pub.current_lang = '/' + window.location.href.split('/')[3];
    pub.is_authenticated = false;

    function jqueryInit() {
        $(document).ready(function () {
            pub.lazyLoad();
            pub.languageSwitch();
            pub.clickableReportListRows();
            pub.homeCityModals();
            pub.blueLineAnimation();
            pub.clickableHomeCounts();
            pub.datePicker();
            pub.blueLineUnload();
            pub.contactPageFixHeight();
        });

    }

    pub.lazyLoad = function () {
        $("img.lazy").lazyload();
    };

    pub.languageSwitch = function () {
        $(".lang-choose").click(function () {
            var lang = $(this).find('a').data('lang'),
                next = $('#no-lang-path').data('next'),
                csrftoken = $.cookie('csrftoken');

            $.ajax({
                url: '/i18n/setlang/',
                data: {language: lang, next: next},
                headers: {
                    "X-CSRFToken": csrftoken
                }
            }).done(function (result) {
                location.href = '/' + lang + next;
            });
        });
    };

    pub.clickableReportListRows = function () {
        $('.all-reports-table').mousedown(function (e) {
            switch (e.which) {
                case 1:
                    window.location = $(this).find('a').attr('href');
                    break;
            }
            return true;
        });
    };

    pub.homeCityModals = function () {
        $('#city-boxes li').each(function () {
            $(this).click(function () {
                $('#changecityModal').modal('hide');
            });
        });
    };

    pub.blueLineAnimation = function () {
        $(function () {
            $('#cut').animate({
                width: 830 + 'px',
                marginLeft: -415 + 'px'
            }, 1400);
        });
    };

    pub.blueLineUnload = function () {
        window.onbeforeunload = function () {
            $('#cut').animate({
                width: 10 + 'px',
                marginLeft: -20 + 'px'
            }, 400);
        };
    };

    pub.clickableHomeCounts = function () {
        $(function () {
            $('.home-round-inner').click(function () {
                window.location.href = $(this).find('a')[0]['href'];
            });
        });
    };

    pub.datePicker = function () {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd'
        });
    };

    pub.contactPageFixHeight = function () {
        $('#contact-page').css({
            'min-height': window.innerHeight
        });
    };

    jqueryInit();
    return pub;
}());

$(function () {
    'use strict';
    // TODO: Move this to fms.forms.js
    $('#create-report-update').submit(function () {
        var form = $('#create-report-update'),
            form_inputs = $('#create-report-update :input'),
            form_errors = form.find('.error-container'),
            action = form.data('action');

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
                var errors = $.parseJSON(xhr.responseText).errors,
                    i;
                for (i = 0; i < errors.length; i++) {
                    form.find('.error-container').prepend(
                        '<div class="alert alert-dismissible alert-danger" role="alert">' + errors[i] + '</div>'
                    );
                }
            },
            complete: function (data) {
            }
        });
        return false;
    });

});