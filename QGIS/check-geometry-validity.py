import os
from PyQt4.QtCore import QVariant

lyr = iface.activeLayer()
if lyr is None:
    raise Exception('select layer in TOC')

skip_cnt = 0
overall_vertex_cnt = 0
feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
for in_feat in feats:
    in_geom = in_feat.geometry()
    if in_geom.isMultipart():
        polygons = in_geom.asMultiPolygon()
    else:
        polygons = [in_geom.asPolygon()]
    for polygon in polygons:
        for ring in polygon:
            vertex_cnt = len(ring)
            overall_vertex_cnt += vertex_cnt
            if vertex_cnt > 1000:
                print in_feat.id(), vertex_cnt, 'vertices'
#            for vertex in ring:
#                if vertex[0] <= -180 or vertex[0] >= 180 or vertex[1] <= -90 or vertex[1] >= 90:
#                    print 'fid:', in_feat.id(), 'out of bounds:', vertex
    if in_geom is None:
        print in_feat.id(), 'NULL geometry, skipped'
        skip_cnt += 1
        continue
    if not in_geom.isGeosValid ():
       print in_feat.id(), 'NOT geos valid, skipped'
       skip_cnt += 1
       continue
    geom_errors = in_geom.validateGeometry()
    if len(geom_errors) > 0:
        print in_feat.id(), 'geometry NOT valid:'
        for geom_error in geom_errors:
            print geom_error.what()
        print in_feat.id(), 'skipped'
        skip_cnt += 1

print '-------'
print 'orig feature count', lyr.dataProvider().featureCount()
print 'analyzed features', len(feats)
print 'skipped:', skip_cnt
print 'overall_vertex_cnt', overall_vertex_cnt
print 'finished'