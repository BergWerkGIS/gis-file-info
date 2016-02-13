var fs = require('fs');
var gdal = require('gdal');
var in_file = process.argv[2];
var out_base_name = process.argv[3];
var ds = gdal.open(in_file);
var wgs84 = gdal.SpatialReference.fromEPSG(4326);

gdal.verbose();

ds.layers.forEach(function (lyr) {
	console.log('processing: ', lyr.name);
	var lyr_name = lyr.name.replace(':', ''); //strip invalid filename characters
	var out_name = out_base_name + '_' + lyr_name + '.geojson';
	if (fs.existsSync(out_name)) { fs.unlink(out_name);}
	var out_ds = gdal.open(out_name, 'w', 'GeoJSON');
	var geojson = out_ds.layers.create(lyr_name, wgs84, lyr.geomType);
	lyr.features.forEach(function (in_feat) {
		geojson.features.add(in_feat);
	})
	geojson.flush();
	out_ds.flush();
	out_ds.close();
});