verbose = False
from qgis.gui import QgsRubberBand
canvas = iface.mapCanvas()
map_crs = canvas.mapRenderer().destinationCrs()
map_authid = map_crs.authid()
lyr = iface.activeLayer()
lyr_authid = lyr.crs().authid()
lyr_pnt = QgsVectorLayer('Point?crs=' + lyr_authid + '&index=yes', 'points', 'memory')
lyr_line = QgsVectorLayer('LineString?crs=' + lyr_authid + '&index=yes', 'lines', 'memory')
lyr_polygon = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'poly', 'memory')
lyr_bbox = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'bbox-features', 'memory')
lyr_bbox_parts = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'bbox-parts', 'memory')

#feats = lyr.getFeatures()
feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
xmin=180
ymin=90
xmax=-180
ymax=-90
cnt_single_part=0
cnt_multi_part=0
for feat in feats:
    bb = feat.geometry().boundingBox()
    if verbose: print bb.toString();
    xmin = xmin if xmin < bb.xMinimum() else bb.xMinimum()
    ymin = ymin if ymin < bb.yMinimum() else bb.yMinimum()
    xmax = xmax if xmax > bb.xMaximum() else bb.xMaximum()
    ymax = ymax if ymax > bb.yMaximum() else bb.yMaximum()

    feat_bb = QgsFeature()
    feat_bb.setGeometry(QgsGeometry.fromRect(bb))
    lyr_bbox.dataProvider().addFeatures([feat_bb])

    geom = feat.geometry()
    if geom.isMultipart():
        cnt_multi_part += 1
        if verbose:
            print feat.id(), 'multipart'
            print bb.toString()
        parts = geom.asGeometryCollection()
        if verbose: print 'parts:', len(parts);
        for part in parts:
            new_feat = QgsFeature()
            new_feat.setGeometry(part)
            #print 'wkbType:', part.wkbType()
            part_bb = QgsFeature()
            part_bb.setGeometry(QgsGeometry.fromRect(new_feat.geometry().boundingBox()))
            lyr_bbox_parts.dataProvider().addFeatures([part_bb])
            if part.wkbType() == QGis.WKBPoint:
                #print 'point:', part.exportToWkt()
                lyr_pnt.dataProvider().addFeatures([new_feat])
            elif part.wkbType() == QGis.WKBLineString:
                lyr_line.dataProvider().addFeatures([new_feat])
            else:
                #print 'polygon:', part.exportToWkt()
                lyr_polygon.dataProvider().addFeatures([new_feat])
    else:
        cnt_single_part += 1
        #print 'NO multipart'

    #if cnt_multi_part == 1:
    #    break

QgsMapLayerRegistry.instance().addMapLayers([lyr_pnt, lyr_line, lyr_polygon, lyr_bbox, lyr_bbox_parts])

print 'single part:', cnt_single_part
print 'multi part:' , cnt_multi_part
print 'feat cnt:', cnt_single_part + cnt_multi_part
print 'dataset bbox', xmin, ymin, xmax, ymax
print 'finished'
