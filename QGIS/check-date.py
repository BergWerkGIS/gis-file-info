date = '2018'
lyrName = 'division.geom'

lyr = QgsProject.instance().mapLayersByName(lyrName)
if not lyr:
    raise Exception(u'layer {} not found'.format(lyrName))

lyr = lyr[0]
print(u'checking layer {}'.format(lyr.name()))
filter = QgsFeatureRequest().setFilterExpression ( u'"date"!=\'{}\''.format(date))
for feat in lyr.getFeatures(filter):
    print('id:', feat['id'], feat['type'], 'level:', feat['level'], 'name:', feat['name'], 'name_ascii:', feat['name_ascii'], 'date:', feat['date'])
print('done checking', lyr.name())
