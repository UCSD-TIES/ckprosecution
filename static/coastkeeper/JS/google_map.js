var geocoder = null
var map = null

function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(37.4419, -122.1419),
        zoom: 10
    };
    map = new google.maps.Map($("#map_canvas").get(0), mapOptions);
    geocoder = new google.maps.Geocoder();
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
            }
        );
    }
}