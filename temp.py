#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import gdal
from PIL import Image
import numpy as np
from methods_on_modis import *
import matplotlib.pyplot as plt

result = getRasters('data',['h26v05','h26v06','h25v05','h25v06'])

for i in result:
	print i



