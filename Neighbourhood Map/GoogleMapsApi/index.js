var markers = [];

function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 13,
      center: {lat: 40.7413549, lng: -73.9980244},
    });

    // var infowindow = new google.maps.InfoWindow({
    //     content: "Yo!!! Mumbai"
    // });

    // var mumbai = {lat : 19.0760, lng : 72.8777};
    // var marker = new google.maps.Marker({
    //   position: mumbai,
    //   map: map,
    // });

    // marker.addListener('click', function() {
    //     infowindow.open(map, marker);
    // });

    var locations = [
        {title: 'Park Ave Penthouse', location: {lat: 40.7713024, lng: -73.9632393}},
        {title: 'Chelsea Loft', location: {lat: 40.7444883, lng: -73.9949465}},
        {title: 'Union Square Open Floor Plan', location: {lat: 40.7347062, lng: -73.9895759}},
        {title: 'East Village Hip Studio', location: {lat: 40.7281777, lng: -73.984377}},
        {title: 'TriBeCa Artsy Bachelor Pad', location: {lat: 40.7195264, lng: -74.0089934}},
        {title: 'Chinatown Homey Space', location: {lat: 40.7180628, lng: -73.9961237}}
    ];

    var largeInfowindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    for (var i = 0; i < locations.length; i++) {

        var position = locations[i].location;
        var title = locations[i].title;
        var marker = new google.maps.Marker({
            position: position,
            title: title,
            map: map,
            animation: google.maps.Animation.DROP,
            id: i
        });

        markers.push(marker);
        bounds.extend(marker.position);

        marker.addListener('click', function() {
            populateInfoWindow(this, largeInfowindow);
        }, this);
    }

    map.fitBounds(bounds);
};


// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.
function populateInfoWindow(marker, infowindow) {

        // Check to make sure the infowindow is not already opened on this marker.
    if (infowindow.marker != marker) {
        infowindow.marker = marker;
        infowindow.setContent('<div>' + marker.title + '</div>');
        infowindow.open(map, marker);
        infowindow.addListener('closeclick', function() {
            infowindow.marker = null;
        });
    }
};

