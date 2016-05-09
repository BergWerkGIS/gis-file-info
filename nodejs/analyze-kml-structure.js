var gdal = require('gdal');
gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');

var ds = gdal.open(process.argv[2]);

var lyr_cnt = ds.layers.count();

console.log('layers:', lyr_cnt);
ds.layers.forEach(function (lyr) {
	var lyr_name = lyr.name;
	console.log(' -', lyr_name);
});

var lyr_shapes = ds.layers.get('Shapes');
lyr_shapes.features.forEach(function (feat) {
	console.log(feat.defn);
	feat.fields.forEach(function (fld) {
		console.log(fld);
	});
});

