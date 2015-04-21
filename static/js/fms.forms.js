var FMSForms = (function () {
    'use strict';
    var pub = {};

    /**
     * Loads problem submit form and changes map position. Called by event when map is idle.
     */
    pub.loadDivs = function () {
        var mapCanvas = $("#map_canvas");
        mapCanvas.append('<div id="blue-overlay-200"></div>');
        mapCanvas.after('<div id="box-reports-transpar-logo"></div>');
    };

    /**
     * Makes element visible with smooth transition
     */
    pub.makeVisible = function (selector) {
        selector.css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);
    };


    /**
     * Process forms on homepage
     */
    pub.processForms = function () {
        var self = this;
        if (FMS.is_authenticated) {
            this.processForms(forms.new_report);
        } else {
            this.loginOrRegister();
        }
    };

    pub.loginOrRegister = function () {
        var self = this,
            form = $('#ajax-login'),
            help_text = gettext('Please login to your account or <a href="/user/register/">create new one</a> in order to create report.');
        pub.makeVisible(form);
        $('#help-text').html(help_text);

        form.validate({
            ignore: "",
            errorClass: 'has-error',
            highlight: function (element, errorClass) {
                $(element).parent().addClass(errorClass);
            },
            rules: {
                username: "required",
                password: "required"
            },
            messages: {
                username: gettext("Invalid email"),
                password: gettext("Please enter the password")
            },
            submitHandler: function () {
                form.css({'cursor': 'progress'});
                form.find('button').attr({'disabled': 'disabled'});

                $.ajax({
                    type: "POST",
                    url: FMS.current_lang + "/user/ajax/login/",
                    headers: {
                        "X-CSRFToken": $.cookie('csrftoken')
                    },
                    data: form.serialize(),
                    success: function (data) {
                        pub._ajaxLoginCallback(form, data);
                    }
                });
            }
        });

    };


    pub._ajaxLoginCallback = function (form, data) {
        var self = this,
            error_container = form.find('.form-error');

        if (!data.errors) {
            $('#preform').find("input[name='csrfmiddlewaretoken']").each(function () {
                $(this).val($.cookie('csrftoken'));
            });
            pub.newReport(form);
        } else {
            pub.makeVisible(error_container);
            error_container.html('');
            $.each(data.errors, function (i, val) {
                console.log(val);
                error_container.append(val.message);
            });
            form.css({'cursor': 'default'});
            form.find('button').removeAttr('disabled');
        }
    };

    /**
     * User form. I.e. user is registered
     * @param prev_form
     */
    pub.newReport = function (prev_form) {
        var form = $('#new-report');

        form.css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);

        // Mark required fields
        form.validate({
            ignore: "",
            rules: {
                title: "required",
                street: "required"
            },
            messages: {
                title: gettext("Please enter problem title"),
                street: gettext("Enter street")
            },
            submitHandler: function (form) {
                form.submit();
            }
        });
    };

    return pub;

}());