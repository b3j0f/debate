{% load static %}

var address = $.cookie('address');
if (address) {
	$('#address').val(address);
}

function getCookie(name, def) {
	var result = $.cookie(name);
	if (result === undefined || isNaN(result[0])) {
		result = def;
	} else {
		result = result.split(',');
	}
	return result;
}

var center = getCookie('center', ol.proj.fromLonLat([0, 0]));
for(var index in center) {
	center[index] = parseFloat(center[index]);
}

/*var clusterSource = new ol.source.Cluster({
	distance: parseInt('40', 10),
	//source: features
});*/

function getClusterStyle(size) {
	var result = styleClusterCache[size];
	if (result === undefined) {
		result = new ol.style.Style({
			image: new ol.style.Circle({
				radius: 32 + 1.5 * size,
				stroke: new ol.style.Stroke({
					color: '#fff'
				}),
				fill: new ol.style.Fill({
					color: '#3399CC'
				})
			}),
			text: new ol.style.Text({
				text: size.toString(),
				fill: new ol.style.Fill({
					color: '#fff'
				})
			})
		});
		styleClusterCache[size] = result;
	}
	return result;
}

function getLocatedElementStyle(elt) {
	var key = elt.type + elt.needs.join() + elt.emergency;
	var result = styles[key];
	if (result === undefined) {
		var src = '{% static 'img' %}/pin.png';
		var text = elt.needs.length.toString();
		var style = new ol.style.Style({
			image: new ol.style.Icon({
				src: src,
				anchor: [0.5, 1]
			})
		});
		result = styles[key] = style;
	}
	return result;
}

function getStyle(feature) {
	var result;
	var features = feature.get('features');
	if (features.length == 1) {
		result = getLocatedElementStyle(features[0].get('elt'));
	} else {
		result = getClusterStyle(features.length);
	}
	return result;
}

/*var clusters = new ol.layer.Vector({
	id: 'clusters',
	source: clusterSource,
	style: function(feature) {
		return getStyle(feature);
	}
});*/

var map = new ol.Map({
	target: 'map',
	layers: [
	new ol.layer.Tile({
		source: new ol.source.OSM()
	}),
	//clusters
	],
	view: new ol.View({
		center: ol.proj.fromLonLat(center[0], center[1]),
		zoom: 16
	})
});
map.on('singleclick', function(evt, layer) {
	var feature = map.forEachFeatureAtPixel(
		evt.pixel,
		function(feature) { return feature; }
		);
	if (feature === undefined) {
		edit(feature, evt.coordinate);
	}
});
function getCurrentPosition() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function(pos) {
				map.getView().setCenter(ol.proj.fromLonLat([pos.coords.longitude, pos.coords.latitude]));
			}
		);
	} else {
		$('#errors').innerHTML = 'Ce navigateur ne supporte pas la géolocalisation.';
	}
}
getCurrentPosition();

function setCenter(longitude, latitude) {
	console.log(longitude, latitude);
	map.getView().setCenter([parseFloat(longitude), parseFloat(latitude)]);
	updateAddress(longitude, latitude);
}

function updateAddress(longitude, latitude) {
	$.ajax({
		method: 'GET',
		url: 'http://nominatim.openstreetmap.org/reverse',
		data: {
			format: 'json',
			lon: longitude,
			lat: latitude
		},
		success: function(data) {
			if(data !== undefined) {
				$('#address').val(data.display_name);
			}
		}
	});
}

function geoloc() {
	$('#load').modal('open');
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function(pos) {
				setCenter(pos.coords.longitude, pos.coords.latitude);
				map.getView().setZoom(
					Math.max(
						map.getView().getZoom(),
						15
						)
					);
				$('#load').modal('close');
			},
			function(msg) {
				$('#status')[0].innerHTML = 'Erreur : ' + (typeof msg == 'string' ? msg : 'failed');
			}
			);
	} else {
		$('#status')[0].innerHTML = 'Erreur : Geolocalisation non supportée';
	}
}

function setAddress(address) {
	$('#load').modal('open');
	$.ajax({
		method: 'GET',
		url: 'http://nominatim.openstreetmap.org/search/',
		data: {
			format: 'json',
			q: address
		},
		success: function(data) {
			$('#load').modal('close');
			console.log(data);
			if (data.length > 0) {
				var item = data[0];
				var boundingbox = [
				item.boundingbox[2],
				item.boundingbox[0],
				item.boundingbox[3],
				item.boundingbox[1]
				];
				var size = ol.extent.getSize(boundingbox);
				setCenter(item.lon, item.lat);
				//map.setSize(size);
				refresh();
				var names = [];
				data.forEach(function(item) {
					names.push(item.display_name);
				});
				var msg = names.length + ' adresse(s) trouvée(s) : <br/>' + names.join(',<br/>');
				var $toastContent = $('<p class="green-text">'+msg+'</p>');
			} else {
				var msg = 'Aucun adresse trouvée';
				var $toastContent = $('<p class="red-text">'+msg+'</p>');
			}
			Materialize.toast($toastContent, 5000);
		},
		error: function(error) {
			$('#load').modal('close');
			console.log(error);
			var msg = 'erreur : ' + error.responseText;
			var $toastContent = $('<p class="red-text">'+msg+'</p>');
			Materialize.toast($toastContent, 5000);
		}
	}, );
}