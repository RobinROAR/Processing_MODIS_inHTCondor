#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pdb

def readFile(path):
	pdb.set_trace()
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
		


readFile('temp')
str = 'out/HDF4_EOS:EOS_GRID:"data/MCD12Q1/MCD12Q1.A2012001.h26v05.051.2014288202641.hdf":MOD12Q1:Land_Cover_Type_1'
str = str.split('"')
name = str[1][13:29]
print name