$('.add').hide();
$('.update').hide();
{% if elt %}
$('.update').show();
{% else %}
$('.add').show();
{% endif %}

var type = '{{ type }}';

var types = {
    topic: {
        translation: 'Sujet',
        name: 'Agir au lendemain des élections',
        shortdescription: '',
        description: ''
    },
    space: {
        translation: 'Endroit',
        name: 'Débats publics place de la République à Lille',
        shortdescription: '',
        description: ''
    },
    event: {
        translation: 'conférence',
        name: 'Agir au lendemain des élections tous les mardis',
        shortdescription: '',
        description: ''
    }
};

for(var _type in types) {
    $('.' + _type).hide();
}
$('.' + type).show();

var typesul = document.getElementById('types');
for(var type in types) {
    var html = '<li><h2><a onclick="changeType(\'' + type + '\');">' + types[type].translation + '</a></h2></li>'
    typesul.insertAdjacentHTML('beforeEnd', html);
}

var elt = {
    name: '{{ elt.name }}',
    description: '{{ elt.description }}',
    created: '{{ elt.created }}',
    contacts: [{% for contacts in elt.contacts.all %}'{{ contacts.id }}', {% endfor %}],
    tags: [{% for category in elt.tags.all %}'{{ category.id }}', {% endfor %}],
    public: {% if elt.public %}true{% else %}false{% endif %},
    medias: [{% for media in elt.medias.all %}'{{ media.url }}', {% endfor %}],
    address: '{{ elt.address }}',
    lon: '{{ elt.lon }}',
    lat: '{{ elt.lat }}',
    votes: { {% for vote in elt.votes %}{{ vote.id }}: {id: {{ vote.id }}, account: {{ vote.account.id }}, value: {{ vote.value }} }, {% endfor %}}
};

{% if elt %}
$('#contacts').material_chip({
    placeholder: 'Entrez un pseudo',
    secondaryPlaceholder: '+pseudo',
    data: [
        {% for contact in elt.contacts.all %}
        {% if contact.id != user.id %}
        {
            tag: '{{ contact.pseudo }}',
            image: '{{ contact.media.url }}',
            id: {{ contact.id }}
        },
        {% endif %}
        {% endfor %}
    ],
    autocompleteOptions: {
      data: {
        {% for user in users %}
        {% if user.id != user.id %}
        '{{ user.pseudo }}': '{{ user.media.url }}',
        {% endif %}
        {% endfor %}
      },
      limit: Infinity,
      minLength: 1
    }
});
for(var prop in elt) {
    try {
        $('#' + prop).val(elt[prop]);
    } catch {
    }
}
{% endif %}

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

{% for media in elt.medias.all %}

adddropify({{ media.url }});

{% empty %}

adddropify();

{% endfor %}

function updateProperty(name) {
    $('.' + name).filter(function(index, elt) {
        elt.innerHTML = document.getElementById(name).value;
    });
}

function changeType(type) {
    dtype = types[type];
    document.getElementById('type').innerHTML = dtype.translation;
    document.getElementsByName('type')[0].setAttribute('value', type);

    document.getElementById('formedit').action = '/' + type;

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

function newId() {
    return new Date().getTime();
}

{% if elt or type %}
changeType('{{ elt.type }}' || '{{ type }}');
{% else %}
changeType(Object.keys(types)[0]);
{% endif %}



{% include 'tags.js' %}

{% include 'map.js' %}
