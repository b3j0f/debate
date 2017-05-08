var votes = {
	organizations: {},
	debates: {}
};
{% for vote in user.account.votes %}
votes.
{% if vote.contactelement.type == 'Organization' %}
organizations
{% else %}
debates
{% endif %}
[{{ vote.id }}] = {id: {{ vote.id }}, eltid: {{ vote.elt.id }}, value: {{ vote.value }} };
{% endfor %}

function getUserVote(elt) {
	var votes_by_type = votes[elt.type];
	for(var vote of elt.votes) {
		if (votes_by_type.contains(vote.id)) {
			return vote;
		}
	}
}

function changeVote(type, id, eltid, value) {
	var vote = votes[type][id];
	var url = '{{ API }}votes/'
	var method ;
	if (vote === undefined) {
		method = 'POST';
		vote = {
			value: value,
			elt: eltid,
			account: {{ user.id }}
		};
	}
	if (votes[type].contains(id)) {
		method = 'PUT';
		url += id + '/';
		if(vote.value == value) {
			value = vote.value = 0;
		}
	}
	$.ajax(
		url,
		{
			data: vote
		},
		success: function(data) {
			$('#vote-' + id + '-dislike').removeClass('red');
			$('#vote-' + id + '-dislike').removeClass('white');
			$('#vote-' + id + '-like').removeClass('white');
			$('#vote-' + id + '-like').removeClass('green');
			if (value == 1) {
				$('#vote-' + id + '-like').addClass('green');
				$('#vote-' + id + '-dislike').addClass('white');
			} else if (value == -1) {
				$('#vote-' + id + '-dislike').addClass('red');
				$('#vote-' + id + '-like').addClass('white');
			} else {
				$('#vote-' + id + '-dislike').addClass('white');
				$('#vote-' + id + '-like').addClass('white');
			}
		}
	)
}