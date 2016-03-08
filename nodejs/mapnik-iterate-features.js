var path = require('path');
var mapnik = require('mapnik');

var in_shape = process.argv[2];
console.log('iterating:', in_shape);

mapnik.register_datasource(path.join(mapnik.settings.paths.input_plugins, 'shape.input'));
var ds = new mapnik.Datasource({ type: 'shape', file: in_shape });
var featureset = ds.featureset()

while ((feat = featureset.next())) {
	if (1594 == feat.id()) {
		console.log('-----------1594----------');
	}
	// for (var k in feat) {
	// 	console.log('\n' + k + ':\n' + feat[k]);
	// }
	console.log(feat.id(), feat.attributes(), feat.extent().join(','));
	if (1594 == feat.id()) {
		console.log(feat.toWKT());
		process.exit(0);
	}
}