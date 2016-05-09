var gdal = require('gdal');
gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');

var in_file = process.argv[2];

console.log('iterating:', in_file);
var cnt_null = 0;
var cnt_geom_invalid = 0;
try{
  ds = gdal.open(in_file);
  ds.layers.forEach(function(lyr) {
    console.log('------ ' + lyr.name);
    lyr.features.forEach(function(feat) {
      var geom = feat.getGeometry();
      //console.log(feat.fid);
      if (34087 !== feat.fid) { return;}
      if (null === geom) {
        console.error('NULL geom, fid:', feat.fid);
        cnt_null++;
        return;
      }
      if (!geom.isValid()) {
        console.error('geom invalid, fid:', feat.fid);
        cnt_geom_invalid++;
        return;
      }
    });
  });
}
catch(err){
	console.error('exception: ', err);
	if(gdal.lastError){
		console.error('last error: ', gdal.lastError);
	}
}

console.log('null geoms    : ', cnt_null);
console.log('invalid geoms : ', cnt_geom_invalid);

console.log('finished');
