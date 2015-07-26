import sys
from osgeo import gdal
ds = gdal.Open(sys.argv[1])
for i in range(ds.RasterCount):
	print "band", i, "calculating check sum"
	check_sum = ds.GetRasterBand(i+1).Checksum()
	print "band", i, "check sum:", check_sum
	error_type = gdal.GetLastErrorType()
	print "band", i, "error_type:", error_type
	if error_type != 0:
		print "exiting!!!! error band", i
		sys.exit(1)
sys.exit(0)
