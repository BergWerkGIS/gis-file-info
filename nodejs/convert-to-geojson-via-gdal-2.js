var fs = require('fs');
var gdal = require('gdal');
var in_file = process.argv[2];
var out_name = process.argv[3];
var add_all_fields = process.argv[4] || false;
var ds = gdal.open(in_file);
var wgs84 = gdal.SpatialReference.fromEPSG(4326);

gdal.verbose();

//get all possible fields as we (could) be concatenating different layers
//eg kml or gpx (routes, tracks, ...)
var all_fields = [];
if (add_all_fields) {
	console.log('all fields of all layers:')
	ds.layers.forEach(function (lyr) {
		console.log('-----', lyr.name, '-----');
		lyr.fields.forEach(function (fld) {
			console.log('   -', fld.name);
			if (-1 === all_fields.indexOf(fld)) {
				all_fields.push(fld);
			}
		});
	});
}

if (fs.existsSync(out_name)) { fs.unlink(out_name);}
var out_ds = gdal.open(out_name, 'w', 'GeoJSON');
var geojson = out_ds.layers.create('blabla', wgs84, gdal.wkbGeometryCollection);

geojson.fields.add(new gdal.FieldDefn('layer', gdal.OFTString));
if (add_all_fields) {
    console.log('adding fields to output');
    all_fields.forEach(function (fld) {
        console.log('  -', fld.name, fld.type);
        geojson.fields.add(fld);
    });
}

var stop = false;
ds.layers.forEach(function (lyr) {
	if (stop) { return; }
	console.log('processing: ', lyr.name);
	if (0 === lyr.features.count(true)) {
		console.log('skipping: 0 features');
	}
	lyr.features.forEach(function (in_feat) {
		if (stop) { return;}
		var out_feat = new gdal.Feature(geojson);
		out_feat.setGeometry(in_feat.getGeometry());
		out_feat.fields.set('layer', lyr.name);
		if (add_all_fields) {
			all_fields.forEach(function (fld) {
				if (-1 !== in_feat.fields.indexOf(fld.name)) {
					out_feat.fields.set(fld.name, in_feat.fields.get(fld.name));
				}
			});
		}
		geojson.features.add(out_feat);
		//stop = true; //uncomment to stop after first feature
	})
	console.log('flush geojson');
	geojson.flush();
	return;
});

geojson.flush();
console.log('flush out_ds');
out_ds.flush();
console.log('close out_ds');
out_ds.close();

console.log('! DONE !');
