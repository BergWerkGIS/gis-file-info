var gdal = require('gdal');

var ds = gdal.open(process.argv[2]);
var lyr_cnt = ds.layers.count();
console.log('layers:', lyr_cnt);
ds.layers.forEach(function (lyr) {
	console.log(' -', lyr.name);
});
var overall_feat_cnt=0;
ds.layers.forEach(function (lyr) {
	console.log('------------------------', lyr.name, '-----------------------');
	try {
		var feat_cnt = 0;
		lyr.features.forEach(function (feat) {
			feat_cnt++;
		});
		console.log('lyr.features.count():', lyr.features.count());
		console.log('feat_cnt:', feat_cnt);
		overall_feat_cnt+=feat_cnt;
	}
	catch (err) {
		console.error(err);
	}
});

console.log('layers:', lyr_cnt);
console.log('all features of all layers:', overall_feat_cnt);
console.log('!!! finished !!!');
