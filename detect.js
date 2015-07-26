var fs = require('fs');
var gdal = require("gdal");

if(process.argv.length<3){ return console.log('no tiff specified');}

var tiff_path=process.argv[2];
if(!fs.existsSync(tiff_path)){ return console.log('not found: ' + tiff_path);}


gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');
gdal.config.set('CPL_LOG', 'gdal-log.txt');
//gdal.config.set('', );

//hrm: not compiled for logging: Logging requires node-gdal be compiled with --enable_logging=true
//gdal.startLogging({filename:'node-gdal-log.txt'});

var dataset = gdal.open(tiff_path);

dataset.bands.forEach(function(band){
	console.log(gdal.checksumImage(band));
});

//gdal.stopLogging();

console.log(gdal);