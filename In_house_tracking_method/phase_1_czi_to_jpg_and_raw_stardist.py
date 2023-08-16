from czifile import CziFile  # CZI is the file format designed by Zeiss, a microscope manufacturer
import matplotlib.pyplot as plt  # standard python plotting library
from PIL import Image
import numpy as np
import pandas as pd
# import cv2
# import tensorflow as tf
# from tensorflow import keras
from stardist.models import StarDist2D  # This seems to require tensorflow
from stardist.plot import render_label
from csbdeep.utils import normalize


img = CziFile("czi_files/20220128 LifeAct nTnG 6um straight channels rep2.czi")
print(img.shape)

# remove the spurious dimension at the end 
img = img.asarray()

# remove spurious dimensions and check that they have been removed
img = img[:,:,:,:,0]
print(img.shape)

plt.figure(figsize=(20,20))
# channel 0, Actin stain, https://en.wikipedia.org/wiki/LifeAct_Dye
plt.imshow(img[0,0])

plt.figure(figsize=(20,20))
# channel 1, DNA stain for cell nucleus, https://en.wikipedia.org/wiki/Hoechst_stain
plt.imshow(img[0,1])

# generate stardist output

# prints a list of available models 
#StarDist2D.from_pretrained() 

# creates a pretrained model
model = StarDist2D.from_pretrained('2D_versatile_fluo') # could try "2D_paper_dsb2018" model as well

# predict centers of nuclei (which are captured in channel 1)
labels, coordinates = model.predict_instances(normalize(img[0,1]))
coordinates = coordinates["points"]

# plot labels of segmented cells
plt.figure(figsize=(20,20))
plt.imshow(labels)


for t in range( img.shape[0] ):
    frame = img[t,:,:,:]
    print( frame.shape )
    b = np.zeros( (img.shape[2],img.shape[3],3), "uint8" )
    print( b.shape )
    print( np.min( frame ), np.max( frame ) )
    b[:,:,0] = normalize(frame[1,:,:],pmin=3,pmax=99.8,clip=True)*255
    b[:,:,1] = normalize(frame[0,:,:],pmin=3,pmax=99.8,clip=True)*255
    im = Image.fromarray(b)
    im.save(f"frames/jpg_221129_LifeAct_nTnG_Dock8_KO_T_cells_6um/{t}.jpg" )
    
# number of frames
img.shape[0]

data = []
for t in range(img.shape[0]):
    labels, a = model.predict_instances(normalize(img[t,1]))  # Why did they choose to use python basic normalize, instead of the built in normalize?
    for x,y in a['points']:
        data.append({'x':x, 'y':y, 'tframe':t})

df = pd.DataFrame(data)
df.to_csv("stardist_output/raw_stardist_output/csv/raw_stardist_221129_LifeAct_nTnG_Dock8_KO_T_cells_6um.csv", index=False)