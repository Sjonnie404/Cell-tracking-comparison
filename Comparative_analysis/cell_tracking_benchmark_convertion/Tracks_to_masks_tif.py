# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import numpy as np
from pathlib import Path
import os
# import sys
from PIL import Image


# if len(sys.argv)==4:
#     filename = sys.argv[1].strip()
#     x_size = int(sys.argv[2])
#     y_size = int(sys.argv[3])
#     radius = 15
    
# else:
#     filename="arg_no_negativos.csv"
#     x_size = 1376
#     y_size = 1104
    




# dir = "./masks_saved-"+filename[0:-4]  
# command = "mkdir -p "+dir
# print(command)
# os.system(command)
   
def position2mask(filename,x_size,y_size,path,name):
    df = pd.read_csv(filename)
    # df.columns =  ["tframe","x","y","track"]
    
    
    for f,frame in df.groupby("tframe"):
        data = np.zeros((y_size,x_size),dtype=np.uint16)
        for i,ID in frame.groupby("track"):
            # print(ID)
            ID = ID
            x = int(ID["x"])
            y = int(ID["y"])
            miny = max(0,y-10)
            maxy = min(y_size,y+10)
            minx = max(0,x-10)
            maxx = min(x_size,x+10)
            if int(ID['track']) == 6:
                if f == 122:
                    print('Got here')
            # if int(ID['track']) == XX:
            #     if f == 21:
            #         print('Got here')
            data[miny:maxy,minx:maxx] = ID['track']
        img = Image.fromarray(data)

        new_name = name+str(f).zfill(3)+".tif"
        print(f'Finished:\t{new_name}')
        final_pos = Path(path / new_name)
        img.save(final_pos)






