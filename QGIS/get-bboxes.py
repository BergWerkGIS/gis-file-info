lyr = iface.activeLayer()
feats = lyr.getFeatures()
xmin=180
ymin=90
xmax=-180
ymax=-90
vertices=0
for feat in feats:
    bb = feat.geometry().boundingBox()
    #print bb.toString()
    xmin = xmin if xmin < bb.xMinimum() else bb.xMinimum()
    ymin = ymin if ymin < bb.yMinimum() else bb.yMinimum()
    xmax = xmax if xmax > bb.xMaximum() else bb.xMaximum()
    ymax = ymax if ymax > bb.yMaximum() else bb.yMaximum()
    lines = feat.geometry().asPolyline()
    vertices+=len(lines)
print xmin, ymin, xmax, ymax
print vertices
