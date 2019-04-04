access_geom = True

import os
from PyQt5.QtCore import QVariant

lyr = iface.activeLayer()
if lyr is None:
    raise Exception('select layer in TOC')

feat_cnt = 0
feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
for feat in feats:
    feat_cnt+=1
    #print('fid:', feat.id())
    if feat_cnt % 1000 == 0:
        print('fid:', feat.id())
    if access_geom:
        geom = feat.geometry()
        #print(geom.type())
        #print(geom.boundingBox().toString())
        if not geom.isGeosValid ():
          print(feat.id(), 'NOT geos valid')
        #line = geom.asPolyline()
        #print(len(line))
        geom_errors = geom.validateGeometry()
        if len(geom_errors) > 0:
            print(feat.id(), 'geometry NOT valid:')
            for geom_error in geom_errors:
                print(geom_error.what())
        
print('-------')
print('iterated features', feat_cnt)
print('layer feature count', lyr.featureCount())
print('dataprovider feature count', lyr.dataProvider().featureCount())
print('finished')
