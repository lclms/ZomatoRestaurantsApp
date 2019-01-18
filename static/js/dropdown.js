'use strict';

function filldropdown(data) {

	var uniqueNames = [];
	data.forEach(function(d) {
		
		if (!uniqueNames.includes(d.city))
		{
			uniqueNames.push(d.city);
			$('#city_id').append($('<option>', {
				value: d.city,
				text: d.city
				}));
		}
		
	});
	
}

