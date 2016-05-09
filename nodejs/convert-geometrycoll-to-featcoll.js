var fs = require('fs');
var gdal = require('gdal');
var in_file = process.argv[2];
var out_file = process.argv[3];
var ds_in = gdal.open(in_file);
var wgs84 = gdal.SpatialReference.fromEPSG(4326);

if (fs.existsSync(out_file)) { fs.unlink(out_file); }

var out_ds = gdal.open(out_file, 'w', 'GeoJSON');

gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');


ds_in.layers.forEach(function (lyr) {
    console.log('processing: ', lyr.name);
    var geojson = out_ds.layers.create(lyr.name, wgs84, gdal.wkbGeometryCollection);
    lyr.features.forEach(function (in_feat) {
        var in_geom = in_feat.getGeometry();
        if (in_geom.wkbType !== gdal.wkbGeometryCollection) {
            console.log('regular feature');
            geojson.features.add(in_feat);
        } else {
            console.log('geometry collection');
            in_geom.children.forEach(function (child_geom, idx) {
                //console.log('geomColl:', idx);
                var out_feat = new gdal.Feature(geojson);
                out_feat.setGeometry(child_geom);
                geojson.features.add(out_feat);
            });
        }
    })
    geojson.flush();
    out_ds.flush();
    out_ds.close();
});