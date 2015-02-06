function FMSMarkers(map) {
    if (arguments.callee._singletonInstance)
        return arguments.callee._singletonInstance;
    arguments.callee._singletonInstance = this;
    var cluster_opts = {gridSize: 20, maxZoom: 17}
    this.map = map;
    this.addressmarker = '';

    this.markericons = {
        dragme: "/static/images/marker/default/marker.png",
        green: "/static/images/marker/default/green.png",
        red: "/static/images/marker/default/red.png",
        yellow: "/static/images/marker/default/yellow.png"
    };
    this.markercluster = new MarkerClusterer(this.map, [], cluster_opts);

    /*
     Creates google.maps.Marker
     */
    this.createMarker = function (name, latlng, opts) {
        var timestamp = new Date().valueOf(); //Generate unique name if it's not supplied
        var params = {};
        opts = opts || {};

        //Set defaults
        params.name = name || "marker_" + String(timestamp);
        params.position = latlng || map.getCenter();
        params.draggable = opts.draggable || false;
        params.animation = opts.animation || google.maps.Animation.DROP;
        params.icon = opts.icon || this.markericons.dragme;
        params.title = opts.title || "Marker";

        //Create marker and store in global GmapMarkers object
        marker = new google.maps.Marker({
            position: params.position,
            map: this.map,
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
    this.addressMarker = function () {
        var center = this.map.getCenter(); // Get center of the map where user is
        var marker = this.addressmarker;

        //If marker is already there, remove it and make it again. Otherwise it won't work
        if (!marker) {
            this.addressmarker = this.createMarker('address_marker', center, {
                draggable: true,
                animation: google.maps.Animation.BOUNCE
            });
        } else {
            this.addressmarker.setMap(null);
            this.addressmarker = this.createMarker('address_marker', center, {
                draggable: true,
                animation: google.maps.Animation.BOUNCE
            });
        }
        marker = this.addressmarker;

        //Populate hidden input fields for problem reporting on homepage with lonlat data.
        //TODO: Change input to one field. I.e. not separate lat and lon, but one single POINT geom field.
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

};

function FMSMap() {
    if (arguments.callee._singletonInstance)
        return arguments.callee._singletonInstance;
    arguments.callee._singletonInstance = this;

    var map_options = {
        center: new google.maps.LatLng(41.708484, 44.79847),
        zoom: 17,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    this.map = new google.maps.Map(document.getElementById("map_canvas"), map_options);
    this.markers = new FMSMarkers(this.map);
    this.geocoder = new google.maps.Geocoder();


    this.initialize = function () {
        var input = (document.getElementById('address_search'));
        var autocomplete = new google.maps.places.Autocomplete(input);
        var scope = this;
        autocomplete.bindTo('bounds', this.map);
        autocomplete.setComponentRestrictions({'country': 'GE'});
        window.infowindow = new google.maps.InfoWindow({
            maxWidth: 300
        });

        //START GOOGLE MAPS AUTOCOMPLETE
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            input.className = '';
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                // Inform the user that the place was not found and return.
                input.className = 'notfound';
                return;
            }

            if (place.geometry.viewport) {
                scope.map.fitBounds(place.geometry.viewport);
            } else {
                scope.map.setCenter(place.geometry.location);
                scope.map.setZoom(17);
            }

            var address = '';
            if (place.address_components) {
                address = [
                    (place.address_components[0] && place.address_components[0].short_name || ''),
                    (place.address_components[1] && place.address_components[1].short_name || ''),
                    (place.address_components[2] && place.address_components[2].short_name || '')
                ].join(' ');
            }
            scope.markers.addressMarker();
        });

        //END GOOGLE MAPS AUTOCOMPLETE

        google.maps.event.addListenerOnce(this.map, 'idle', function () {
            fmsforms.loadDivs();
            scope.populateMarkers();
        });

        $('.cities-moveto li').each(function () {
            $(this).click(function () {
                if ($(this).data('city')) {
                    var city = $(this).data('city');
                    $('#change-city').show();
                    scope.moveToCity(city);
                }
            });
        });

        this.jqueryfuncs();
    };

    this.jqueryfuncs = function(){
        var scope = this;

        // Geocoding on homepage
        $(document).on('submit', '.address-search-form', function getLocation() {
            var inputs = $(this).serializeArray();
            var address = inputs[0].value.trim().replace(' ', '+');
            var city = inputs[1].value;

            scope.geocoder.geocode({
                address: address + ', ' + city
            }, scope.panToStreet);

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
    };

    this.mapResize = function () {
        var window_height = $(window).height();
        var window_width = $(window).width();
        if (window_height < 600 && window_width < 1005)
            $('#map_canvas').css({
                'height': window_height - 120
            });
    };

    /*Resizes google map if nesessary. Without this, map breaks. Poll it in case of animation
     */
    this.checkSize = function () {
        google.maps.event.trigger(this.map, 'resize');
    };

    /*
     * Moves map to city center when clicking on cities on homepage
     */
    this.moveToCity = function (cityName) {
        cityName = cityName || 'Tbilisi';
        var cityCenter, cityData;
        var scope = this;

        $('.choose-city.hidden-lg').remove();
        this.checkSize();
        $('#desk-city').empty();
        cityData = getCityData(cityName);
        cityCenter = cityData.center.LatLng;
        this.map.panTo(cityCenter);
        this.map.setZoom(17);
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

            fmsforms.processForms();

            left_img.animate({
                opacity: 0,
                marginLeft: -1600
            }, 800, scope.checkSize());

            $('.choose-city.visible-lg').remove();

        });

        $('.geocode-city').val(cityName);
        $('#id-city').val(cityName);
        this.markers.addressMarker();
    };

    /**
     * Initial loader of markers. Run when map is idle
     */
    this.populateMarkers = function () {
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
        var scope = this;

        /***
         * Non-blocking loop to populate markers
         */
        var AsyncLoop = function (i) {
            if (reports[i]['status'] == 'fixed') {
                icon = scope.markers.markericons.green;
            } else if (reports[i]['status'] == 'not-fixed') {
                icon = scope.markers.markericons.red;
            } else if (reports[i]['status'] == 'in-progress') {
                icon = scope.markers.markericons.yellow;
            }
            coords = reports[i]['point']['coordinates'];
            LatLng = new google.maps.LatLng(coords[1], coords[0]);
            marker = scope.markers.createMarker('id_marker_' + reports[i]['id'], LatLng, {icon: icon});
            marker.description = reports[i]['description'] + '<br><a href="' + protocol + domain + '/' +
            lang + '/reports/' + reports[i]['id'] + '">' + texts.readmore + '</a>';

            google.maps.event.addListener(marker, 'click', function () {
                infowindow.setContent(this.description);
                infowindow.open(this.map, this);
            });

            scope.markers.markercluster.addMarker(marker);

            if (i < reports.length - 1) {
                setTimeout(function () {
                    AsyncLoop(i + 1);
                }, 1)
            }
        }

        AsyncLoop(0);
    };

    /**
     * Gets latest reports in json format
     */
    this.getLatestReports = function () {
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
    this.fixCenter = function (inverted) {
        var inverted = inverted || false;
        if (screen.width > 1005) {
            if (inverted) {
                this.map.panBy(-screen.width / 7, 0);
            } else {
                this.map.panBy(screen.width / 7, 0);
            }
        }
    };

    this.panToStreet = function (response, status) {
        var streetObj;

        if (!response || status != google.maps.GeocoderStatus.OK) {
            console.log(status);
        } else {
            streetObj = response[0];
            var steetName = streetObj.formatted_address;

            // Zoom in to correctly calculate pixels to move by
            fmsmap.map.setZoom(15);
            fmsmap.map.panTo(streetObj.geometry.location);
            fmsmap.fixCenter();
            fmsmap.markers.addressMarker();
        }
    };

};
