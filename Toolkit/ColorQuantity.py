#!/usr/bin/env python
# -*- coding:utf-8 -*-
###############################################################################
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# Author : Robin   <zrb915@live.com> tif_array.
###############################################################################
# changes  20151021
# this script used to realize the function of color quantization


try:
    from osgeo import gdal
except ImportError:
    import gdal

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
import methods_on_tif
from time import time

def Usage():
    print("""
    $ colorquantization.py  input_raster n_colors
    """)
    sys.exit(1)

def recreate_image(codebook, labels, w, h):
    """Recreate the (compressed) image from the code book & labels"""
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image

def count_color(input_array):
	res = []
	for i in input_array:
		temp = i[0]*1000+i[1]*10000+i[2]*100
		res.append(temp)
	print len(res)
	print len(set(res))


def main(input_raster,n_colors):
	tif_array = methods_on_tif.read_tif_as_array(input_raster)
	#Convert to floats instead of the default 8 bits integer coding. Dividing by
	# 255 is important so that plt.imshow behaves works well on float data (need to
	# be in the range [0-1]
	tif_array = np.array(tif_array, dtype=np.float64) / 255

	# Load Image and transform to a 2D numpy array.
	w, h, d = original_shape = tuple(tif_array.shape)
	print w,h
	assert d == 3
	image_array = np.reshape(tif_array, (w * h, d))
	
	#count_color(image_array)

	print("Fitting model on a small sub-sample of the data")
	t0 = time()
	image_array_sample = shuffle(image_array, random_state=0)[:1000]
	print image_array_sample.shape
	
	kmeans = MiniBatchKMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
	print("done in %0.3fs." % (time() - t0))
	print kmeans.cluster_centers_.shape

	# Get labels for all points
	print("Predicting color indices on the full image (k-means)")
	t0 = time()
	labels = kmeans.predict(image_array)
	print("done in %0.3fs." % (time() - t0))


	#~ codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
	#~ print("Predicting color indices on the full image (random)")
	#~ t0 = time()
	#~ #为全图划分分类，计算一组数据到一组坐标点中最近的一个点。
	#~ labels_random = pairwise_distances_argmin(codebook_random,
											  #~ image_array,
											  #~ axis=0)
											  
	
	#~ print("done in %0.3fs." % (time() - t0))
	
	#~ # Display all results, alongside original image
	plt.figure(1)
	plt.clf()
	ax = plt.axes([0, 0, 1, 1])
	plt.axis('off')
	plt.title('Original image data')
	plt.imshow(tif_array)
	plt.savefig("origin.jpeg")
	
	plt.figure(2)
	plt.clf()
	ax = plt.axes([0, 0, 1, 1])
	plt.axis('off')
	plt.title('Quantized image (8 colors, K-Means)')
	plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))
	plt.savefig("64.jpeg")
	
	#~ plt.figure(3)
	#~ plt.clf()
	#~ ax = plt.axes([0, 0, 1, 1])
	#~ plt.axis('off')
	#~ plt.title('Quantized image (64 colors, Random)')
	#~ plt.imshow(recreate_image(codebook_random, labels_random, w, h))
	plt.show()

	

if __name__ == '__main__':

    #~ if len( sys.argv ) < 2:
        #~ print """
        #~ [ ERROR ] you must supply at least two arguments:
        #~ 1) the band number to retrieve and 2) input raster
        #~ """
        #~ Usage()

    #~ main( sys.argv[1], sys.argv[2] )
	main('/home/robin/DataBackup/Landsatqhh.tif',16)