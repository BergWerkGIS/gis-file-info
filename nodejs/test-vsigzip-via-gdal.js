var gdal = require('gdal');
gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');

console.log('GML Driver: ', gdal.drivers.get('GML'));
var ds =gdal.open('/vsigzip/hp40ne.gz');
ds.layers.forEach(function(layer){
    console.log('----', layer.name, '----');
    console.log("     number of features: " + layer.features.count());
    console.log("     fields: " + layer.fields.getNames());
    console.log("     extent: " + JSON.stringify(layer.extent));
    console.log("     srs: " + (layer.srs ? layer.srs.toProj4() : 'null'));
    layer.fields.forEach(function (fld) {
        console.log(fld.type);
    });
    //layer.features.forEach(function (feat) {
      //  console.log('feat:', feat.fid);
    //});
    var feat = layer.features.next();
    console.log('getfeature:\n', feat);
    console.log('fields:', feat.fields.toObject());
});
