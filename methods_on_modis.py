# -*- coding:utf-8 -*-

###############################################################################
#该模块定义了对modis文件的操作的各种方法
#整个处理遥感数据需要的一些方法。
###############################################################################

import os
import gdal
import shutil
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from gdalconst import *

#检查素材文件夹是否存在，不存在建立
def checkEnv(names):
	for i in names:
		if os.path.exists(i):
			continue;
		else:
			os.mkdir(i)

#~ #返回形式为 [['0501.hdf', '0502.hdf'],['0601.hdf','0602.hdf']] 的文件索引
#~ #参数： folder为根目录，keywords为文件名的关键字
def getRasters(folder,keywords):
	result = []
	for root ,dirs,files in os.walk(folder):
		#只有显示二级目录
		if files ==[]:
			continue
		else:
			temp= []
			#连接文件名
			for name in files:
				str =  os.path.join(root,name)
				#根据关键字过滤
				for j in keywords:
					if j in str and 'xml' not in str:
						temp.append(str)
						break
		result.append(temp)
		
		
	return result

#遍历文件夹，只显示文件
def readFile(path):
	for root ,dirs,files in os.walk(path):
		#只有显示二级目录
		if files ==[]:
			continue
		else:
			temp= []
			#连接文件名
			for name in files:
				str =  os.path.join(root,name)
				temp.append(str)
		return temp
		
	


#输入path1, 输出 [ [band1,band2,...],[name1,name2...] ]
def getBandName(path):
	dataset = gdal.Open(path,GA_ReadOnly)
	#获取子波段
	subdatasets = dataset.GetSubDatasets()
	pathname=[]
	bandname=[]
	for i in subdatasets:
		#排除一个质量图层
		#~ if '[1x2400x2400]'in i[1]:
			#~ continue
		pathname.append(i[0])
		bandname.append(i[1])
	
	result = [pathname,bandname]
	dataset = None
	return result
	
#转换
def transHDF(infile,outfile):
	    os.system('gdal_translate %s %s -of GTiff' %(infile,'temp/'+outfile))  

#拼接
def merge(infiles,outfile):
	str=''
	for i in infiles:
		#过滤xml文件
		if 'xml' in i:
			continue
		str+=i+' '		
	os.system('gdal_merge.py -o %s -of GTiff %s' %(outfile,str))

#更改投影
def warp(infile,outfile):
	os.system('gdalwarp %s %s -r near -t_srs EPSG:900913' % (infile,outfile))
	return 'warp ok. generate'+outfile

#矢量图重投影	
def shpRepro(inshp,outshp):
	os.system('ogr2ogr -t_srs EPSG:900913 %s %s' % (outshp, inshp))


#从栅格图中裁剪
# -crop_to_cutline  忽略矢量图外部分
def mask(inshp,inraster,outraster):
	os.system('gdalwarp -cutline %s %s %s -crop_to_cutline'% (inshp,inraster,outraster) )
	
	return 'warp ok. generate'+outraster	
	
	
#生成缩略图
def makeThumbnail(src):
	dataset = gdal.Open(src)
	#判断数据集的波段数
	if(dataset.RasterCount<1):
		return
	if(dataset.RasterCount>1):
		ds = dataset.GetRasterBand(1).ReadAsArray()
	else:
		ds = dataset.ReadAsArray()
	
	A = np.array(ds)
	fig = plt.figure(frameon = False)    #生成画布
	ax = fig.add_subplot(111)             #增加子图
	ax.imshow(A, interpolation='nearest', vmin = 0,vmax = 16,cmap=plt.cm.gist_earth)    #子图上显示数据
	plt.savefig(src.replace('.tif','THUMBNAIL.png'),dpi = 80)
	ax.set_xticks([])                            #去除坐标轴
	ax.set_yticks([])
	plt.savefig(src.replace('.tif','.png'),dpi = 300)
	ds = None
	dataset = None











