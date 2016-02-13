from os import path
src_lyr=iface.activeLayer()
src_prov=src_lyr.dataProvider()
out_name=path.join(
    path.dirname(src_prov.dataSourceUri())
    ,'copy.shp'
)
print 'writing to:', out_name
writer = QgsVectorFileWriter(
    out_name
    , src_prov.encoding()
    , src_prov.fields()
    , QGis.WKBLineString
    , src_prov.crs()
)
if writer.hasError() != QgsVectorFileWriter.NoError:
    print writer.errorMessage()
else:
    feats=src_lyr.getFeatures()
    invalid_cnt=0
    for feat in feats:
        if feat.geometry() is None:
            #print 'invalid feature:', feat.id()
            invalid_cnt+=1
            continue
        writer.addFeature(feat)
    #cleanup and close writer
    del writer
    print 'NULL features (dropped):', invalid_cnt
