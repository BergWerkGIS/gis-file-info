import sys
from osgeo import gdal
ds = gdal.Open(sys.argv[1])
for i in range(ds.RasterCount):
	print "band", i, "calculating check sum ..."
	check_sum = ds.GetRasterBand(i+1).Checksum()
	print "band", i, "check sum:", check_sum
	error_type = gdal.GetLastErrorType()
	error_no = gdal.GetLastErrorNo()
	print "band", i, "error_no:", error_no, "error_type:", error_type, "\n"
	if error_type != 0 or error_no != 0:
		print "LastErrorMsg:", gdal.GetLastErrorMsg()
		print "exiting!!!! error band", i
		sys.exit(1)
sys.exit(0)
