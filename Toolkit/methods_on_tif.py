#!/usr/bin/env python
# -*- coding:utf-8 -*-
###############################################################################
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# Author : Robin   <zrb915@live.com> CHINA.
###############################################################################
#This script is used to contain some basic methods on Tif
# changes  20151020

try:
	from osgeo import gdal
except ImportError:
	import time
	
import sys
import numpy as np

def read_tif_as_array(input_file):
	src_ds = gdal.Open(input_file)
	if src_ds is None:
		print 'unable to opne %s' % input_file
		sys.exit(1)
	#打印包波段数      print band_num of  input_file
	print 'the band_num of input_file is %d' % src_ds.RasterCount
	temp = []
	for band in range(1,src_ds.RasterCount+1):
		try:
			src_band = src_ds.GetRasterBand(band)
			stats = src_band.GetStatistics(True,True)
			print "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (stats[0], stats[1], stats[2], stats[3] )
			src_array = src_band.ReadAsArray()
		except RuntimeError,e:
			print 'cant read band %s ' % band_num
			print e
			sys.exit(1)
		temp.append(src_array)
	temp = np.array(temp)  
	
	#改变维度      chane to sklearn style
	result = np.zeros((temp.shape[1],temp.shape[2],temp.shape[0]))
	result[:,:,0] = temp[0,:,:]
	result[:,:,1] = temp[1,:,:]
	result[:,:,2] = temp[2,:,:]
	del temp
	return result



#调试用
if __name__ == '__main__':
	data = read_tif_as_array('/home/robin/data/Landsatqhh.tif')
	print data.dtype
	print data.shape
	
	
		
	


		
		
	
	