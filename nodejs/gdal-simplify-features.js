var util = require('util');
var gdal = require('gdal');

// gdal.verbose();
// gdal.config.set('CPL_DEBUG', 'ON');
// gdal.config.set('CPL_LOG_ERRORS', 'ON');

console.log('gdal version:', gdal.version);

var in_file = process.argv[2];
var simplify = +process.argv[3];
var out_file = process.argv[4];

var ds;
var ds_out;

console.log('iterating:', in_file);
var cnt_null = 0;
var cnt_geom_invalid = 0;
var cnt_feats = 0;

try {
  ds = gdal.open(in_file);
  ds_out = gdal.open(out_file, 'w', 'ESRI Shapefile');

  ds.layers.forEach(function (lyr) {
    console.log('------ ' + lyr.name);
    var shp_lyr = ds_out.layers.create(lyr.name, lyr.srs, lyr.geomType);

    lyr.features.forEach(function (feat) {
      cnt_feats++;
      var geom = feat.getGeometry();
      if (null === geom) {
        cnt_null++;
        console.error('geom NULL, fid:', feat.fid);
        return;
      }
      if (!geom.isValid()) {
        cnt_geom_invalid++;
        console.error('geom NOT valid, fid:', feat.fid);
        return;
      }
      var new_feat = new gdal.Feature(shp_lyr);
      var geom_simplified = geom.simplify(simplify);
      if (!geom_simplified.isValid) {
        console.log('new geom not valid');
      }
      //console.log(geom.toWKT(), geom_simplified.toWKT());
      // new_feat.setGeometry(geom);
      new_feat.setGeometry(geom_simplified);
      new_feat.fields.set(feat.fields.toObject());
      shp_lyr.features.add(new_feat);
    });

    shp_lyr.flush();
    shp_lyr = null;
  });
}
catch (err) {
  console.error('exception: ', err);
  if (gdal.lastError) {
    console.error('last error: ', gdal.lastError);
  }
}
finally {
  ds.close();
  ds = null;
  ds_out.flush();
  ds_out.close();
  ds_out = null;
}

console.log('-------------------------------------');
console.log('original features        : ', cnt_feats);
console.log('null geoms (dropped)     : ', cnt_null);
console.log('invalid geoms (droppped) : ', cnt_geom_invalid);

console.log('\n================');
console.log('--- finished ---');
console.log('================\n');
