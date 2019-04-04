# the shapefile(!!!) has to be the selected layer in the TOC

# uncomment the layer to check
#lyrName = 'admin_1.geom'
lyrName = 'admin_2.geom'
#lyrName = 'admin_3.geom'

#clear the Python Console, comment if you don't want it
from PyQt5.QtWidgets import QDockWidget
consoleWidget = iface.mainWindow().findChild( QDockWidget, 'PythonConsole' )
consoleWidget.console.shellOut.clearConsole()

adminLyr = QgsProject.instance().mapLayersByName(lyrName)[0]
shpLyr = iface.activeLayer()
print (u'using admin layer "{0}" and shapefile "{1}"'.format(adminLyr.name(), shpLyr.name()))
shpFeatures = shpLyr.getFeatures()
faultyNames = []
for featShp in shpFeatures:
    #get properties from shapefile
    shpId = featShp["ID"]
    shpName = featShp["Name"]
    shpNameAscii = featShp["Name_ASCII"]
    #filter admin layer by name and source ID (several features might have the same name)
    #filter = QgsFeatureRequest().setFilterExpression ( u'"name"=\'{0}\''.format(shpName))
    filter = QgsFeatureRequest().setFilterExpression ( u'"name"=\'{0}\' AND "source_id"=\'{1}\''.format(shpName, shpId))
    #filter = QgsFeatureRequest().setFilterExpression ( u'"source_id"=\'{}\''.format(shpId))
    #filter = QgsFeatureRequest().setFilterExpression ( u'"name_ascii"=\'{0}\' AND "source_id"=\'{1}\''.format(shpNameAscii, shpId))
    adminFeatures = list(adminLyr.getFeatures(filter))
    adminFeatCnt = len(adminFeatures)
    if adminFeatCnt < 1:
        faultyNames.append({'fid':featShp.id(),'srcId':shpId,'shpName':shpName,'shpNameAscii':shpNameAscii,'lyrName':adminLyr.name()})
        #print("XXXX srcId:{0} name:'{1}' nameASCII:'{2}' not found in {3}".format(shpId, shpName, shpNameAscii, adminLyr.name()))
    elif adminFeatCnt > 1:
        faultyNames.append({'fid':featShp.id(),'srcId':shpId,'shpName':shpName,'shpNameAscii':shpNameAscii,'lyrName':adminLyr.name()})
        print("'{0}' found more than once in {1}".format(shpName, adminLyr.name()))
    else:
        #print(u'{0}: ok'.format(shpName))
        pass
    
# print info about names not found
if len(faultyNames) > 0:
    #sort mismatches by source ID
    for faulty in sorted(faultyNames, key = lambda f: f['srcId']):
        print("srcId:{0} name:'{1}' nameASCII:'{2}' not found in {3}".format(faulty['srcId'], faulty['shpName'], faulty['shpNameAscii'], faulty['lyrName']))
    #select features in shapefile
    faultyFids = [f['fid'] for f in faultyNames]
    shpLyr.selectByIds(faultyFids)
    #try to select features in admin layer by source id
    srcIds = [f['srcId'] for f in faultyNames]
    exp = u'"source_id" in ({})'.format(','.join(srcIds))
    #print(exp)
    adminLyr.selectByExpression(exp)

print('number of features:')
print(u'{0} "{1}"'.format(adminLyr.featureCount(), adminLyr.name()))
print(u'{0} "{1}"'.format(shpLyr.featureCount(), shpLyr.name()))

print('done, {0} features with no exact(!) match (source id AND name)'.format(len(faultyNames)))
