#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np

a = np.array([[1.1,1.2,1.3,1.4,1.5],[2.1,2.2,2.3,2.4,2.5],[3.1,3.2,3.3,3.4,3.5],[4.1,4.2,4.3,4.4,4.5]])
temp = np.array([a,a+1,a+2])
print temp.shape
print temp
zero = np.zeros([temp.shape[1],temp.shape[2],temp.shape[0]])
print zero.shape

print '//////////////////////////////'
print zero[:,:,0].shape
print zero[:,:,0]
print temp[0,:,:]
print temp[0,:,:].shape

zero[:,:,0] = temp[0,:,:]
zero[:,:,1] = temp[1,:,:]
zero[:,:,2] = temp[2,:,:]
print zero

