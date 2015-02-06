function FMSForms () {
    if (arguments.callee._singletonInstance)
        return arguments.callee._singletonInstance;
    arguments.callee._singletonInstance = this;

    /**
     * Loads problem submit form and changes map position. Called by event when map is idle.
     */
    this.loadDivs = function () {
        var mapCanvas = $("#map_canvas");
        mapCanvas.append('<div id="blue-overlay-200"></div>');
        mapCanvas.after('<div id="box-reports-transpar-logo"></div>');
    };

    /**
     * Makes element visible with smooth transition
     */
    this.makeVisible = function (selector) {
        $('#' + selector).css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);
    };


    /**
     * Process forms on homepage
     * @param form Form to process. This makes step-forms possible
     * @param other_data additional data to pass to form processors. Like email
     */
    this.processForms = function (form, other_data) {

        // All available forms.
        var forms = {
            'check_email_form': 'check-email',
            'ajax_login_form': 'ajax-login',
            'new_report_full': 'new-report-full',
            'new_report_user': 'new-report-user'
        };
        form = form || 'startFormCheck';
        other_data = other_data || {};

        // Form strategy
        switch (form) {
            case 'startFormCheck':
                this.startFormCheck(forms);
                break;
            case forms.check_email_form:
                $('#' + forms.ajax_login_form).hide();
                this.checkEmail(forms);
                break;
            case forms.ajax_login_form:
                $('#' + forms.check_email_form).hide();
                this.ajaxLogin(forms, other_data);
                break;
            case forms.new_report_full:
                $('#' + forms.check_email_form).hide();
                this.newReportFull(forms, other_data);
                break;
            case forms.new_report_user:
                $('#' + forms.check_email_form).hide();
                $('#' + forms.ajax_login_form).hide();
                this.newReportUser(forms, other_data);
                break;
        }

    };

    this.startFormCheck = function (forms) {
        if (fms.is_authenticated) {
            this.processForms(forms.new_report_user);
        } else {
            this.processForms(forms.check_email_form);
        }
    };

    /**
     * Check if user email exists. Passes result to callback
     * @param forms Forms object.
     */
    this.checkEmail = function (forms) {
        this.makeVisible(forms.check_email_form);
        var scope = this;

        $('#' + forms.check_email_form).submit(function (event) {
            event.preventDefault();
            var email = $(this).serializeArray()[0].value;

            $.get(fms.current_lang + '/user/email-exists', {'email': email}, function (data) {
                scope._checkEmailCallback(data, forms, email);
            });
        });
    };

    /**
     * Process response and handle next step accordingly.
     *
     * @param data Response data from email existence checker
     * @param forms Forms object
     * @param email Email which was checked
     * @private
     */
    this._checkEmailCallback = function (data, forms, email) {
        var scope = this;
        if (data.email_exists) {
            scope.processForms(forms.ajax_login_form, data = {'email': email});
        } else {
            scope.processForms(forms.new_report_full, data = {'email': email})
        }
    };

    /**
     * Ajax login form process
     */
    this.ajaxLogin = function (forms, data) {
        this.makeVisible(forms.ajax_login_form);
        var scope = this;
        var cached_form = $('#' + forms.ajax_login_form);
        if (data.email) {
            cached_form.find('#login_email').val(data.email).attr({'readonly': 'True'});
            cached_form.find('#id_password').focus();
        }
        cached_form.submit(function (event) {
            cached_form.css({'cursor': 'progress'});
            cached_form.find('button').attr({'disabled': 'disabled'});
            event.preventDefault();

            $.ajax({
                type: "POST",
                url: fms.current_lang + "/user/ajax/login/",
                headers: {
                    "X-CSRFToken": $.cookie('csrftoken')
                },
                data: cached_form.serialize(),
                success: function (data) {
                    scope._ajaxLoginCallback(forms, data)
                }
            });
        });

    };

    this._ajaxLoginCallback = function (forms, data) {
        var cached_form = $('#' + forms.ajax_login_form);
        var error_container = cached_form.find('.error-container');
        var scope = this;

        if (!data.errors) {
            $('#preform').find("input[name='csrfmiddlewaretoken']").each(function () {
                console.log($(this));
                $(this).val($.cookie('csrftoken'));
            });
            scope.processForms(forms.new_report_user, data);
        } else {
            error_container.html('');
            $.each(data.errors, function (i, val) {
                console.log(data);
                error_container.append(
                    '<div class="alert alert-danger" role="alert">' + val + '</div>'
                )
            });
            cached_form.css({'cursor': 'default'});
            cached_form.find('button').removeAttr('disabled');
        }
    };

    /**
     * Full report form. I.e. user is not registered
     * @param forms
     * @param data
     */
    this.newReportFull = function (forms, data) {
        var cached_form = $('#new-report');
        cached_form.css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);

        cached_form.find('#id_report_start-email').val(data.email);

        // Mark required fields
        cached_form.validate({
            ignore: "",
            rules: {
                title: "required",
                street: "required",
                first_name: "required",
                last_name: "required",
                phone: "required",
                email: "required",
                lon: "required",
                lat: "required"
            },
            messages: {
                title: gettext("Please enter problem title"),
                street: gettext("Enter street"),
                lon: "Set point on map!"
            },
            submitHandler: function (form) {
                form.submit();
            }
        });
    };

    /**
     * User form. I.e. user is registered and only some fields are required
     * @param forms
     * @param data
     */
    this.newReportUser = function (forms, data) {
        $('#new-report').css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);
        $('.user-hidden').css({'display': 'none'}).attr({'disabled': 'disabled', 'read-only': true})

        // Mark required fields
        $('#new-report').validate({
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

};

fmsforms = new FMSForms();