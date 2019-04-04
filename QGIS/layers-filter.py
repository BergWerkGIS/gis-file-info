parent0 = 'SV'
lyrNames = ['admin_0.geom', 'admin_1.geom', 'admin_2.geom', 'admin_3.geom', 
  'postal_0.geom', 'postal_1.geom', 'postal_2.geom', 'postal_3.geom', 'postal_4.geom', 'postal_5.geom']

root = QgsProject.instance().layerTreeRoot()
model = iface.layerTreeView().layerTreeModel()

for lyrName in lyrNames:
    lyr = QgsProject.instance().mapLayersByName(lyrName)
    if not lyr:
        print('not found:', lyrName)
        continue
    else:
        lyr = lyr[0]
    lyr.setSubsetString('"parent_0"=\'%s\'' % parent0)
    # repaint map canvas
    lyr.triggerRepaint()
    # update toc
    node = root.findLayer(lyr.id())
    node.setCustomProperty("showFeatureCount", True)
    model.refreshLayerLegend(node)
