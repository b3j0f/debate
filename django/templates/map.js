var map = new ol.Map({
	target: 'map',
	layers: [
	new ol.layer.Tile({
		source: new ol.source.OSM()
	})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([37.41, 8.82]),
		zoom: 16
	})
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
