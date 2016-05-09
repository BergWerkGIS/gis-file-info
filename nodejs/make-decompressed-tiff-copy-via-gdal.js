var fs = require('fs');
var util = require('util');
var gdal = require('gdal');
gdal.verbose();
gdal.config.set('CPL_DEBUG', 'ON');
gdal.config.set('CPL_LOG_ERRORS', 'ON');

if(process.argv.length<3){ return console.log('no tiff specified');}

gdal.config.set('GTIFF_IGNORE_READ_ERRORS', 'TRUE');
gdal.config.set('GDAL_CACHEMAX', '1500');


var infile = process.argv[2];
var outfile = infile + '-copy.tif';

if(fs.existsSync(outfile)){
	console.log('deleting existing outfile');
	fs.unlinkSync(outfile);
}

var copyoptions = {
	"BIGTIFF": "YES",
	"COMPRESS":"NONE",
	"TILED": "YES",
	"BLOCKXSIZE": "512",
	"BLOCKYSIZE": "512"
};


function show_gdal_error(){
	if (gdal.lastError) {
		var le = gdal.lastError;
		console.log(util.format('last error:\n  code  : %d\n  level : %d\n  msg   : %s', le.code, le.level, le.message));
	}
};


function make_decompressed_copy(callback) {
	var ds;
	try {
		console.log('opening source');
		ds = gdal.open(infile);
		ds.bands.forEach(function (band, i) {
			console.log('band', i);
			var check_sum = gdal.checksumImage(band);
			show_gdal_error();
			console.log('checksum:', check_sum);
		});
	}
	catch (err) {
		return callback('gdal open: ' + err);
	}

	var driver = gdal.drivers.get('GTiff');

	try {
		console.log('creating copy...');
		var dscopy = driver.createCopy(outfile, ds, copyoptions);
		show_gdal_error();
		dscopy.bands.forEach(function (band, i) {
			console.log('copy band', i);
			var check_sum = gdal.checksumImage(band);
			show_gdal_error();
			console.log('checksum:', check_sum);
		});
		ds.close();
		dscopy.close();
		console.log('copy finished');
		callback(null);
	}
	catch (err) {
		return callback('create copy: ' + err);
	}
};


function verify_copy(callback){
	try {
		console.log('verifying copy');
		var ds = gdal.open(outfile);
		ds.bands.forEach(function (band, i) {
			console.log('verify copy band', i);
			var check_sum = gdal.checksumImage(band);
			show_gdal_error();
			console.log('checksum:', check_sum);
		});
		ds.close();
		callback(null);
	}
	catch (err) {
		callback('verfify copy:', err);
	}
};


function add_overviews(callback){
	try {
		console.log('adding overviews');
		var ds = gdal.open(outfile);
		ds.buildOverviews('NEAREST', [2,4,8,16]);
		show_gdal_error();
		ds.close();
		callback(null);
	}
	catch (err) {
		callback('add overviews:', err);
	}
};


make_decompressed_copy(function (err) {
	if (err) {
		console.log(err);
		process.exit(1);
	}
	verify_copy(function(err){
		if (err) {
			console.log(err);
			process.exit(1)
		};
		add_overviews(function(err){
			if(err){
				console.log(err);
				process.exit(1);
			}
		});
	});
});