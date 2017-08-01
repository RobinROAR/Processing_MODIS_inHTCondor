#!/usr/bin/env python
# -*- coding:utf-8 -*-

###############################################################################
#主函数
#完成了对批量modis文件的转换，拼接，重投影
#根据矢量图裁剪的工作
#输出文件夹    ./out
#输入文件夹    ./data       ./shp
#暂存文件夹    ./temp
# Author : Robin   <zrb915@live.com> CHINA.
###############################################################################
# changes @ 20151021,  add Usage(),main()


try:
    from osgeo import gdal
except ImportError:
    import gdal
import os
import shutil
import time
import sys
import numpy as np
from methods_on_modis import *
from gdalconst import *

def Usage():
    print("""
    $ main.py  
    """)
    sys.exit(1)

def main():
	#获取素材
	checkEnv(['data','shp','temp','out'])
	result = getRasters('data',['h26v05','h26v06','h25v05','h25v06'])

	#temp为三层list
	temp = []
	#遍历不同数据文件夹
	stime = time.time()
	for folder in result:
		print '新作业开始',folder
		st = time.time()
		
		for i in folder:
			temp.append(getBandName(i))

		bnum = len(temp[0][0])
		#转换,b为波段,bnum为波段总数
		for b in range(bnum):
			#由len(temp)个图合成
			#字符串处理，生成文件名
			# a = str(temp[0][1][b]).split() # commented by neptune;
			# added by neptune;
			a = str(temp[0][1][b])
			bname = a[a.index(' ')+1:a.rindex('(')-1]
			bname = bname.replace(' ', '_')
			# end of add;
			#bname =a[1] # commented by neptune;
			#生成文件夹名
			a =  str(temp[0][0][b]).split('"')[1].split('/')[-1].split('.')
			fname  = ''.join(a[:2])
			#1. 转换
			for i,j in zip(temp,range(1,len(temp)+1)):
				transHDF(i[0][b],str(j)) 
			#2. 拼接
			merge(readFile('temp'),'temp/merge')
			#3. 投影
			warp('temp/merge','temp/warp.tif')
			#4.  根据矢量图裁剪
			shpRepro('shp/qhlake_102113.shp','temp/repro.shp')
			if(os.path.exists('out/'+fname)):
					m=1
			else:
					os.mkdir('out/'+fname)
			mask('temp/repro.shp','temp/warp.tif','out/'+fname+'/'+fname+'_'+bname+'.tif')  # modified by neptune by add '_' between fname and bname
			
			#清空temp文件夹
			shutil.rmtree('temp')
			os.mkdir('temp')
			
			#生成两张缩略图
			if b == 0:
					src = 'out/'+fname+'/'+fname+'_'+bname+'.tif'   # modified by neptune by add '_' between fname and bname
					makeThumbnail(src)

		#清空文件夹名索引	
		temp=[]
		et = time.time()	
		print '已输出到文件夹：'+fname,
		print '该数据集耗时：'+ str(et-st)+'  s'
	etime = time.time()	
	print '总共耗时：'+ str(etime-stime)+'  s'

if __name__ == '__main__':

    #~ if len(sys.argv ) > 0:
        #~ print """
        #~ [ ERROR ] useless argv
        #~ """
        #~ Usage()
	main()
