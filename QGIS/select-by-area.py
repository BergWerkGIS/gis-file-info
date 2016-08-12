import os
from PyQt4.QtCore import QSettings
import distutils
from distutils import util

#https://github.com/qgis/QGIS/blob/f38856e7381519431f828cc890bc8b33a8f2a544/src/gui/qgsmaptoolidentify.cpp#L413-L427

#min area in canvas units <- selected display projection
#e.g. WebMerc 100km2 = 100000000m2
min_area= 100000000
sel_features = []

lyr = iface.activeLayer()
if lyr is None:
    raise Exception('select layer in TOC')

print 'min_area:', min_area
print 'layer:', lyr.name()

displayAreaUnits = QgsUnitTypes.distanceToAreaUnit(iface.mapCanvas().mapUnits())
print 'displayAreaUnits:', displayAreaUnits

settings = QSettings()
baseUnit = bool(distutils.util.strtobool(settings.value( "/qgis/measure/keepbaseunit", False )))
print 'baseUnit:', baseUnit

ellipsoid = QgsProject.instance().readEntry( "Measure", "/Ellipsoid", GEO_NONE )
print 'ellipsoid:', ellipsoid
calc = QgsDistanceArea()
calc.setEllipsoidalMode(iface.mapCanvas().hasCrsTransformEnabled())
calc.setEllipsoid( ellipsoid[0] )
src_srs = lyr.crs().srsid()
print 'src_srs:', src_srs
calc.setSourceCrs(src_srs)
#calc.setSourceCrs(3857)

#feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
feats = lyr.getFeatures()
for feat in feats:
    area = calc.measureArea(feat.geometry())
    #print feat.id(), ':', area
    area = calc.convertAreaMeasurement(area, displayAreaUnits)
    #print feat.id(), ':', area
    if area >= min_area:
        sel_features.append(feat.id())
        #print as readable string
        #area = QgsDistanceArea.formatArea(area, 3, displayAreaUnits, baseUnit)
        #print feat.id(), ':', area

lyr.setSelectedFeatures(sel_features)
print 'feats to select:', len(sel_features)
print 'selectedFeatureCount():', lyr.selectedFeatureCount()