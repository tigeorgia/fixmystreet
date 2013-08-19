(function ($, sr) {

    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
        var timeout;

        return function debounced() {
            var obj = this, args = arguments;

            function delayed() {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
            };

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100);
        };
    }
    // smartresize
    jQuery.fn[sr] = function (fn) {
        return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr);
    };

})(jQuery, 'smartresize');

(function ($) {
// usage:
    $(window).smartresize(function () {
        mapResize();
    });

    $(function () {
        mapResize();
    });

    $(function () {
        $(".lang-choose").click(function () {
            var lang = $(this).find('a').data('lang');
            var next = $('#no-lang-path').data('next');
            $.post("/i18n/setlang/", { language: lang, next: next})
                .done(function () {
                    location.href = '/' + lang + next;
                });

        });
    });


    $(function () {
        $('.all-reports-table').mousedown(function (e) {
            switch (e.which) {
                case 1:
                    window.location = $(this).find('a').attr('href');
                    break;
            }
            return true;
        });
    });


    $(function () {
        var map = $("#map_canvas");
        var reportsMap = $(".reports #map_canvas");
        // Google map loads 7 divs. Insert blue overlay after all elements are
        // loaded.
        var mapInterval = setInterval(function () {
            if (reportsMap.children().size() == 7) {
                clearInterval(mapInterval);
                map.append('<div id="blue-overlay-200"></div>');
                map.after('<div id="box-reports-transpar-logo"></div>');
            }
        }, 100);
    });

    window.onbeforeunload = function () {
        $('#cut').animate({
            width: 10 + 'px',
            marginLeft: -20 + 'px'
        }, 400);
    };

    $(function () {
        $('#cut').animate({
            width: 830 + 'px',
            marginLeft: -415 + 'px'
        }, 1400);
    });

    /*
     * Lats and Lngs of cities
     * TODO Maybe store these in database?
     */
    function getCityCenter(cityName) {
        var center = {
            lat: '',
            lng: ''
        };
        switch (cityName) {
            case 'Tbilisi':
                center.lat = '41.708484';
                center.lng = '44.79847';
                break;

            case 'Batumi':
                center.lat = '41.633086';
                center.lng = '41.633291';
                break;

            case 'Kutaisi':
                center.lat = '42.252473';
                center.lng = '42.695875';
                break;

            case 'Zugdidi':
                center.lat = '42.503807';
                center.lng = '41.86203';
                break;
        }
        return center;
    }

    $(function () {
        $('#contact-page').css({
            'min-height': window.innerHeight
        })
    });


    function mapResize() {
        var window_height = $(window).height();
        var window_width = $(window).width();
        if (window_height < 600 && window_width < 1005)
            $('#map_canvas').css({
                'height': window_height - 120
            })
    }


    /*Resizes google map if nesessary. Without this, map breaks. Poll it in case of animation
     */
    function checkSize() {
        geodjango.map_canvas.checkResize();
    }

    /*
     * Moves map to city center when clicking on cities on homepage
     */
    $(function moveToCity() {
        var cityName;
        var cityLatLng;
        var cityCenter;

        $('.cities-home li.cities').each(function () {
            $(this).click(function () {

                $('.choose-city.hidden-lg').remove();

                checkSize();

                $('#desk-city').empty();

                cityName = $(this).data('city');
                cityLatLng = getCityCenter(cityName);
                cityCenter = new GLatLng(cityLatLng.lat, cityLatLng.lng);
                geodjango.map_canvas.panTo(cityCenter);
                geodjango.map_canvas.setZoom(15);


                var left_img = $('#left-image');
                var left_width = left_img.width() - 10;

                $('#map_canvas').animate({
                    marginLeft: '-' + left_width
                }, 800, function () {
                    $('#left-image').remove();

                    $('.start-hidden').css({'visibility': 'visible'}).animate({
                        opacity: 1,
                    }, 1300);

                    left_img.animate({
                        opacity: 0,
                        marginLeft: -1600
                    }, 800, function () {
                        checkSize();
                    });

                    $('.choose-city.visible-lg').remove();

                });

                $('.geocode-city').val(cityName);
                $('#id-city').val(cityName);


                geodjango.map_canvas.clearOverlays();

                if (typeof geodjango.map_canvas_marker_new === 'undefined') {
                    geodjango.map_canvas_marker_new = new GMarker(cityCenter, {icon: dragme, draggable: true});
                }


                geodjango.map_canvas.addOverlay(geodjango.map_canvas_marker_new);


                $('input[id=id_lat]').val(geodjango.map_canvas_marker_new.getPoint().lat().toString());
                $('input[id=id_lon]').val(geodjango.map_canvas_marker_new.getPoint().lng().toString());

                //then change on drag end
                GEvent.addListener(geodjango.map_canvas_marker_new, "dragend", function () {
                    $('input[id=id_lat]').val(geodjango.map_canvas_marker_new.getPoint().lat().toString());
                    $('input[id=id_lon]').val(geodjango.map_canvas_marker_new.getPoint().lng().toString());
                });

            });

        });

    });


    $(document).on('submit', '.address-search-form', function getLocation() {
        var geocoder = new GClientGeocoder();
        var inputs = $(this).serializeArray();
        var address = inputs[0].value.trim().replace(' ', '+');
        var city = inputs[1].value;
        var replacement;

        //split words to run them through replaced
        var addressWords = address.split(/\+/);

        // remove empty strings
        addressWords = addressWords.filter(function (e) {
            return e
        });

        for (var i = 0; i < addressWords.length; i++) {
            replacement = addressTurnaround(addressWords[i].toLowerCase());

            if (typeof replacement != 'undefined') {
                addressWords[i] = replacement;
            }
        }

        geocoder.getLocations(addressWords + ', ' + city, panToStreet);

        return false;

    });

    function addMarker() {
        var center = geodjango.map_canvas.getCenter();
        var pixel = geodjango.map_canvas.fromLatLngToContainerPixel(center)
        var locLatLng;
        var newPixel;

        newPixel = new GPoint(pixel.x - $('#map_canvas').width() / 7, pixel.y);
        locLatLng = geodjango.map_canvas.fromContainerPixelToLatLng(newPixel);

        geodjango.map_canvas.clearOverlays();
        geodjango.map_canvas_marker_new = new GMarker(locLatLng, {icon: dragme, draggable: true});
        geodjango.map_canvas.addOverlay(geodjango.map_canvas_marker_new);

        GEvent.addListener(geodjango.map_canvas_marker_new, "dragend", function () {
            $('input[id=id_lat]').val(geodjango.map_canvas_marker_new.getPoint().lat().toString());
            $('input[id=id_lon]').val(geodjango.map_canvas_marker_new.getPoint().lng().toString());
        });
    }


    function panToStreet(response) {
        var street;
        var mapWidth = $('#map_canvas').width();
        var mapHeight = $('#map_canvas').height();
        var streetObj;
        var searchName;
        geodjango.map_canvas.clearOverlays();

        if (!response || response.Status.code != 200) {
            alert("Something went wrong!")
        } else {
            streetObj = response.Placemark[0];
            var steetName = streetObj.address;
            var searchName = response.name.split(/(.+)\,/)[1];


            // Zoom in to correctly calculate pixels to move by
            geodjango.map_canvas.setZoom(15);
            // 1= lat, 0= lng
            var streetCoord = new GLatLng(streetObj.Point.coordinates[1], streetObj.Point.coordinates[0]);
            // Calculates pixels to move by and gives smooth transition.
            var newLoc = geodjango.map_canvas.fromLatLngToContainerPixel(streetCoord);
            //Smooth transition to location
            geodjango.map_canvas.panBy(new GSize(-newLoc.x + mapWidth / 2 - (mapWidth / 20), -newLoc.y + mapHeight / 2));

            geodjango.map_canvas.clearOverlays();
            geodjango.map_canvas_marker_new = new GMarker(streetCoord, {icon: dragme, draggable: true});
            geodjango.map_canvas.addOverlay(geodjango.map_canvas_marker_new);

            //set first marker location at form load
            $('input[id=id_lat]').val(streetCoord.y);
            $('input[id=id_lon]').val(streetCoord.x);

            //then change on drag end
            GEvent.addListener(geodjango.map_canvas_marker_new, "dragend", function () {
                $('input[id=id_lat]').val(geodjango.map_canvas_marker_new.getPoint().lat().toString());
                $('input[id=id_lon]').val(geodjango.map_canvas_marker_new.getPoint().lng().toString());
            });
        }
    }


    function addressTurnaround(address) {
        var arr = [
            {
                'name': 'გლდანი',
                'replacement': 'GLDANI MICRODISTRICT'
            },
            {
                'name': 'მიკრო-რაიონი',
                'replacement': 'Microdistrict'
            },
            {
                'name': 'gldani',
                'replacement': 'Gldani Microdistrict'
            }

        ];


        for (var i = 0; i < arr.length; i++) {
            if (arr[i].name === address) {
                return arr[i].replacement;
            }
        }


    }

//Forms

    $(function () {
        $('#new-report').validate({
            ignore: "",
            rules: {
                title: "required",
                category_id: "required",
                street: "required",
                author: "required",
                email: {
                    required: true,
                    email: true
                },
                phone: "required",
                lon: "required",
                lat: "required"
            },
            messages: {
                title: gettext("Please enter problem title"),
                category_id: gettext("Please enter category"),
                street: gettext("Enter street"),
                author: gettext("Your name is required as well"),
                email: gettext("You'll need this for verification"),
                phone: gettext("We won't spam you! Promise!"),
                lon: "Set point on map!"
            },
            submitHandler: function (form) {
                form.submit();
            }

        });
    });

    $(function () {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd'
        });
    });

})(jQuery);