#!/usr/bin/env python
# -*- coding:utf-8 -*-  

from osgeo import gdal,osr,ogr
import matplotlib.pyplot as plt


#显示多张图片

def showTifs():
	lc_data1 = gdal.Open ( 'HDF4_EOS:EOS_GRID:"data/MCD12Q1.A2012001.h25v06.051.2014288202556.hdf":MOD12Q1:Land_Cover_Type_1' )
	lc_data2= gdal.Open('out1/tif-nopro/MCD12Q1.A2012001.h25v05.051.2014288202540_MOD12Q1.tif')
	lc_data3 = gdal.Open('out1/tif-wgs/MCD12Q1.A2012001.h25v05.051.2014288202540_MOD12Q1.tif')
	lc_data4= gdal.Open('out1/tif-utm/MCD12Q1.A2012001.h25v05.051.2014288202540_MOD12Q1.tif')


	data = [lc_data1,lc_data2,lc_data3,lc_data4]
	fig = plt.figure()
	num=221
	for i in data:
		lc = i.ReadAsArray()
		print "detail: ", (lc.min(), lc.max(), lc.mean(), lc.std())
		
		ax = fig.add_subplot(num)    #num为子图的坐标
		im = ax.imshow(lc,interpolation='nearest', vmin=0,vmax=16,cmap=plt.cm.gist_earth)   #生成二维图，插入点的方式为最近邻，最小值为0,最大值为16,参考颜色为gist-earth
		print num,i," has finished"
		plt.colorbar(im)                      #子图增加颜色条
		num+=1

	plt.show()


#显示一张图片
def showTif():
	src = 'out/MCD12Q1.A2012001/MCD12Q1.A2012001Land_Cover_Type_1.tif'
	ds = gdal.Open(src)
	lc = ds.ReadAsArray()   #以数组方式获取数据

	detail = (lc.min(), lc.max(), lc.mean(), lc.std())
	print detail

	proj = ds.GetProjection()  #获取投影

	print proj
	print lc.shape

	plt.imshow ( lc, interpolation='nearest', vmin=0,vmax = 16,cmap=plt.cm.gist_earth)     #显示图像
	plt.colorbar()  #添加颜色条
	plt.show()
	
	

#调试用方法
if __name__ == "__main__":
	showTif()