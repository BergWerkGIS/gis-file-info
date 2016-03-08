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
    , src_lyr.wkbType()
    , src_prov.crs()
)
if writer.hasError() != QgsVectorFileWriter.NoError:
    print writer.errorMessage()
else:
    feats=src_lyr.getFeatures()
    invalid_cnt=0
    for feat in feats:
        geom = feat.geometry()
        if geom is None:
            print 'NULL geometry:', feat.id()
            invalid_cnt+=1
            continue
        if not geom.isGeosValid ():
            print feat.id(), 'NOT geos valid, skipped'
            invalid_cnt += 1
            #continue
            feat.setGeometry(geom.simplify(0.0))
        geom_errors = geom.validateGeometry()
        if len(geom_errors) > 0:
            print in_feat.id(), 'geometry NOT valid:'
            for geom_error in geom_errors:
                print geom_error.what()
            print in_feat.id(), 'skipped'
            invalid_cnt += 1
            
        writer.addFeature(feat)
    #cleanup and close writer
    del writer
    print 'features with error (dropped):', invalid_cnt
    print 'finished'