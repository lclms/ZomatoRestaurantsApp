'use strict';
// with strict mode, you can not, for example, use undeclared variables

//****************************************************
// 		the map
//****************************************************

// Note: visualization will be put in the div with id=map_id 


// the markers

// room_categories = ['Entire home/apt', 'Private room', 'other'];

var mapMarkers = [];

function deleteMapMarkers() {
	for (var d in mapMarkers) {
		d.setMap(null);
	}
	mapMarkers = [];
}

function drawMapMarkers(data) {
	deleteMapMarkers();


// my own token to access mapbox tiles
var mymapboxtoken = 'pk.eyJ1IjoiYW1sc3MxIiwiYSI6ImNqZzZxMjdvbjd3bDQyd3FvaWc1cnZjNHgifQ.vQiQw-UlfnCNfguzGdGT2A';

// the map
var zoom = 2;
var la = 38.72;
var lo = -9.15;
if(data)
{
	
	zoom = 5;
	
	data.forEach(function(d) {
		la = d.Latitude;
		lo = d.Longitude;
		
	});

}
var mapcentre = [la, lo], zoom = zoom, max_zoom = 20;
var mymap = L.map('map_id').setView(mapcentre, zoom);

// the base layer
var baselayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: max_zoom,
  id: 'mapbox.streets',
  accessToken: mymapboxtoken
}).addTo(mymap);

// the popup
var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
		.setContent("You clicked at " + e.latlng.toString())
		.openOn(mymap);
	
 }

mymap.on('click', onMapClick);

	var msg = "";
	var marker;
	data.forEach(function(d) {
		//d.Latitude = +d.Latitude;
		//d.Longitude = +d.Longitude;
		var price = "";
		for (var i = 0; i < d.priceRange; i++) { 
			price = price + '$';
		}
		var star = "";
		for (var i = 0; i < (parseInt(d.aggregateating)); i++) { 
			star = star + '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Gold_Star.svg/768px-Gold_Star.svg.png" width="15" height="15">';
		}

		msg = '<h3>'+d.restaurantName + '</h3><hr>'+star+'<br><br><b>Cuisines: </b>' + d.Cuisines + '<br>'  + '<b>Price Range:</b> '+ price + ' of $$$$$';
		var pic = "Grey";
		if(d.ratingColor == "Dark Green"){pic = "Dark%20Green";}else if(d.ratingColor == "Green"){pic = "Green";}else if(d.ratingColor == "Orange"){pic = "Orange"}else if(d.ratingColor == "Red"){pic = "Red";}else if(d.ratingColor == "Yellow"){pic = "Yellow";}else if(d.ratingColor == "White"){pic = "White";}
		var myIcon = L.icon({
			iconUrl: 'http://0.0.0.0:5678/static/img/marker/'+pic+'.png'
		});
		marker = L.marker([d.Latitude, d.Longitude], {icon: myIcon}).bindPopup(msg).addTo(mymap);
		mapMarkers.push(marker);
	});
}

