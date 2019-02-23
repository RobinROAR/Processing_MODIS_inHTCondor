This program is designed for parallel processing Modis Time-Series Reflectance Data set in High-throughput Environment. The program will automatically wrap the raw MODIS dataset into abundant of subtasks and run them in the High-throughput computing system. The processing module including Format Conversion, Image Mosaic, Re-projection, and Clipping by Mask. The main script need the necessary dependencies including GDAL, numpy and matplotlib. The program can be used both in single PC and HTCondor clusters. 

We use this program to produce the dataset **MODIS remote sensing dataset for Qinghai Lake basin**. 


Dataset: http://www.csdata.org/p/160/ .
Publication: http://escj.cnic.cn/CN/article/downloadArticleFile.do?attachType=PDF&id=13140



## Dependencies ：
- python 2.7
- gdal-bin   >1.8
- python-gdal  > 1.8
- python-numpy
- HTCondor 


## Run： 

- main.py   Main program 主函数
- methods-on-modis.py   define functions 定义需要的处理模块
- viewTif.py   view tif


## Dirs(The Program will automatically detect and build the folder)：
- /out  output folder                   输出文件夹
- /data	put raw data in this folder     储存原始数据
- /shp	put x.shp file in this folder   储存程序需要的矢量数据
- /temp	store temporary files           储存程序产生的临时文件
