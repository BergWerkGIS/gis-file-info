var fs = require('fs');
var gdal = require("gdal");

if(process.argv.length<3){ return console.log('no tiff specified');}

var tiff_path=process.argv[2];
if(!fs.existsSync(tiff_path)){ return console.log('not found: ' + tiff_path);}


gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');
gdal.config.set('CPL_LOG', 'gdal-log.txt');
//gdal.config.set('CPL_LOG_APPEND', 'TRUE');

//hrm: not compiled for logging: Logging requires node-gdal be compiled with --enable_logging=true
//gdal.startLogging({filename:'node-gdal-log.txt'});

var dataset = gdal.open(tiff_path);
var bnd_cnt = dataset.bands.count();

for (var i = 0; i < bnd_cnt; i++) {
	console.log('band ' + i + ' calculating check sum ...')
	var check_sum = gdal.checksumImage(dataset.bands.get(i+1));
	console.log('band ' + i + ' check sum: ', check_sum);
	if (0 === check_sum) {
		console.log('band ' + i + ' check sum is 0!!!\nexiting');
		break;
	};
};

//gdal.stopLogging();

//console.log(gdal);