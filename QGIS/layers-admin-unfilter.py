lyrNames = ['admin_0.geom', 'admin_1.geom', 'admin_2.geom', 'admin_3.geom']

root = QgsProject.instance().layerTreeRoot()
model = iface.layerTreeView().layerTreeModel()

for lyrName in lyrNames:
    lyr = QgsProject.instance().mapLayersByName(lyrName)[0]
    lyr.setSubsetString('')
    # repaint map canvas
    lyr.triggerRepaint()
    # update toc
    node = root.findLayer(lyr.id())
    node.setCustomProperty("showFeatureCount", True)
    model.refreshLayerLegend(node)
