#!/usr/bin/env python
# -*- coding:utf-8 -*-


###############################################################################
#主函数
#完成了对批量modis文件的转换，拼接，重投影
#根据矢量图裁剪的工作
#输出文件夹    ./out
#输入文件夹    ./data       ./shp
#暂存文件夹    ./temp
###############################################################################


import os
import gdal
import shutil
import time
import numpy as np
from methods_on_modis import *
from gdalconst import *

#获取素材
checkEnv(['data','shp','temp','out'])
result = getRasters('data',['h26v05','h26v06','h25v05','h25v06'])

#temp为三层list
temp = []
#遍历不同数据文件夹
for folder in result:
	st = time.time()
	
	for i in folder:
		temp.append(getBandName(i))

	bnum = len(temp[0][0])
	#转换,b为波段
	for b in range(bnum):
		#由len(temp)个图合成
		#字符串处理，生成文件名
		a = str(temp[0][1][b]).split()
		bname =a[1]

		#生成文件夹名
		a =  str(temp[0][0][b]).split('"')
		fname = a[1][13:29]
		#1. 转换
		for i,j in zip(temp,range(1,len(temp)+1)):
			transHDF(i[0][b],str(j)) 
		#2. 拼接
		merge(readFile('temp'),'temp/merge')
		#3. 投影
		warp('temp/merge','temp/warp.tif')
		#4.  根据矢量图裁剪
		shpRepro('shp/qhubjxt.shp','temp/repro.shp')
		
		if(os.path.exists('out/'+fname)):
			m=1
		else:
			os.mkdir('out/'+fname)
		mask('temp/repro.shp','temp/warp.tif','out/'+fname+'/'+fname+bname+'.tif')
		
		#清空temp文件夹
		shutil.rmtree('temp')
		os.mkdir('temp')
		
		#生成两张缩略图
		if b == 0:
			src = 'out/'+fname+'/'+fname+bname+'.tif'
			makeThumbnail(src)
		
	et = time.time()	
	print '已输出到文件夹：'+fname,
	print '该数据集耗时：'+ str(et-st)+'  s'
	
