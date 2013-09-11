$(document).ready(function() {

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

    var drawMap = function(coordinates, foodTrucks){

        var map = new GMaps({
            div: '#map',
            lat: coordinates.lat,
            lng: coordinates.lng,
            zoomControl : false,
            width: '500px',
            height: '500px',
            dragend: function(e){
                center = this.getCenter();
                data = {lat: center.pb, lng: center.qb};
                getTrucks(data);
            }
        });

        map.addMarker({
            lat: coordinates.lat,
            lng: coordinates.lng,
            title: "You are here!",
            infoWindow: {
                content: '<p>You are here</p>'
            }
        });

        for (var i = 0; i < foodTrucks.length; i++){
            map.addMarker({
                lat: foodTrucks[i].latitude,
                lng: foodTrucks[i].longitude,
                title: foodTrucks[i].applicant,
                icon: 'static/images/foodtruck.png',
                infoWindow: {
                    content: '<a href='+foodTrucks[i].schedule+'>'+foodTrucks[i].applicant+'</a>' + '<p>'+ foodTrucks[i].fooditems +'</p>' 
                }
            });
        };
    };
});



       