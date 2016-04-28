lyr = iface.activeLayer()
ext=lyr.extent()
xmin=ext.xMinimum()
ymin=ext.yMinimum()
xmax=ext.xMaximum()
ymax=ext.yMaximum()
canvas=iface.mapCanvas
crsSrc = QgsCoordinateReferenceSystem(3857)
crsDest = QgsCoordinateReferenceSystem(4326)
xform = QgsCoordinateTransform(crsSrc, crsDest)
pt1 = xform.transform(QgsPoint(xmin,ymin))
pt2 = xform.transform(QgsPoint(xmax,ymax))
print pt1, "/", pt2
 