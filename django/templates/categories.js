var categories = {
	{% for category in categories %}
	'{{ category.name }}': {
		debates: [{% for debate in category.debates.all %}{{ debate.id }}, {% endfor %}],
		organizations: [{% for organization in category.organizations.all %}{{ organization.id }}, {% endfor %}],
		name: '{{ category.name }}',
		description: '{{ category.description }}'
	},
	{% endfor %}
};

var categoriesdom = $('#categories');
if (categoriesdom.length > 0) {
	var data = [];
	Object.values(categories).forEach(function(category) {
		data.push(category.name);
	});
	categoriesdom.material_chip({
		placeholder: 'Enter a tag',
		secondaryPlaceholder: '+Tag',
		autocompleteOptions: {
			data: data,
			limit: Infinity,
			minLength: 1
		}
	});
}

function fillCategories(elt) {
	var data = [];
	elt.categories.forEach(function(category) {
		data.push({tag: category.name});
	});
	$('#categories').material_chip({
		data: data
	});
}

{% if elt %}
fillCategories(elt);
{% endif %}