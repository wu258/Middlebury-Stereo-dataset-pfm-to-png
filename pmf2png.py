from pathlib import Path
from PIL import Image
import numpy as np
import csv
import re
import cv2
from matplotlib import pyplot as plt
import matplotlib
%matplotlib inline
import os
def get_pfms_path(path,result):
    
    for filename in os.listdir(path):
        file_path=path+filename
        if os.path.isdir(file_path):
            get_pfms_path(file_path+"/",result)
        else:
            file_type=os.path.splitext(file_path)[-1]
            if ".pfm"==file_type:
                object_type=file_path.split('/')[-2]
                #change the path by your own structure
                calib_file_path="MiddEval3-data-F//MiddEval3-data-F//MiddEval3//trainingF//"+object_type+"//calib.txt"
                result.append((file_path,calib_file_path))
    return result
def read_calib(calib_file_path):
    with open(calib_file_path, 'r') as calib_file:
        calib = {}
        csv_reader = csv.reader(calib_file, delimiter='=')
        for attr, value in csv_reader:
            calib.setdefault(attr, value)

    return calib

def read_pfm(pfm_file_path):
    with open(pfm_file_path, 'rb') as pfm_file:
        header = pfm_file.readline().decode().rstrip()
        channels = 3 if header == 'PF' else 1

        dim_match = re.match(r'^(\d+)\s(\d+)\s$', pfm_file.readline().decode('utf-8'))
        if dim_match:
            width, height = map(int, dim_match.groups())
        else:
            raise Exception("Malformed PFM header.")

        scale = float(pfm_file.readline().decode().rstrip())
        if scale < 0:
            endian = '<' # littel endian
            scale = -scale
        else:
            endian = '>' # big endian

        dispariy = np.fromfile(pfm_file, endian + 'f')
    #
    img = np.reshape(dispariy, newshape=(height, width, channels))
    img = np.flipud(img).astype('uint8')
    #
    #show(img, "disparity")

    return dispariy, [(height, width, channels), scale]


def create_depth_map(pfm_file_path, calib=None):

    dispariy, [shape,scale] = read_pfm(pfm_file_path)

    if calib is None:
        raise Exception("Loss calibration information.")
    else:
        fx = float(calib['cam0'].split(' ')[0].lstrip('['))
        base_line = float(calib['baseline'])
        doffs = float(calib['doffs'])

        # scale factor is used here
        depth_map = fx*base_line / (dispariy / scale + doffs)
        depth_map = np.reshape(depth_map, newshape=shape)
        depth_map = np.flipud(depth_map).astype('uint8')

        return depth_map

def show(img,path):
    if img is None:
        raise Exception("Can't display an empty image.")
    else:
        temp_img=np.reshape(img, (len(img), len(img[0])))
        plt.imshow(temp_img)  
        plt.show() 
        file_type=os.path.splitext(path)[0]
        print(file_type)
        Temp_img=Image.fromarray(temp_img)
        Temp_img.save(file_type+".png")


def main():
    path="./" #the path of input folder
    path_set=[]
    path_set=get_pfms_path(path,path_set)
    for item in path_set:
        disp_left,calib_file_path=item
        print(calib_file_path)
        print(disp_left)

        # calibration information
        calib = read_calib(calib_file_path)
        # create depth map
        depth_map_left = create_depth_map(disp_left, calib)
        #print(depth_map_left)
        show(depth_map_left,disp_left)

if __name__ == '__main__':
    main()
