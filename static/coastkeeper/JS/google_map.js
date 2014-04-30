var geocoder = null
var map = null

function initialize() {
    var SAN_DIEGO = new google.maps.LatLng(32.799636,-117.253385);
    var mapOptions = {
        center: SAN_DIEGO,
        zoom: 10
    };
    map = new google.maps.Map($("#map_canvas").get(0), mapOptions);
    geocoder = new google.maps.Geocoder();
    drawMPA();
}

function showAddress(address) {
    if (geocoder) {
        geocoder.geocode({ 'address': address}, function (results, status) {
            if (status != google.maps.GeocoderStatus.OK) {
                alert(address + " not found");
            } else {
                coordinates = results[0].geometry.location.toUrlValue(6)
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    draggable: true
                });

                var infowindow = new google.maps.InfoWindow({
                    content: coordinates
                });

                $('#id_location').val(coordinates)
                google.maps.event.addListener(marker, "dragend", function () {
                    infowindow.setContent(marker.getPosition().toUrlValue(6))
                    infowindow.open(map, marker)
                    $('#id_location').val(marker.getPosition().toUrlValue(6));
                });
                google.maps.event.addListener(marker, "click", function () {
                    infowindow.setContent(marker.getPosition().toUrlValue(6))
                    infowindow.open(map, marker)
                    $('#id_location').val(marker.getPosition().toUrlValue(6));
                });
                google.maps.event.trigger(marker, "click");
            }  
        });
    }
}

function drawMPA()
{
    /* Baquitos Lagoon */
    var coords1 = [
        new google.maps.LatLng(33.090667, -117.302000),
        new google.maps.LatLng(33.087933, -117.292342),
        new google.maps.LatLng(33.090486, -117.2773),
        new google.maps.LatLng(33.091151,-117.278738),
        new google.maps.LatLng(33.090647,-117.291956),
        new google.maps.LatLng(33.091, -117.302167),
        new google.maps.LatLng(33.091000, -117.302167),
        new google.maps.LatLng(33.090667, -117.302000)
    ];

    /* Swami's State */
    var coords2 = [
        new google.maps.LatLng(33.048333, -117.298783),
        new google.maps.LatLng(33.048333, -117.362383),
        new google.maps.LatLng(33.000000, -117.339967),
        new google.maps.LatLng(33.000000, -117.2783),
        new google.maps.LatLng(33.016333, -117.28095),
        new google.maps.LatLng(33.048333, -117.298783)
    ];

    /* San Elijo Lagoon */
    var coords3 = [
        new google.maps.LatLng(33.015938,-117.281298),
        new google.maps.LatLng(33.009461,-117.264733),
        new google.maps.LatLng(33.007301,-117.262544),
        new google.maps.LatLng(33.002947,-117.277865),
        new google.maps.LatLng(33.015938,-117.281298)
    ];

    /* San Dieguito Lagoon */
    var coords4 = [
        new google.maps.LatLng(32.967565, -117.258939),
        new google.maps.LatLng(32.967385, -117.250228),
        new google.maps.LatLng(32.964928, -117.2507),
        new google.maps.LatLng(32.963244, -117.254605),
        new google.maps.LatLng(32.967565, -117.258939)
    ];

    /* San Diego-Scripps */
    var coords5 = [
        new google.maps.LatLng(32.883333, -117.252767),
        new google.maps.LatLng(32.883333, -117.273333),
        new google.maps.LatLng(32.866067, -117.273333),
        new google.maps.LatLng(32.866067, -117.253883),
        new google.maps.LatLng(32.876242, -117.2511),
        new google.maps.LatLng(32.883333, -117.252767)
    ];

    /* Matlahuayl */
    var coords6 = [
        new google.maps.LatLng(32.866067, -117.253883),
        new google.maps.LatLng(32.866067, -117.273333),
        new google.maps.LatLng(32.851117, -117.273333),
        new google.maps.LatLng(32.848325, -117.265348),
        new google.maps.LatLng(32.859469, -117.256421),
        new google.maps.LatLng(32.866067, -117.253883)
    ];

    /* South La Jolla SMR */
    var coords7 = [
        new google.maps.LatLng(32.826217, -117.279683),
        new google.maps.LatLng(32.826217, -117.316667),
        new google.maps.LatLng(32.799083, -117.316667),
        new google.maps.LatLng(32.799083, -117.25825),
        new google.maps.LatLng(32.826217, -117.279683)
    ];

    /* South La Jolla SMCA */
    var coords8 = [
        new google.maps.LatLng(32.826217, -117.316667),
        new google.maps.LatLng(32.826217, -117.342133),
        new google.maps.LatLng(32.799083, -117.334467),
        new google.maps.LatLng(32.799083, -117.316667),
        new google.maps.LatLng(32.826217, -117.316667)
    ];

    /* Famosa Slough */
    var coords9 = [
        new google.maps.LatLng(32.756283,-117.228931),
        new google.maps.LatLng(32.755621, -117.228974),
        new google.maps.LatLng(32.754115, -117.229811),
        new google.maps.LatLng(32.752554, -117.229425),
        new google.maps.LatLng(32.749594, -117.229135),
        new google.maps.LatLng(32.749378, -117.228051),
        new google.maps.LatLng(32.75083, -117.22686),
        new google.maps.LatLng(32.752644, -117.227086),
        new google.maps.LatLng(32.75268, -117.229038),
        new google.maps.LatLng(32.754187, -117.229371),
        new google.maps.LatLng(32.755685, -117.228513),
        new google.maps.LatLng(32.756283,-117.228931)
    ];

    /* Cabrillo */
    var coords10 = [
        new google.maps.LatLng(32.676667, -117.247),
        new google.maps.LatLng(32.676667, -117.25),
        new google.maps.LatLng(32.661667, -117.25),
        new google.maps.LatLng(32.661667, -117.238333),
        new google.maps.LatLng(32.666667, -117.238333),
        new google.maps.LatLng(32.664805, -117.242753),
        new google.maps.LatLng(32.666568, -117.245378),
        new google.maps.LatLng(32.668808, -117.245035),
        new google.maps.LatLng(32.673938, -117.245679),
        new google.maps.LatLng(32.676667, -117.247)
    ];

    /* Tijuana River */
    var coords11 = [
        new google.maps.LatLng(32.566667,-117.133),
        new google.maps.LatLng(32.566667,-117.15),
        new google.maps.LatLng(32.532833,-117.15),
        new google.maps.LatLng(32.534333,-117.124667),
        new google.maps.LatLng(32.553121,-117.128047),
        new google.maps.LatLng(32.557751,-117.132167),
        new google.maps.LatLng(32.566667,-117.133)
    ];

    var coords = {
        'Baquitos Lagoon': coords1,
        'Swami\'s State': coords2,
        'San Elijo Lagoon': coords3,
        'San Dieguito Lagoon': coords4,
        'San Diego-Scripps': coords5,
        'Matlahuayl': coords6,
        'South La Jolla SMR': coords7,
        'South La Jolla SMCA': coords8,
        'Famosa Slough': coords9,
        'Cabrillo': coords10,
        'Tijuana River': coords11
    };

    for(var i in coords) {
                if(coords.hasOwnProperty(i)) {
                    var polygon = new google.maps.Polygon({
                        paths: coords[i],
                        strokeColor: '#E60000',
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillColor: '#FF3333',
                        fillOpacity: 0.35
                    });

                    polygon.setMap(map);
                    //display_name(polygon, i);
                }
            }
}

function display_name(polygon, name) {
    var tooltip = new MarkerWithLabel({
        position: new google.maps.LatLng(0,0),
        draggable: false,
        raiseOnDrag: false,
        map: map,
        labelContent: name,
        labelAnchor: new google.maps.Point(30, 20),
        labelClass: "labels", // the CSS class for the label
        labelStyle: {opacity: 1.0},
        icon: "http://placehold.it/1x1",
        visible: false
    });

    google.maps.event.addListener(polygon, 'mousemove', function(event) {
        tooltip.setPosition(event.latLng);
        tooltip.setVisible(true);
    });

    google.maps.event.addListener(polygon, 'mouseout', function(event) {
        tooltip.setVisible(false);
    });
}