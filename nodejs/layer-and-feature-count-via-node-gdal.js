var gdal = require('gdal');

var ds = gdal.open(process.argv[2]);
console.log('layers:', ds.layers.count());
ds.layers.forEach(function (lyr) {
	console.log(' -', lyr.name);
});
ds.layers.forEach(function (lyr) {
	console.log('------------------------', lyr.name, '-----------------------');
	try {
		var feat_cnt = 0;
		lyr.features.forEach(function (feat) {
			feat_cnt++;
		});
		console.log('lyr.features.count():', lyr.features.count());
		console.log('feat_cnt:', feat_cnt);
	}
	catch (err) {
		console.error(err);
	}
});

console.log('!!! finished !!!');
