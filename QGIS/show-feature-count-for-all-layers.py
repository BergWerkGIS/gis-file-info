def show_feat_cnt(lyr):
    #nodeType 1=layer, 0= group layer
    if lyr.nodeType() ==  1:
        lyr.setCustomProperty("showFeatureCount", True)
    if lyr.nodeType() == 0:
        for lyr2 in lyr.findLayers():
            show_feat_cnt(lyr2)


root = QgsProject.instance().layerTreeRoot()
for lyr in root.findLayers():
    for prop in dir(lyr):
        #print prop
        pass
    show_feat_cnt(lyr)
