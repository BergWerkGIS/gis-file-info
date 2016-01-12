'use strict';
var mapnikOmnivore = require('mapnik-omnivore');
var path = require('path');

var in_file = process.argv[2];
var file = path.resolve(in_file);

mapnikOmnivore.digest(file, function(err, metadata){
	if (err){
		console.log('err:\n', err);
	} else {
        console.log('metadata:\n');
        console.log(metadata);
	}
});