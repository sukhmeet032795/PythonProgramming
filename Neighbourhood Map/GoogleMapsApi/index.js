function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: {lat: 28.7041, lng: 77.1025}
    });

    var infowindow = new google.maps.InfoWindow({
        content: "Yo!!! Mumbai"
    });

    var mumbai = {lat : 19.0760, lng : 72.8777};
    var marker = new google.maps.Marker({
      position: mumbai,
      map: map,
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
};
