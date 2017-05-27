var types = {
	'topics': {
		translation: 'sujets',
		tkeywords: 'Rôle de l\'économie dans la politique',
		name: 'Rôle de l\'économie dans la politique',
	},
	'events': {
		translation: 'évènements',
		keywords: 'Conférence sur le rôle de l\'économie dans la politique',
		name: 'Rôle de l\'économie dans la politique',
	},
	'spaces': {
		translation: 'endroits',
		keywords: 'Place de la république',
		name: 'Nuit debout',
	}
};

var type = '{{ page }}';

for (var _type in types) {
	$('.' + _type).hide();
}
$('.' + type).show();

for (var field in types[type]) {
	try{
		$('#'+field).attr('placeholder', types[type][field]);
	} catch (Exception) {
	}
}

{% include 'map.js' %}