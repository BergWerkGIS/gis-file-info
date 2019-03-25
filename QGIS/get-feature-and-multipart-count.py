lyr = iface.activeLayer()
feats = lyr.selectedFeatures() if lyr.selectedFeatureCount() > 0 else lyr.getFeatures()
cnt_single_part=0
cnt_multi_part=0
cnt_null_geom=0
cnt_features_overall=0
mp_feats = {}
mp_vertices = {}
for feat in feats:
    geom = feat.geometry()
    if geom is None:
        cnt_null_geom += 1
        cnt_features_overall += 1
        continue
    if geom.isMultipart():
        cnt_multi_part += 1
        parts = geom.asGeometryCollection()
        cnt_features_overall += len(parts)
        mp_feats[feat.id()] = len(parts)
        vertex_cnt = 0
        parts = geom.asMultiPolygon()
        for ring in parts:
            for v in ring:
                vertex_cnt += len(v)
        mp_vertices[feat.id()] = vertex_cnt
    else:
        cnt_single_part += 1
        cnt_features_overall +=1

print('{0} "{1}"'.format(lyr.crs().authid(), lyr.crs().description()))
print

print('* single part features:', cnt_single_part)
print('* multi part features:' , cnt_multi_part)
print('* null geometry features:' , cnt_null_geom)
print('* sum of parts:', cnt_features_overall)
print('')

show_max = 10
show_cnt = 1
print('#### top', show_max, 'features with most multiparts')
print('')

hdr = 'fid | parts'
hdr2 = '----- | -----'
for fld in lyr.fields():
    hdr += ' | ' + fld.name()
    hdr2 += ' | -----'
print(hdr)
print(hdr2)
for key, val in sorted(mp_feats.items(), key=lambda kv: kv[1], reverse=True):
    req = QgsFeatureRequest(key)
    f = next(lyr.getFeatures(req))
    r = u'{0} | **{1}**'.format(key, val)
    for a in f.attributes():
        r += u' | {0}'.format(a)
    print(r)

    if show_cnt >= show_max:
        break
    show_cnt += 1


print('')
show_cnt = 1
print('#### top', show_max, 'features with most vertices')

print('')
hdr = 'fid | vertices'
hdr2 = '----- | -----'
for fld in lyr.fields():
    hdr += ' | ' + fld.name()
    hdr2 += ' | -----'
print(hdr)
print(hdr2)
for key, val in sorted(mp_vertices.items(), key=lambda kv: kv[1], reverse=True):
    req = QgsFeatureRequest(key)
    f = next(lyr.getFeatures(req))
    r = u'{0} | **{1}**'.format(key, val)
    for a in f.attributes():
        r += u' | {0}'.format(a)
    print(r)

    if show_cnt >= show_max:
        break
    show_cnt += 1

print('finished')