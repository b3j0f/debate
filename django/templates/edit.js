$('.add').hide();
$('.update').hide();
{% if common %}
$('.update').show();
{% else %}
$('.add').show();
{% endif %}

var types = {
    product: {
        translation: 'produit',
        name: 'Appareil photo Nikon D80',
        shortdescription: '',
        description: ''
    },
    stock: {
        translation: 'stock',
        name: '',
        shortdescription: '',
        description: ''
    },
    service: {
        translation: 'service',
        name: '',
        shortdescription: '',
        description: ''
    }
};

var typesul = document.getElementById('types');
for(var type in types) {
    var html = '<li><a onclick="changeType(\'' + type + '\');">' + types[type].translation + '</a></li>'
    typesul.insertAdjacentHTML('beforeEnd', html);
}

var common = {
    name: '{{ common.name }}',
    shortdescription: '{{ common.shortdescription }}',
    description: '{{ common.description }}',
    created: '{{ common.created }}',
    owners: [{% for owner in common.owners.all %}'{{ owner.id }}', {% endfor %}],
    users: [{% for user in common.users.all %}'{{ user.id }}', {% endfor %}],
    category: '{{ common.category }}',
    professional: {% if common.professional %}true{% else %}false{% endif %}
};

{% if common %}
$('#owners').material_chip({
    placeholder: 'Entrez un pseudo',
    secondaryPlaceholder: '+pseudo',
    data: [
        {% for owner in common.owner %}
        {% if owner.id != user.id %}
        {
            tag: '{{ owner.pseudo }}',
            image: '{{ owner.media.url }}',
            id: {{ owner.id }}
        },
        {% endif %}
        {% endfor %}
    ],
    autocompleteOptions: {
      data: {
        {% for user in users %}
        '{{ user.pseudo }}': '{{ user.media.url }}',
        {% endfor %}
      },
      limit: Infinity,
      minLength: 1
    }
});
for(var prop in common) {
    try {
        $('#' + prop).val(common[prop]);
    } catch {
    }
}
{% endif %}

var supplyings = {
    {% for supply in common.supplyings.all %}
    '{{ supply.id }}'': {
        name: '{{ supply.name }}',
        description: '{{ supply.description }}',
        start: '{{ supply.start }}',
        stop: '{{ supply.stop }}',
        dates: [{% for date in supply.dates.all %}'{{ date }}', {% endfor %}],
        amount: {{ supply.amount }},
        period: '{{ supply.period }}',
        peruser: {% if supply.peruser %}true{% else %}false{% endif %},
        minusers: {{ supply.minusers }},
        maxusers: parseInt('{{ supply.maxusers }}'),
        bid: {% if supply.bid %}true{% else %}false{% endif %},
        conditions: {
            {% for condition in supply.conditions.all %}
                '{{ condition.id }}': {
                    type: '{{ condition.type }}',
                    amount: {{ condition.amount }},
                    description: '{{ condition.description }}'
                }
            {% endfor %}
        },
        maxbidconditions: {
            {% for condition in supply.maxbidconditions.all %}
                '{{ condition.id }}': {
                    type: '{{ condition.type }}',
                    amount: {{ condition.amount }},
                    description: '{{ condition.description }}'
                }
            {% endfor %}
        }
    }
    {% endfor %}
};

function adddropify() {
    var id = 'medias-' + newId();
    $('#medias .row')[0].insertAdjacentHTML(
        'beforeEnd',
        '<div class="col l3 m4 s12"><input type="file" multi=true id="'+ id +'" name="media-' + id + '" class="dropify" data-allowed-file-extensions="jpg jpeg" accept=".jpg,.jpeg" capture="true" data-max-file-size-preview="3M" /></div>'
        );

    var drEvent = $('#'+id).dropify({
        messages: {
            'default': 'Glissez-déposez un fichier ici ou cliquez',
            'replace': 'Glissez-déposez un fichier ici ou cliquez pour remplacer',
            'remove':  'Supprimer',
            'error':   'Ooops, une erreur est arrivée.'
        },
        error: {
            'fileSize': 'La taille du fichier doit être inférieur à {{ value }}.',
            'minWidth': 'La largeur de l\'image doit être supérieure à {{ value }}px.',
            'maxWidth': 'La largeur de l\'image doit être inférieure à {{ value }}px.',
            'minHeight': 'La hauteur de l\'image doit être supérieure à {{ value }}px.',
            'maxHeight': 'La hauteur de l\'image doit être inférieure à {{ value }}px.',
            'imageFormat': 'Le format de l\'image doit être de type {{ value }}.'
        }
    });

    drEvent.on('dropify.afterClear', function(event, element) {
        $('#carousel-' + event.target.id).remove();
        event.target.parentNode.parentNode.remove();
    });

    drEvent.on('change', function(event) {
        if (event.target.hasFile === undefined) {
            adddropify();
            setTimeout(function() {
                refreshcarousel();
                event.target.hasFile = true;
            }, 1000);
        }
    });
}

{% for media in product.medias.all %}

adddropify();

{% empty %}

adddropify();

{% endfor %}

function refreshcarousel() {
    $('.carousel').remove();
    document.getElementById('-image').insertAdjacentHTML(
        'beforeEnd',
        '<div class="carousel carousel-slider"></div>'
        );
    var carousel = $('.carousel')[0];
    var ids_files = [];
    var dropifies = $('.dropify');
    for(var i=0; i<(dropifies.length - 1); i++) {
        var dropify = dropifies[i];
        var img = $(dropify.parentNode).find('img');
        if (img.length === 0) {
            continue;
        }
        var src = img[0].src;
        if (src !== undefined) {
            ids_files.push([dropify.id, src]);
        }
    }
    ids_files.forEach(function(id_file) {
        carousel.insertAdjacentHTML(
            'beforeEnd',
            '<a id="carousel-' + id_file[0] + '" class="carousel-item" data-caption="' + document.getElementById('name').value + '" href="#one!"><img class="responsive-img" src="' + id_file[1] + '" /></a>'
            );
    });
    $('.carousel').carousel();
    $('.materialboxed').materialbox();
}

function updateProperty(name) {
    $('.' + name).filter(function(index, elt) {
        elt.innerHTML = document.getElementById(name).value;
    });
}

var defaultproperties = {
    name: {
        product: 'Appareil photo Nikon D80',
        stock: 'Garage voiture et moto',
        service: 'Cours de guitare'
    },
    shortdescription: {
        product: '10 millions de pixels, carte mémoire 2 Go',
        stock: '10 places en plein centre ville',
        service: 'Maximum 10 grans débutants',
    },
    description: {
        product: '',
        stock: '',
        service: ''
    }
};

function changeType(type) {
    dtype = types[type];
    document.getElementById('type').innerHTML = dtype.translation;
    document.getElementsByName('type')[0].setAttribute('value', type);

    for(var _type in types) {
        $('.' + _type).hide();
    }
    $('.' + type).show();
    for(var property in dtype) {
        var elt = document.getElementById(property);
        if (elt) {
            elt.setAttribute('placeholder', dtype[property]);
        }
    }
}

changeType('product');

var lowcategories = {
    //{% for lowcategory in lowcategories %}
    '{{ lowcategory.name }}': '{{ lowcategory.media.media.path.url }}',
    //{% endfor %}
};

function newEntrySet(divid, entrysettype, entrysetid) {
    if (entrysetid === undefined) {
        entrysetid = newId();
    }
    var html = '<table class="bordered striped highlight centered entryset ' + entrysettype + '" id="entryset-' + entrysettype + '-' + entrysetid + '"><thead><tr>';
    html += '<td>Type</td><td>Montant</td>';
    html += '<td>' + (entrysettype === 'supply' ? ('<a onclick="newEntrySet(\'' + divid + '\', undefined);" class="btn-floating blue" ><i class="material-icons">add</i></a>') : '') + '</td>';
    html += '</tr></thead>';
    html += '<tbody id="entry-content-' + new Date().getTime() + '"></tbody></table>';
    document.getElementById(divid).insertAdjacentHTML('beforeEnd', html);
    return $('#' + divid)[0];
}

function newEntry(entrysetid, entryid, type, amount) {
    if (entryid === undefined) {
        entryid = newId();
    }
    var html = '<tr class="' + entrysetid + '" id="entry-' + entryid + '">';
    html += '<td><input onchange="updateEntry(this);" class="entry-type" type="text" name="entry-type-' + entrysetid + '-' + entryid + '" value="' + type + '" placeholder="€, voiture, ..." /></td>';
    html += '<td><input onchange="updateEntry(this);" class="entry-amount" type="number" name="entry-amount-' + entrysetid + '-' + entryid + '" value="' + amount + '" placeholder="10" /></td>';
    html += '<td><a onclick="removeEntry(this);" class="btn-floating red"><i class="material-icons">remove</i></a></td></tr>';
    $('entry-type-' + entryid).autocomplete(
    {
        data: lowcategories,
        minLength: 1
    });
}

function updateEntry(elt) {
    var cls = elt.name.replace(elt.type === 'text' ? 'type' : 'amount', 'group');
    var empty = false;
    var jqcls = $(cls);
    for(var i =0; i<jqcls.length; i++) {
        var input = jqcls[i];
        empty = !Boolean(input.value);
    }
    if (emtpy) {
        removeEntry(elt);
    } else {
        var entryid = elt.parentNode.parentNode.parentNode.parentNode.id;
        var tds = $('#' + entryid + ' td');
        var tdslength = tds.length;
        [tds[tdslength - 2], tds[trslength - 3]].forEach(function(td) {
            empty = !Boolean(td.value);
        });
        if (empty) {
            newEntry(entrysettype);
        }
    }
}

function removeEntry(elt) {
    var body = elt.parentNode.parentNode.parentNode;
    elt.remove();
    if (body.childElementCount === 0) {
        newEntry(body.parentNode.id);
    }
}

function newSupply(supplytype, supplyid) {
    if (supplyid === undefined) {
        supplyid = newId();
    }
    var supply = supplyings[supplyid];

    var html = '<li id="supply-' + supplyid + '" class="collapsible supply-' + supplytype + ' data-collapsible="expandable">';

    html += '<div class="collapsible-header row">';

    html += '<div class="col s8 input-field">';
    html += '<input id="supply-name-' + supplyid + '" type="text" name="supply-name-' + supplyid + '" placeholder="Condition par voiture" />';
    html += '<label for="supply-name-' + supplyid + '">nom</label>'
    html += '</div>';

    html += '<div class="col offset-s2 s2>';
    html += '<a class="btn waves-effect waves-light" onclick="removeSupply(this);">';
    html += '<i class="material-icons">remove</i></a>';
    html += '</div>';

    html += '</div>';

    html += '<div class="collapsible-body row">';

    html += '<div class="col s8>';
    html += '<textarea name="supply-description-' + supplyid + '" placeholder="Description..."></textarea>';
    html += '</div>';

    html += '<div class="col s4>';
    html += '<input type="number" placeholder="1" value="1" name="supply-description-' + supplyid + '" placeholder="Description..."></textarea>';
    html += '</div>';

    html += '<div class="col s4>';
    html += '<input type="date" class="datepicker" id="supply-start-' + supplyid + '" name="supply-start-' + supplyid + '" />';
    html += '<label for="supply-start-' + supplyid + '"><i class="material-icons">date_range</i>début</label>';
    html += '</div>';

    html += '<div class="col s4>';
    html += '<input type="date" class="datepicker" id="supply-stop-' + supplyid + '" name="supply-stop-' + supplyid + '" />';
    html += '<label for="supply-stop-' + supplyid + '"><i class="material-icons">date_range</i>fin</label>';
    html += '</div>';

    html += '<div class="col s4>';
    html += '<input type="date" class="datepicker" id="supply-dates-' + supplyid + '" name="supply-dates-' + supplyid + '" />';
    html += '<label for="supply-dates-' + supplyid + '"><i class="material-icons">date_range</i>dates</label>';
    html += '</div>';

    html += '<div id="conds-' + supplyid + '" class="col s12></div>';

    html += '</div>';

    html += '</li>';

    document.getElementById(supplytype).insertAdjacentHTML('beforeEnd', html);
    newEntrySet('conds-' + supplyid);
}

function newId() {
    return new Date().getTime();
}

{% include 'categories.js' %}

{% include 'map.js' %}
