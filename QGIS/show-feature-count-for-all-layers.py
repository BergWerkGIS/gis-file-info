root = QgsProject.instance().layerTreeRoot()
for lyr in root.findLayers():
    for prop in dir(lyr):
        #print prop
        pass
    #nodeType 1=layer, 0= group layer
    if lyr.nodeType() ==  1:
        lyr.setCustomProperty("showFeatureCount", True)
