var gdal = require('gdal');

try{
	ds = gdal.open('unspecified.geojson');
}
catch(err){
	console.log('exception: ', err);
	if(gdal.lastError){
		console.log('last error: ', gdal.lastError);
	}
	return;
}

console.log('file ok - continue');
