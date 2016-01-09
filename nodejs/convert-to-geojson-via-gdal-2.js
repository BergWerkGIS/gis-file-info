var fs = require('fs');
var gdal = require('gdal');
var in_file = process.argv[2];
var out_name = process.argv[3];
var ds = gdal.open(in_file);
var wgs84 = gdal.SpatialReference.fromEPSG(4326);

if (fs.existsSync(out_name)) { fs.unlink(out_name);}
var out_ds = gdal.open(out_name, 'w', 'GeoJSON');
var geojson = out_ds.layers.create('blabla', wgs84, gdal.wkbGeometryCollection);
geojson.fields.add(new gdal.FieldDefn('layer', gdal.OFTString));
geojson.fields.add(new gdal.FieldDefn('style', gdal.OFTString));
geojson.fields.add(new gdal.FieldDefn('description', gdal.OFTString));

var stop = false;
ds.layers.forEach(function (lyr) {
	if (stop) { return;}
	console.log('processing: ', lyr.name);
	lyr.features.forEach(function (in_feat) {
		if (stop) { return;}
		var out_feat = new gdal.Feature(geojson);
		out_feat.setGeometry(in_feat.getGeometry());
		out_feat.fields.set('layer', lyr.name);
		out_feat.fields.set('style', in_feat.fields.get('Name'));
		out_feat.fields.set('description', in_feat.fields.get('description'));
		geojson.features.add(out_feat);
		//stop = true;
	})
	console.log('flush');
	geojson.flush();
	return;
});

out_ds.flush();
out_ds.close();
