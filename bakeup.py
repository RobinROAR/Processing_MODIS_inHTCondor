#!/usr/bin/env python
# -*- coding:utf-8 -*-  

import os  
import time



#检查素材文件夹是否存在，不存在建立
def checkEnv(names):
	for i in names:
		if os.path.exists(i):
			continue;
		else:
			os.mkdir(i)
			


#返回形式为 [['0501.hdf', '0502.hdf'],['0601.hdf','0602.hdf']] 的文件索引
#参数： folder为根目录，keywords为文件名的关键字
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


#转换
def transHDF(infiles,outfiles):
	
	for i,j in zip(infiles,outfiles):
	    os.system('gdal_translate %s %s -of GTiff' %("HDF4_EOS:EOS_GRID:\'"+i+"\':MOD12Q1:Land_Cover_Type_1",'temp/'+j))  

	et = time.time()

#拼接
def merge(infiles,outfile):
	
	str=''
	for i in infiles:
		str+=i+' '		
	os.system('gdal_merge.py -o %s -of GTiff %s' %(outfile,str))

#更改投影
def warp(infile,outfile):
	os.system('gdalwarp %s %s -r near -t_srs EPSG:900913' % (infile,outfile))
	return 'warp ok. generate'+outfile
	



if __name__ == "__main__":
	checkEnv(['data','shp','temp'])
	
	
	files = getRasters('data',['h26v05','h26v06','h25v05','h25v06'])

	for i in files:
		infiles = i
		

		outfiles=['1.tif',
			'2.tif',
			'3.tif',
			'4.tif']

		transHDF(infiles,outfiles)

		
		infiles = ['temp/1.tif',
			'temp/2.tif',
			'temp/3.tif',
			'temp/4.tif']
		outfile = 'temp/merge.tif'
		
		merge(infiles,outfile)
		warp('temp/merge.tif','warp.tif')



	