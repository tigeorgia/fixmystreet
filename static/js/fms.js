//Icons for markers
GmapMarkerIcons = {
    dragme: "/static/images/marker/default/marker.png",
    green: "/static/images/marker/default/green.png",
    red: "/static/images/marker/default/red.png",
    yellow: "/static/images/marker/default/yellow.png"
};

// Object which stores all markers
GmapMarkers = {};

/**
 * Map functions to run on pageload;
 */
$(function () {
    if (google.maps) {
        /**
         * Homepage function which monitors for click on cities on homepage and sends data to moveToCity function.
         */
        $('.cities-moveto li').each(function () {
            $(this).click(function () {
                if ($(this).data('city')) {
                    var city = $(this).data('city');
                    $('#change-city').show();
                    FMS.moveToCity(city);
                }
            });
        });
    }
});

/**
 * Other functions to run on pageload;
 */
$(function () {
    /**
     * Language switch.
     * TODO: It's not really obvious that dropdown stands for language. Change template to more intuitive way
     */
    $(".lang-choose").click(function () {
        var lang = $(this).find('a').data('lang');
        var next = $('#no-lang-path').data('next');
        $.post("/i18n/setlang/", {language: lang, next: next})
            .done(function () {
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

// Geocoding on homepage
$(document).on('submit', '.address-search-form', function getLocation() {
    var inputs = $(this).serializeArray();
    var address = inputs[0].value.trim().replace(' ', '+');
    var city = inputs[1].value;

    geocoder.geocode({
        address: address + ', ' + city
    }, FMS.panToStreet);

    return false;

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


var FMS = ( function () {

    var fn = {};
    current_lang = '/' + window.location.href.split('/')[3];

    /**
     * Loads problem submit form and changes map position. Called by event when map is idle.
     */
    fn.loadDivs = function () {
        var mapCanvas = $("#map_canvas");
        mapCanvas.append('<div id="blue-overlay-200"></div>');
        mapCanvas.after('<div id="box-reports-transpar-logo"></div>');
    };

    /**
     * Makes element visible with smooth transition
     */
    fn.makeVisible = function (selector) {
        $('#'+selector).css({'display': 'block', 'visibility': 'visible'}).animate({
            opacity: 1
        }, 1300);
    };


    /**
     * Process forms on homepage
     * @param form Form to process. This makes step-forms possible
     * @param other_data additional data to pass to form processors. Like email
     */
    fn.processForms = function (form, other_data) {

        // All available forms.
        var forms = {
            'check_email_form': 'check-email',
            'ajax_login_form': 'ajax-login',
            'new_report_full': 'new-report-full',
            'new_report_user': 'new-report-user'
        };
        form = form || forms.check_email_form;
        other_data = other_data || {};
        console.log('processing forms');

        // Form strategy
        switch (form) {
            case forms.check_email_form:
                $('#'+forms.ajax_login_form).hide();
                this.checkEmail(forms);
                break;
            case forms.ajax_login_form:
                $('#'+forms.check_email_form).hide();
                this.ajaxLogin(forms, other_data);
                break;
            case forms.new_report_full:
                $('#'+forms.check_email_form).hide();
                this.newReportFull(forms, other_data);
                break;
            case forms.new_report_user:
                $('#'+forms.ajax_login_form).hide();
                this.newReportUser(forms, other_data);
                break;
        }

    };

    /**
     * Check if user email exists. Passes result to callback
     * @param forms Forms object.
     */
    fn.checkEmail = function (forms) {
        this.makeVisible(forms.check_email_form);

        $('#'+forms.check_email_form).submit(function (event) {
            event.preventDefault();
            var email = $(this).serializeArray()[0].value;

            $.get(current_lang + '/user/email-exists', {'email': email}, function (data) {
                FMS._checkEmailCallback(data, forms, email);
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
    fn._checkEmailCallback = function (data, forms, email) {
        if (data.email_exists) {
            FMS.processForms(forms.ajax_login_form, data={'email': email});
        } else {
            FMS.processForms(forms.new_report_full, data={'email': email})
        }
    };

    /**
     * Ajax login form process
     */
    fn.ajaxLogin = function (forms, data) {
        this.makeVisible(forms.ajax_login_form);
        var cached_form = $('#'+forms.ajax_login_form);
        if (data.email){
            cached_form.find('#login_email').val(data.email);
            cached_form.find('#id_password').focus();
        }
        cached_form.submit(function(event){
            cached_form.css({'cursor': 'progress'});
            cached_form.find('button').attr({'disabled': 'disabled'});
            event.preventDefault();

            $.ajax({
                type: "POST",
                url: current_lang + "/user/ajax/login/",
                data: cached_form.serialize(),
                success: function(data){
                    FMS._ajaxLoginCallback(forms, data)
                }
            });
        });

    };

    fn._ajaxLoginCallback = function (forms, data) {
        var cached_form = $('#' + forms.ajax_login_form);
        var error_container = cached_form.find('.error-container');

        if (!data.errors){
            FMS.processForms(forms.new_report_user, data)
        } else {
            error_container.html('');
            $.each(data.errors, function(i, val){
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
    fn.newReportFull = function (forms, data) {
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
    fn.newReportUser = function (forms, data) {
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

    /*
     * Lats and Lngs of cities
     * TODO: Move this to model
     */
    fn.getCityData = function (cityName) {
        var data = {
            center: {
                'lat': null,
                'lng': null,
                'LatLng': {}
            },
            bounds: {
                sw: {
                    'lat': null,
                    'lng': null,
                    'LatLng': {}
                },
                ne: {
                    'lat': null,
                    'lng': null,
                    'LatLng': {}
                }
            }
        };
        switch (cityName.toLocaleLowerCase()) {
            case 'tbilisi':
                data.center = {
                    'lat': 41.708484,
                    'lng': 44.79847
                };
                data.bounds.sw.lat = 41.83418996702034;
                data.bounds.sw.lng = 41.62922108610059;
                data.bounds.ne.lat = 44.72675802558592;
                data.bounds.ne.lng = 45.216336272656235;
                break;

            case 'batumi':
                data.center.lat = 41.633086;
                data.center.lng = 41.633291;
                break;

            case 'kutaisi':
                data.center.lat = '42.252473';
                data.center.lng = '42.695875';
                break;

            case 'zugdidi':
                data.center.lat = '42.503807';
                data.center.lng = '41.86203';
                break;
        }
        data.center.LatLng = new google.maps.LatLng(data.center.lat, data.center.lng);
        data.bounds.sw.latlng = new google.maps.LatLng(data.bounds.sw.lat, data.bounds.sw.lng);
        data.bounds.ne.latlng = new google.maps.LatLng(data.bounds.ne.lat, data.bounds.ne.lng);
        data.bounds.LatLngBounds = new google.maps.LatLngBounds(google.maps.LatLng(data.bounds.sw.latlng, data.bounds.ne.latlng));
        return data;
    };

    fn.mapResize = function () {
        var window_height = $(window).height();
        var window_width = $(window).width();
        if (window_height < 600 && window_width < 1005)
            $('#map_canvas').css({
                'height': window_height - 120
            });
    };

    /*Resizes google map if nesessary. Without this, map breaks. Poll it in case of animation
     */
    fn.checkSize = function () {
        google.maps.event.trigger(map, 'resize');
    };

    /*
     * Moves map to city center when clicking on cities on homepage
     */
    fn.moveToCity = function (cityName) {
        cityName = cityName || 'Tbilisi';
        var cityCenter, cityData;

        $('.choose-city.hidden-lg').remove();
        this.checkSize();
        $('#desk-city').empty();
        cityData = this.getCityData(cityName);
        cityCenter = cityData.center.LatLng;
        map.panTo(cityCenter);
        map.setZoom(17);
        this.fixCenter(true);

        var left_img = $('#left-image');
        var left_width = left_img.width() - 10;

        $('#map_canvas').animate({
            marginLeft: '-' + left_width
        }, 800, function () {
            $('#left-image').remove();

            $('.start-hidden').css({'visibility': 'visible'}).animate({
                opacity: 1
            }, 1300);

            FMS.processForms();

            left_img.animate({
                opacity: 0,
                marginLeft: -1600
            }, 800, function () {
                FMS.checkSize();
            });

            $('.choose-city.visible-lg').remove();

        });

        $('.geocode-city').val(cityName);
        $('#id-city').val(cityName);
        this.addressMarker();
    };

    /*
     Creates marker and adds them to GmapMarkers object
     */
    fn.addMarker = function (name, latlng, opts) {
        var timestamp = new Date().valueOf(); //Generate unique name if it's not supplied
        var params = {};
        opts = opts || {};

        //Set defaults
        params.name = name || "marker_" + String(timestamp);
        params.position = latlng || map.getCenter();
        params.draggable = opts.draggable || false;
        params.animation = opts.animation || google.maps.Animation.DROP;
        params.icon = opts.icon || GmapMarkerIcons.dragme;
        params.title = opts.title || "Marker";

        //Create marker and store in global GmapMarkers object
        GmapMarkers[params.name] = new google.maps.Marker({
            position: params.position,
            map: map,
            draggable: params.draggable,
            animation: params.animation,
            icon: params.icon,
            title: params.title
        });

        // Return marker object
        return GmapMarkers[params.name];
    };

    /*
     Removes marker from map and from global markers array
     */
    fn.removeMarker = function (name) {
        GmapMarkers[name].setMap(null);
        delete GmapMarkers.name
    },

    /**
     * Initial loader of markers. Run when map is idle
     */
        fn.populateMarkers = function () {
            var coords, LatLng, marker, icon;
            var reports = this.getLatestReports();
            var texts = {
                readmore: gettext('Read more...')
            };

            var url = window.location.href;
            var urlArr = url.split("/");
            var protocol = urlArr[0] + "//";
            var domain = urlArr[2];
            var lang = urlArr[3];

            for (var i = 0; i < reports.length; i++) {
                if (reports[i]['status'] == 'fixed') {
                    icon = GmapMarkerIcons['green'];
                } else if (reports[i]['status'] == 'not-fixed') {
                    icon = GmapMarkerIcons['red'];
                } else if (reports[i]['status'] == 'in-progress') {
                    icon = GmapMarkerIcons['yellow'];
                }
                coords = reports[i]['point']['coordinates'];
                LatLng = new google.maps.LatLng(coords[1], coords[0]);
                marker = FMS.addMarker('id_marker_' + reports[i]['id'], LatLng, {icon: icon});
                marker.description = reports[i]['description'] + '<br><a href="' + protocol + domain + '/' +
                lang + '/reports/' + reports[i]['id'] + '">' + texts.readmore + '</a>';

                google.maps.event.addListener(marker, 'click', function () {
                    infowindow.setContent(this.description);
                    infowindow.open(map, this);
                })
            }
        };

    /**
     * Hides or shows problem markers on a map
     * @param {boolean} visible Shows markers by default, hides if false
     */
    fn.markersVisible = function (visible) {
        visible = visible || true;
        var exceptions = ['address_marker']; // Don't hide main marker
        for (var marker in GmapMarkers) {
            if (GmapMarkers.hasOwnProperty(marker) && exceptions.indexOf(marker) < 0) {
                if (visible) {
                    GmapMarkers[marker].setVisible(false);
                } else {
                    GmapMarkers[marker].setVisible(true);
                }
            }
        }
    };

    /**
     * Gets latest reports in json format
     */
    fn.getLatestReports = function () {
        var result = '';
        $.ajax({
            url: 'ajax/latest-reports',
            async: false,
            dataType: 'json',
            success: function (data) {
                result = data;
            }
        });
        return result;
    };

    /**
     * Blue marker, which is draggable and used for reporting a problem
     */
    fn.addressMarker = function () {
        var center = map.getCenter(); // Get center of the map where user is

        //If marker is already there, remove it and make it again. Otherwise it won't work
        if (typeof GmapMarkers['address_marker'] == 'undefined') {
            this.addMarker('address_marker', center, {draggable: true, animation: google.maps.Animation.BOUNCE});
        } else {
            this.removeMarker('address_marker');
            this.addMarker('address_marker', center, {draggable: true});
        }

        //Populate hidden input fields for problem reporting on homepage with lonlat data.
        //TODO: Change input to one field. I.e. not separate lat and lon, but one single POINT geom field.
        google.maps.event.addListener(GmapMarkers['address_marker'], "dragend", function () {
            GmapMarkers['address_marker'].setAnimation(google.maps.Animation.BOUNCE);

            $('input[name=report_start-lat]').val(GmapMarkers['address_marker'].getPosition().lat().toString());
            $('input[name=report_start-lon]').val(GmapMarkers['address_marker'].getPosition().lng().toString());
        });

        google.maps.event.addListener(GmapMarkers['address_marker'], "drag", function () {
            GmapMarkers['address_marker'].setAnimation();
        });

        //Fire dragend event to get initial values
        google.maps.event.trigger(GmapMarkers['address_marker'], "dragend");
    };

    /*
     This function fixes center of the map according to width. Affects only large screens.
     */
    fn.fixCenter = function (inverted) {
        var inverted = inverted || false;
        if (screen.width > 1005) {
            if (inverted) {
                map.panBy(-screen.width / 7, 0);
            } else {
                map.panBy(screen.width / 7, 0);
            }
        }
    };

    fn.panToStreet = function (response, status) {
        var streetObj;

        if (!response || status != google.maps.GeocoderStatus.OK) {
            alert("Something went wrong!");
        } else {
            streetObj = response[0];
            var steetName = streetObj.formatted_address;

            // Zoom in to correctly calculate pixels to move by
            map.setZoom(15);
            map.panTo(streetObj.geometry.location);
            this.fixCenter();
        }
    };

    return fn;

}());


