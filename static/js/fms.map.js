var FMSMarkers = (function () {
    'use strict';
    var pub = {},
        cluster_opts = {
            gridSize: 20,
            maxZoom: 17,
            imagePath: 'https://google-maps-utility-library-v3.googlecode.com/svn/trunk/markerclustererplus/images/m'
        };
    pub.map = '';
    pub.addressmarker = '';
    pub.markercluster = '';

    pub.initialize = function (map) {
        pub.map = map;
        pub.markercluster = new MarkerClusterer(pub.map, [], cluster_opts);
    };

    pub.markericons = {
        dragme: "/static/images/marker/default/marker.png",
        green: "/static/images/marker/default/green.png",
        red: "/static/images/marker/default/red.png",
        yellow: "/static/images/marker/default/yellow.png"
    };

    /*
     Creates google.maps.Marker
     */
    pub.createMarker = function (name, latlng, opts) {
        var marker = '', params = {},
            timestamp = new Date().valueOf(); //Generate unique name if it's not supplied
        opts = opts || {};

        //Set defaults
        params.name = name || "marker_" + String(timestamp);
        params.position = latlng || pub.map.getCenter();
        params.draggable = opts.draggable || false;
        params.animation = opts.animation || google.maps.Animation.DROP;
        params.icon = opts.icon || pub.markericons.dragme;
        params.title = opts.title || "Marker";

        //Create marker and store in global GmapMarkers object
        marker = new google.maps.Marker({
            position: params.position,
            map: pub.map,
            draggable: params.draggable,
            animation: params.animation,
            icon: params.icon,
            title: params.title
        });

        return marker;
    };


    /**
     * Blue marker, which is draggable and used for reporting a problem
     */
    pub.addressMarker = function () {
        var center = pub.map.getCenter(),
            marker = pub.addressmarker;

        //If marker is already there, remove it and make it again. Otherwise it won't work
        if (!marker) {
            pub.addressmarker = pub.createMarker('address_marker', center, {
                draggable: true,
                animation: google.maps.Animation.BOUNCE
            });
        } else {
            pub.addressmarker.setMap(null);
            pub.addressmarker = pub.createMarker('address_marker', center, {
                draggable: true,
                animation: google.maps.Animation.BOUNCE
            });
        }
        marker = pub.addressmarker;

        //Populate hidden input fields for problem reporting on homepage with lonlat data.
        google.maps.event.addListener(marker, "dragend", function () {
            marker.setAnimation(google.maps.Animation.BOUNCE);

            $('input[name=report_start-lat]').val(marker.getPosition().lat().toString());
            $('input[name=report_start-lon]').val(marker.getPosition().lng().toString());
        });

        google.maps.event.addListener(marker, "drag", function () {
            marker.setAnimation();
        });

        //Fire dragend event to get initial values
        google.maps.event.trigger(marker, "dragend");
    };

    return pub;

}());

var FMSMap = (function () {
    'use strict';
    var pub = {},
        map_options = {
            center: new google.maps.LatLng(41.708484, 44.79847),
            zoom: 17,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    pub.map = '';
    pub.markers = '';
    pub.geocoder = new google.maps.Geocoder();


    pub.initialize = function (canvas) {
        pub.map = new google.maps.Map(canvas, map_options);
        FMSMarkers.initialize(pub.map);
        pub.markers = FMSMarkers;
    };

    pub.homeinit = function () {
        var input = (document.getElementById('address_search')),
            autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.bindTo('bounds', pub.map);
        autocomplete.setComponentRestrictions({'country': 'GE'});
        window.infowindow = new google.maps.InfoWindow({
            maxWidth: 300
        });

        //START GOOGLE MAPS AUTOCOMPLETE
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            input.className = '';
            var place = autocomplete.getPlace(),
                address;
            if (!place.geometry) {
                // Inform the user that the place was not found and return.
                input.className = 'notfound';
                return;
            }

            if (place.geometry.viewport) {
                pub.map.fitBounds(place.geometry.viewport);
            } else {
                pub.map.setCenter(place.geometry.location);
                pub.map.setZoom(17);
            }

            if (place.address_components) {
                address = [
                    ((place.address_components[0] && place.address_components[0].short_name) || ''),
                    ((place.address_components[1] && place.address_components[1].short_name) || ''),
                    ((place.address_components[2] && place.address_components[2].short_name) || '')
                ].join(' ');
            }
            pub.markers.addressMarker();
        });

        //END GOOGLE MAPS AUTOCOMPLETE

        google.maps.event.addListenerOnce(pub.map, 'idle', function () {
            FMSForms.loadDivs();
            pub.populateMarkers();
        });

        $('.cities-moveto li').each(function () {
            $(this).click(function () {
                if ($(this).data('city')) {
                    var city = $(this).data('city');
                    $('#change-city').show();
                    pub.moveToCity(city);
                }
            });
        });

        pub.jqueryfuncs();
    };

    pub.jqueryfuncs = function () {

        // Geocoding on homepage
        $(document).on('submit', '.address-search-form', function getLocation() {
            var inputs = $(this).serializeArray(),
                address = inputs[0].value.trim().replace(' ', '+'),
                city = inputs[1].value;

            pub.geocoder.geocode({
                address: address + ', ' + city
            }, pub.panToStreet);

            return false;
        });
    };


    /*
     * Lats and Lngs of cities
     * TODO: Move this to model
     */
    function getCityData(cityName) {
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
    }

    pub.mapResize = function () {
        var window_height = $(window).height(),
            window_width = $(window).width();

        if (window_height < 600 && window_width < 1005) {
            $('#map_canvas').css({
                'height': window_height - 120
            });
        }
    };

    /*Resizes google map if nesessary. Without this, map breaks. Poll it in case of animation
     */
    pub.checkSize = function () {
        google.maps.event.trigger(pub.map, 'resize');
    };

    /*
     * Moves map to city center when clicking on cities on homepage
     */
    pub.moveToCity = function (cityName) {
        cityName = cityName || 'Tbilisi';
        var cityCenter,
            cityData,
            left_img = $('#left-image'),
            left_width = left_img.width() - 10;

        $('.choose-city.hidden-lg').remove();
        pub.checkSize();
        $('#desk-city').empty();
        cityData = getCityData(cityName);
        cityCenter = cityData.center.LatLng;
        pub.map.panTo(cityCenter);
        pub.map.setZoom(17);
        pub.fixCenter(true);

        $('#map_canvas').animate({
            marginLeft: '-' + left_width
        }, 800, function () {
            $('#left-image').remove();

            $('.start-hidden').css({'visibility': 'visible'}).animate({
                opacity: 1
            }, 1300);

            FMSForms.processForms();

            left_img.animate({
                opacity: 0,
                marginLeft: -1600
            }, 800, pub.checkSize());

            $('.choose-city.visible-lg').remove();

        });

        $('.geocode-city').val(cityName);
        $('#id-city').val(cityName);
        pub.markers.addressMarker();
    };

    /**
     * Initial loader of markers. Run when map is idle
     */
    pub.populateMarkers = function () {
        var coords, LatLng, marker, icon,
            reports = pub.getLatestReports(),
            texts = {
                readmore: gettext('Read more...')
            },
            url = window.location.href,
            urlArr = url.split("/"),
            protocol = urlArr[0] + "//",
            domain = urlArr[2],
            lang = urlArr[3],
            asyncLoop;

        /***
         * Non-blocking loop to populate markers
         */
        asyncLoop = function (i) {
            if (reports[i].status === 'fixed') {
                icon = pub.markers.markericons.green;
            } else if (reports[i].status === 'not-fixed') {
                icon = pub.markers.markericons.red;
            } else if (reports[i].status === 'in-progress') {
                icon = pub.markers.markericons.yellow;
            }
            coords = reports[i].point.coordinates;
            LatLng = new google.maps.LatLng(coords[1], coords[0]);
            marker = pub.markers.createMarker('id_marker_' + reports[i].id, LatLng, {icon: icon});
            marker.description = reports[i].description + '<br><a href="' + protocol + domain + '/' +
            lang + '/reports/' + reports[i].id + '">' + texts.readmore + '</a>';

            google.maps.event.addListener(marker, 'click', function () {
                infowindow.setContent(pub.description);
                infowindow.open(pub.map, this);
            });

            pub.markers.markercluster.addMarker(marker);

            if (i < reports.length - 1) {
                setTimeout(function () {
                    asyncLoop(i + 1);
                }, 1);
            }
        };

        asyncLoop(0);
    };

    /**
     * Gets latest reports in json format
     */
    pub.getLatestReports = function () {
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


    /*
     This function fixes center of the map according to width. Affects only large screens.
     */
    pub.fixCenter = function (inverted) {
        inverted = (inverted !== undefined) ? inverted : false;
        if (screen.width > 1005) {
            if (inverted) {
                pub.map.panBy(-screen.width / 7, 0);
            } else {
                pub.map.panBy(screen.width / 7, 0);
            }
        }
    };

    pub.panToStreet = function (response, status) {
        var streetObj,
            streetName;

        if (!response || status !== google.maps.GeocoderStatus.OK) {
            console.log(status);
        } else {
            streetObj = response[0];
            var steetName = streetObj.formatted_address;

            // Zoom in to correctly calculate pixels to move by
            pub.map.setZoom(15);
            pub.map.panTo(streetObj.geometry.location);
            pub.fixCenter();
            pub.markers.addressMarker();
        }
    };

    return pub;

}());
