#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import gdal
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def readFile(path):
	for root ,dirs,files in os.walk(path):
		#只显示二级目录
		if files ==[]:
			continue
		else:
			temp= []
			#连接文件名
			for name in files:
				str =  os.path.join(root,name)
				temp.append(str)
		return temp
		


r = readFile('out')
s= ''
for i in r:
	if 'Land_Cover_Type_1.tif' in i:
		s = i
		break
ds = gdal.Open(s)
ds1 = Image.open(s)

A = np.array(ds.ReadAsArray())
B = np.array(ds1)

print A.dtype
print B.dtype



#~ fig = plt.figure(frameon = False)    #生成画布
#~ ax = fig.add_subplot(111)             #增加子图
#~ ax.imshow(A, interpolation='nearest', cmap=plt.cm.gist_earth)    #子图上显示数据
#~ plt.savefig('./test1.JPEG',dpi = 80)
#~ ax.set_xticks([])                            #去除坐标轴
#~ ax.set_yticks([])
#~ plt.savefig('./test2.JPEG',dpi = 210)




