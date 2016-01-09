lyr = iface.activeLayer()
feats = lyr.getFeatures()
cnt_single_part=0
cnt_multi_part=0
cnt_features_overall=0
for feat in feats:
    geom = feat.geometry()
    if geom.isMultipart():
        cnt_multi_part += 1
        parts = geom.asGeometryCollection()
        cnt_features_overall += len(parts)
    else:
        cnt_single_part += 1
        cnt_features_overall +=1

print 'single part features:', cnt_single_part
print 'multi part features:' , cnt_multi_part
print 'all features:', cnt_features_overall
