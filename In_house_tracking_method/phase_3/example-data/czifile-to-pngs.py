from czifile import CziFile# CZI is the file format designed by Zeiss, a microscope manufacturer
from PIL import Image
from csbdeep.utils import normalize

import numpy as np
import pandas as pd
#import cv2

import tensorflow as tf
from tensorflow import keras

from lxml import etree
import czifile

import time

czi_names = ["20221103 LifeAct nTnG neutrophils 6um"]
	#, 
        #    "20220128_LifeAct_nTnG_6um_straight_channels_rep1",
        #     "20220128_LifeAct_nTnG_6um_straight_channels_rep2"]

for name_of_rep_file in czi_names:
  czi_file = f"data/{name_of_rep_file}.czi"

  # load file and print shape
  img = CziFile(czi_file)
  print( img.shape )

  # extract time metadata
  czi_xml_str = img.metadata()
  czi_parsed = etree.fromstring(czi_xml_str)

  time_points = czi_parsed.xpath("//Time")
# print number of frames and time points
  print(img.shape[0])
# num of time points is num_frames+1, because the final point is also recorded (when the filming is stopped)
  len(time_points)

# check what the time info looks like
  print(time_points[0].text)

# extract the string representing the time point (between T and Z)
  a = time_points[0].text
  start = a.find('T')
  end = a.find('Z')
  print(a[start+1:end])

  num_frames = img.shape[0]
  time_array = []
  for i in range(0,num_frames):
    a = time_points[i].text
    start = a.find('T')
    end = a.find('Z')
    time_array.append(a[start+1:end])

  time_array

# remove the spurious dimension at the end 
  img = img.asarray()

# remove spurious dimensions and check that they have been removed
  img = img[:,:,:,:,0]
  print(img.shape)

# generate png's from the array of images
  for t in range( img.shape[0] ):
    frame = img[t,:,:,:]
    print( frame.shape )
    b = np.zeros( (img.shape[2],img.shape[3],3), "uint8" )
    print( b.shape )
    print( np.min( frame ), np.max( frame ) )
    b[:,:,0] = normalize(frame[1,:,:],pmin=3,pmax=99.8,clip=True)*255
    b[:,:,1] = normalize(frame[0,:,:],pmin=3,pmax=99.8,clip=True)*255
    im = Image.fromarray(b)
    path_png = f"frames/{t:03}.png" 
    im.save( path_png )
