$(document).ready(function() {

    google.maps.visualRefresh = true;

    var map;

    function initialize() {
        var mapOptions = {
            zoom: 12,
            center: new google.maps.LatLng(37.7616170601249, -122.4298728500122),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    }

    google.maps.event.addDomListener(window, 'load', initialize);

    // When enter is pressed, mimick a click
    $('#input').keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          $("#button").click();
        }
    });

    $("#button").click(function(){
        address = $("input[name=address]").val();
        data = {location: address};
        getTrucks(data);
    });

    var getTrucks = function(data) {
        // Make an API call to the back-end to get all nearyby foodtrucks
        // If successful, draw the map
        $.ajax({
            url: "/api/foodtrucks",
            type: 'GET',
            data: data,
            dataType: 'json', 
            contentType: 'application/json',
            error: function(){
                alert("Uh oh, looks like you searched for an invalid SF address!"); 
            },
            success: function(response) {
                drawMap(response.coordinates, response.foodtrucks);
            }
        });
    }

    var drawMap = function(coordinates, foodTrucks) {

        var markersArray = [];

        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(coordinates.lat, coordinates.lng),
            map: map,
            title: 'You are here'
        });

        markersArray.push(marker);
        
        map.panTo(marker.getPosition());
        
        map.setZoom(15);

        for (var i = 0; i < foodTrucks.length; i++){
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(foodTrucks[i].latitude, foodTrucks[i].longitude),
                map: map,
                title: foodTrucks[i].applicant,
                icon: 'static/images/foodtruck.png'
            });
            markersArray.push(marker);
            marker.content =    '<a href='+foodTrucks[i].schedule+'>'+
                                foodTrucks[i].applicant+'</a>' +
                                '<p>'+ foodTrucks[i].fooditems +'</p>';

            var infoWindow = new google.maps.InfoWindow();

            google.maps.event.addListener(marker, 'click', function() {
                infoWindow.setContent(this.content);
                infoWindow.open(this.getMap(), this);
            });
        };

        // Adds a listener to the map on drag, 
        // clears all markers and gets all the trucks in that area
        google.maps.event.addListener(map, 'dragend', function() {
            window.setTimeout(function() {
                clearOverlays();
                center = map.getCenter();
                data = {lat: center.pb, lng: center.qb};
                getTrucks(data);
            }, 500);
        });

        // Iterates through the markersArray and sets all markers to null
        function clearOverlays() {
            for (var i = 0; i < markersArray.length; i++ ) {
                markersArray[i].setMap(null);
            }
            markersArray = [];
        }
    }
});