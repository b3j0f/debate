document.getElementById('categories').innerHTML =
'<nav>' +
'Catégorie' +
'<a class="breadcrumb dropdown-button" id="topcategory" href="#" data-activates="topcategories" data-beloworigin="true" data-constrainWidth="true" data-gutter="0" data-hover="true" name="topcategory">Tout</a>' +
'<ul name="topcategories" id="topcategories" class="dropdown-content">' +
'</ul>' +
'<a class="breadcrumb dropdown-button" id="midcategory" href="#" data-activates="midcategories" data-beloworigin="true" data-constrainWidth="true" data-hover="true">Tout</a>' +
'<ul name="midcategories" id="midcategories" class="dropdown-content">' +
'</ul>' +
'<a class="breadcrumb dropdown-button" id="lowcategory" href="#" data-activates="lowcategories" data-beloworigin="true" data-constrainWidth="true" data-hover="true">Tout</a>' +
'<ul name="lowcategories" id="lowcategories" class="dropdown-content">' +
'</ul>' +
'</nav>';

var topcategories = {};
var midcategories = {};

var toplis = '<li id="topall" class="active"><a onclick="selectcat(\'top\', this);">Tout</a></li>';
var midlis = '<li id="midall" class="active"><a onclick="selectcat(\'mid\', this);">Tout</a></li>';
var lowlis = '<li id="lowall" class="active"><a onclick="selectcat(\'low\', this);">Tout</a></li>';

{% for topcategory in topcategories %}
var topcat = '{{ topcategory.name }}'.replace('/', '-');
topcategories['{{ topcategory.name }}'] = [];
toplis += '<li class="top"><a id="' + topcat + '" onclick="selectcat(\'top\', this)">{{ topcategory.name }}</a></li>';
	{% for midcategory in topcategory.children.all %}
	var midcat = '{{ midcategory.name }}'.replace('/', '-');
topcategories['{{ topcategory.name }}'].push('{{ midcategory.name }}');
midlis += '<li class="mid ' + topcat + '"><a id="' + midcat + '" onclick="selectcat(\'mid\', this)">{{ midcategory.name }}</a></li>';
midcategories['{{ midcategory.name }}'] = [];
		{% for lowcategory in midcategory.children.all %}
var lowcat = '{{ lowcategory.name }}'.replace('/', '-');
midcategories['{{ midcategory.name }}'].push('{{ lowcategory.name }}');
lowlis += '<li class="low ' + topcat + ' ' + midcat + '"><a id="' + lowcat + '" onclick="selectcat(\'low\', this)">{{ lowcategory.name }}</a></li>';
		{% endfor %}
	{% endfor %}
{% endfor %}

$('#topcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	toplis
);

$('#midcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	midlis
);

$('#lowcategories')[0].insertAdjacentHTML(
	'beforeEnd',
	lowlis
);

var selectedtop = 'tout';
var selectedmid = 'tout';
var selectedlow = 'tout';

var lasttop = $('#topall');
var lastmid = $('#midall');
var lastlow = $('#lowall');

$('#midcategory').hide();
$('#lowcategory').hide();

function selectcat(type, elt) {
	var id = elt.id ? elt.id : 'tout';
	switch(type) {
		case 'top':
			if (selectedtop === id) break;
			selectedtop = id;
			lasttop.removeClass('active');
			lasttop = $(elt.parentNode);
			lasttop.addClass('active');
			if (! elt.id) {
				$('.lowcategory').hide();
				$('#lowcategory').hide();
				$('.midcategory').hide();
				$('#midcategory').hide();
			} else {
				selectedmid = selectedlow = 'tout';
				$('.lowcategory').hide();
				$('#lowcategory').hide();
				$('.mid').hide();
				$('.mid.'+id).show();
				$('#midcategory').show();
			}
			lastmid.removeClass('active');
			lastmid = $('#midall');
			lastmid.addClass('active');
			break;
		case 'mid':
			if (selectedmid === id) break;
			selectedmid = id;
			lastmid.removeClass('active');
			lastmid = $(elt.parentNode);
			lastmid.addClass('active');
			if (! elt.id) {
				$('.lowcategory').hide();
				$('#lowcategory').hide();
			} else {
				selectedlow = 'tout';
				$('.low').hide();
				$('.low.'+id).show();
				$('#lowcategory').show();
			}
			lastlow.removeClass('active');
			lastlow = $('#lowall');
			lastlow.addClass('active');
			break;
		case 'low':
			if (selectedlow === id) break;
			selectedlow = id;
			lastlow.removeClass('active');
			lastlow = $(elt.parentNode);
			lastlow.addClass('active');
	};
	$('#topcategory')[0].innerHTML = selectedtop;
	$('#midcategory')[0].innerHTML = selectedmid;
	$('#lowcategory')[0].innerHTML = selectedlow;
}
