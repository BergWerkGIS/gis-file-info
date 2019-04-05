#fine the point
pts = [QgsPoint(7685429,2782735),QgsPoint(7685480,2782761),QgsPoint(7685616,2782832),QgsPoint(7685999,2783098)]

polyLyrName = 'admin-split'
polyLyr = QgsProject.instance().mapLayersByName(polyLyrName)
if not polyLyr:
    raise Exception('polygon layer not found', polyLyrName)

polyLyr = polyLyr[0]
polyFeats = polyLyr.selectedFeatures() if polyLyr.selectedFeatureCount() > 0 else polyLyr.getFeatures()


#TODO: use CRS from project
lyrNearestPnts =  QgsVectorLayer('Point?crs=epsg:3857', 'nearest points' , "memory")
provNearestPnts = lyrNearestPnts.dataProvider()

#TODO: use CRS from project
lyrShortestLines =  QgsVectorLayer('LineString?crs=epsg:3857', 'shortest line' , "memory")
provShortestLines = lyrShortestLines.dataProvider() 

#get cut line
lyrCutLine = qgis.utils.iface.activeLayer()
cutLine = next(lyrCutLine.getFeatures())
cutLineGeom = cutLine.geometry()

for polyFeat in polyFeats:
    polyGeom = polyFeat.geometry()
    if polyGeom.isMultipart():
        polygons = polyGeom.asMultiPolygon()
    else:
        polygons = [polyGeom.asPolygon()]
        
    for polygon in polygons:
        for ring in polygon:
            for vertex in ring:
                #print(vertex)
                   
                #pt = QgsGeometry(vertex)
                pt = QgsGeometry.fromPointXY(vertex)

                distanceToPolygon = QgsGeometry.distance(pt, cutLineGeom)
                #print(distanceToPolygon)
                #if distanceToPolygon > 0 and distanceToPolygon < 2000:
                if distanceToPolygon == 0 or distanceToPolygon > 2000:
                    continue
                nearestPoint = cutLineGeom.nearestPoint(pt)
                shortLine = cutLineGeom.shortestLine(pt)

                pt = QgsFeature()
                pt.setGeometry(QgsGeometry(nearestPoint))
                provNearestPnts.addFeatures([pt])
                # update extent
                lyrNearestPnts.updateExtents()

                line = QgsFeature()
                #line.setGeometry(QgsGeometry.fromPolyline([point1,point2]))
                line.setGeometry(shortLine)
                provShortestLines.addFeatures([line])
                lyrShortestLines.updateExtents()

# add the layer to the canvas
QgsProject.instance().addMapLayers([lyrNearestPnts,lyrShortestLines])
