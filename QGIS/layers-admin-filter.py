parent0 = 'HN'
lyrNames = ['admin_0.geom', 'admin_1.geom', 'admin_2.geom', 'admin_3.geom']

root = QgsProject.instance().layerTreeRoot()
model = iface.layerTreeView().layerTreeModel()

for lyrName in lyrNames:
    lyr = QgsProject.instance().mapLayersByName(lyrName)[0]
    lyr.setSubsetString('"parent_0"=\'%s\'' % parent0)
    # repaint map canvas
    lyr.triggerRepaint()
    # update toc
    node = root.findLayer(lyr.id())
    node.setCustomProperty("showFeatureCount", True)
    model.refreshLayerLegend(node)
