'use strict';
var mapnikOmnivore = require('mapnik-omnivore');
var path = require('path');

var file = path.resolve('RadrundeUebernKahlenberg.kml');

mapnikOmnivore.digest(file, function(err, metadata){
	if (err){
		console.log('err:\n', err);
	} else {
		console.log('metadata:\n', metadata);
	}
});