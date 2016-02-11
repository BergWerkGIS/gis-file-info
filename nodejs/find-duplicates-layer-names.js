var gdal = require('gdal');

var ds = gdal.open(process.argv[2]);

var lyr_cnt = ds.layers.count();
var lyr_name_cnt = {};

console.log('layers:', lyr_cnt);
console.log('unique layer names:')
ds.layers.forEach(function (lyr) {
	var lyr_name = lyr.name;
	if (lyr_name in lyr_name_cnt) {
		//console.log(' -', lyr.name, '\talready found');
		lyr_name_cnt[lyr_name]++;
	} else {
		lyr_name_cnt[lyr_name] = 1;
		console.log(' -', lyr_name);
	}
});

var duplicates = false;
for (var name in lyr_name_cnt) {
	var cnt = lyr_name_cnt[name];
	if (cnt > 1) {
		console.log('lyr [' + name + '] found ' + cnt + ' times');
		duplicates = true;
	}
}

if (duplicates) {
	console.log('!!! not valid - duplicate layer names !!!');
}