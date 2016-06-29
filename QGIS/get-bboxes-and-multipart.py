verbose = False
from PyQt4.QtCore import QVariant
from qgis.gui import QgsRubberBand
canvas = iface.mapCanvas()
map_crs = canvas.mapRenderer().destinationCrs()
map_authid = map_crs.authid()
lyr = iface.activeLayer()
lyr_authid = lyr.crs().authid()
fld_orig_fid = 'origfid'

lyr_pnt = QgsVectorLayer('Point?crs=' + lyr_authid + '&index=yes', 'points', 'memory')
lyr_pnt.dataProvider().addAttributes([QgsField(fld_orig_fid, QVariant.Int)])
lyr_pnt.updateFields()

lyr_line = QgsVectorLayer('LineString?crs=' + lyr_authid + '&index=yes', 'lines', 'memory')
lyr_line.dataProvider().addAttributes([QgsField(fld_orig_fid, QVariant.Int)])
lyr_line.updateFields()

lyr_polygon = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'poly', 'memory')
lyr_polygon.dataProvider().addAttributes([QgsField(fld_orig_fid, QVariant.Int)])
lyr_polygon.updateFields()

lyr_bbox = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'bbox-features', 'memory')
lyr_bbox.dataProvider().addAttributes([QgsField(fld_orig_fid, QVariant.Int)])
lyr_bbox.updateFields()

lyr_bbox_parts = QgsVectorLayer('Polygon?crs=' + lyr_authid + '&index=yes', 'bbox-parts', 'memory')
lyr_bbox_parts.dataProvider().addAttributes([QgsField(fld_orig_fid, QVariant.Int)])
lyr_bbox_parts.updateFields()

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

    feat_bb = QgsFeature(lyr_bbox.pendingFields())
    feat_bb.setGeometry(QgsGeometry.fromRect(bb))
    feat_bb.setAttribute(fld_orig_fid, feat.id())
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
            if part.wkbType() == QGis.WKBPoint:
                new_feat = QgsFeature(lyr_pnt.pendingFields())
            elif part.wkbType() == QGis.WKBLineString:
                new_feat = QgsFeature(lyr_line.pendingFields())
            else:
                new_feat = QgsFeature(lyr_polygon.pendingFields())
            new_feat.setGeometry(part)
            new_feat.setAttribute(fld_orig_fid, feat.id())
            #print 'wkbType:', part.wkbType()
            part_bb = QgsFeature(lyr_bbox_parts.pendingFields())
            part_bb.setGeometry(QgsGeometry.fromRect(new_feat.geometry().boundingBox()))
            part_bb.setAttribute(fld_orig_fid, feat.id())
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
