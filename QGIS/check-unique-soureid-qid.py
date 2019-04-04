lyr = iface.activeLayer()
if lyr is None:
    raise Exception('select admin layer in TOC')

#feat_cnt = lyr.featureCount()
#unique_ids = lyr.uniqueValues(lyr.fields().indexFromName('id'))
#if(feat_cnt != len(unique_ids)):
#    print('duplicate ids')
#unique_qids = lyr.uniqueValues(lyr.fields().indexFromName('qid'))
#if(feat_cnt != len(unique_qids)):
#    print('duplicate qids')

srcids = {}
qids = {}

# iterate through all features and use source_id/qid as key
# assign the feature id(s) as list
for feat in lyr.getFeatures():
    # source ids
    existing = feat['id'] in srcids
    if not existing:
        srcids[feat['id']] = [feat.id()]
    else:
        srcids[feat['id']].append(feat.id())
        
    # wikidata ids
    existing = feat['qid'] in qids
    if not existing:
        qids[feat['qid']] = [feat.id()]
    else:
        qids[feat['qid']].append(feat.id())

# feature ids of features with duplicate sourceid or qid
selection = []

# find source_ids that have more than one feature id assigned -> duplicate
dupliSrcIdFids = [fid for fid in srcids.values() if len(fid)>1]
if len(dupliSrcIdFids)>0:
    #extend selection list with list of feature ids
    selection.extend(dupliSrcIdFids[0])
    print(len(dupliSrcIdFids), 'duplicate source ids found, showing source_id and associated fids')
    print([item for item in srcids.items() if len(item[1])>1])
    
# find qids that have more than one feature id assigned -> duplicate
dupliQidFids = [fid for fid in qids.values() if len(fid)>1]
if len(dupliQidFids)>0:
    #extend selection list with list of feature ids
    selection.extend(dupliQidFids[0])
    print(len(dupliQidFids), 'duplicate qids found, showing qid and associated fids')
    print([item for item in qids.items() if len(item[1])>1])

#print(dupliSrcIdFids)
#print(dupliQidFids)

if len(selection)>0:
    #make fids in list unique in case we have duplicates here too
    #print(selection)
    tmp_set = set(selection)
    selection = list(tmp_set)
    #print(selection)
    print('duplicates found,', len(selection), 'features will be selected')
    lyr.selectByIds(selection)

print('done')