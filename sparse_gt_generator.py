from pathlib import Path
from PIL import Image
import numpy as np
import csv
import re
import cv2
from matplotlib import pyplot as plt
import matplotlib
import random
%matplotlib inline
import os

def spilt_Channel(imge,sparse_percentage, fill_vaule):
    imgarray = np.array(imge, dtype="float32")
    y_lenght=len(imgarray)
    x_lenght=len(imgarray[0])
    image_size=y_lenght*x_lenght
    count=1
    mark = np.zeros((y_lenght, x_lenght), dtype=np.int)

    while (count/image_size)<sparse_percentage:
        y=random.randint(0, len(imgarray)-1)
        x=random.randint(0, len(imgarray[0])-1)
        if mark[y][x]== 0:
            #print("ssdsddsds")
            imgarray[y][x]=fill_vaule
            count=count+1
            mark[y][x]=1
        else:
            continue
    return imgarray

def get_DepthMap_path(path,result):
    for filename in os.listdir(path):
        file_path=path+filename
        if os.path.isdir(file_path):
            get_DepthMap_path(file_path+"/",result)
        else:
            file_type=os.path.splitext(file_path)[-1]
            if ".pfm"==file_type:
                png_path=os.path.splitext(file_path)[0]+".png"
                result.append((png_path))
    return result

def mkdir(path):
 
    folder = os.path.exists(path)
 
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")
 
    else:
        print("---  There is this folder!  ---")

def main():
    path="./"
    path_set=[]
    path_set=get_DepthMap_path(path,path_set)
    for item in path_set:
        png_path=item
        #print(calib_file_path)
        img=Image.open(png_path)
        img_array=np.array(img)
        
        plt.imshow(img)  
        plt.show()
        rate=0.1
        root_path=png_path.split(png_path.split('/')[-1])[0]
        
        for i in range(10):
            folder_path=root_path+str(rate)
            mkdir(folder_path)
            img_spilted=spilt_Channel(img_array,rate, 0)
            new_depthMap_name=png_path.split('/')[-1]
            plt.imshow(img_spilted)  
            plt.show()
            Temp_img=Image.fromarray(img_spilted)
            Temp_img = Temp_img.convert("L")
            new_depthMap_path=folder_path+"/"+new_depthMap_name
            Temp_img.save(new_depthMap_path)
            
            rate=rate+0.1
if __name__ == '__main__':
    main()
