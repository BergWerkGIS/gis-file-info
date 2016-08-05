var util = require('util');
var gdal = require('gdal');
gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');

var in_file = process.argv[2];

console.log('iterating:', in_file);
var cnt_null = 0;
var cnt_geom_invalid = 0;
var cnt_all_vertices = 0;
var cnt_max_rings = 0;

try {
  ds = gdal.open(in_file);
  ds.layers.forEach(function (lyr) {
    console.log('------ ' + lyr.name);
    lyr.features.forEach(function (feat) {
      var geom = feat.getGeometry();
      if (null === geom) {
        console.error('geom NULL, fid:', feat.fid);
        cnt_null++;
        return;
      }
      var isValid = geom.isValid();
      var isSimple = geom.isSimple();
      var isRing = geom.isRing();
      var hasChildren = geom.children ? true : false;
      var ringCnt = 0;
      if (!isValid) {
        cnt_geom_invalid++;
      }

      var vertices = 0;

      if (hasChildren) {
        //TODO
      }

      if (geom.rings) {
        ringCnt = geom.rings.count();
        cnt_max_rings = Math.max(cnt_max_rings, ringCnt);
        geom.rings.forEach(function (ring, idx) {
          var pnt_cnt = ring.points.count();
          vertices += pnt_cnt;
          if (pnt_cnt >= 3000) {
            console.log(util.format(
              '    fid %s ring %s: %s vertices'
              , feat.fid
              , idx
              , pnt_cnt
            ));
          }
        });
      }

      cnt_all_vertices += vertices;

      if ((vertices >= 10000 || !isValid) && ringCnt > 0) {
        console.log(util.format(
          'fid %s: %s vertices'
          , feat.fid
          , vertices
        ));
        console.log(util.format(
          'fid:%s wkbType:%s geom:(%s,%s,%s) children:%s rings:%s\n~~~~~~~~~~~~~~~~'
          , feat.fid
          , gdal.wkbPolygon25D === geom.wkbType ? 'wkbPolygon25D' : geom.wkbType
          , isValid ? 'valid' : '-------------------- !!!! NOT valid !!! -------------'
          , isSimple ? 'simple' : 'NOT simple'
          , isRing ? 'ring' : 'NOT ring'
          , !hasChildren ? 'no' : geom.children.count()
          , ringCnt === 0 ? 'no' : ringCnt
        ));
      }

      if (3818 ===feat.fid) {
        console.log(geom.toWKT());
      }
    });
  });
}
catch (err) {
  console.error('exception: ', err);
  if (gdal.lastError) {
    console.error('last error: ', gdal.lastError);
  }
}

console.log('------------------------------');
console.log('null geoms    : ', cnt_null);
console.log('invalid geoms : ', cnt_geom_invalid);
console.log('max rings     : ', cnt_max_rings);
console.log('all vertices  : ', cnt_all_vertices);

console.log('--- finished ---');
