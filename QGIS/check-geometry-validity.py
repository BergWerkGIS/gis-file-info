import os
from PyQt4.QtCore import QVariant

lyr = iface.activeLayer()
if lyr is None:
    raise Exception('select layer in TOC')

skip_cnt = 0
null_cnt = 0
qgis_invalid_cnt = 0
overall_vertex_cnt = 0
feat_cnt = 0
feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
multipart_cnt = 0
geos_invalid_cnt = 0
for in_feat in feats:
    feat_cnt+=1
    in_geom = in_feat.geometry()
    if in_geom is None:
        print in_feat.id(), 'NULL geometry, skipped'
        skip_cnt += 1
        null_cnt += 1
        continue
    if in_geom.isMultipart():
        multipart_cnt +=1
        polygons = in_geom.asMultiPolygon()
    else:
        polygons = [in_geom.asPolygon()]
    part_idx = 0
    for polygon in polygons:
        if len(polygon) > 100:
            print 'fid:', in_feat.id(), 'rings:', len(polygon)
        ring_idx = 0
        for ring in polygon:
            vertex_cnt = len(ring)
            overall_vertex_cnt += vertex_cnt
            if vertex_cnt > 3000:
                print 'fid:', in_feat.id(), ' part:', part_idx, ' ring:', ring_idx, ' vertices:', vertex_cnt
#            for vertex in ring:
#                if vertex[0] <= -180 or vertex[0] >= 180 or vertex[1] <= -90 or vertex[1] >= 90:
#                    print 'fid:', in_feat.id(), 'out of bounds:', vertex
            ring_idx += 1
        part_idx += 1
    if not in_geom.isGeosValid ():
       print 'fid:', in_feat.id(), 'NOT geos valid'
       geos_invalid_cnt += 1
       continue
    geom_errors = in_geom.validateGeometry()
    if len(geom_errors) > 0:
        print 'fid:', in_feat.id(), 'geometry NOT valid:'
        for geom_error in geom_errors:
            print geom_error.what()
        print 'fid:', in_feat.id(), 'skipped'
        skip_cnt += 1
        qgis_invalid_cnt += 1

print '-------'
print 'layer feature count', lyr.featureCount()
print 'dataprovider feature count', lyr.dataProvider().featureCount()
print 'analyzed features', feat_cnt
print 'multipart features', multipart_cnt
print 'skipped:', skip_cnt
print 'null geometries', null_cnt
print 'qgis invalid:', qgis_invalid_cnt
print 'geos invalid', geos_invalid_cnt
print 'overall_vertex_cnt', overall_vertex_cnt
print 'finished'