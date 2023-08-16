#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:20:11 2023

@author: lucas
"""

import pandas as pd
# import glob
from matplotlib import image as img
from matplotlib import pyplot as plt
# import glob
import os
# from pathlib import Path
from PIL import Image
import numpy as np
# import cv2

def make_track_file(filepath,output):
    
    #filename = "arg_no_negativos.csv"
    
    df = pd.read_csv(filepath)
    # df.columns =  ["Frame","Position Y","Position X","ID"]
    tracks = df.groupby('track')
    CTB_df = pd.DataFrame({'track': pd.Series(dtype='str'),
                       'Start_frame': pd.Series(dtype='int'),
                       'End_frame': pd.Series(dtype='int'),
                       'Parent': pd.Series(dtype='int')})

    for track in tracks:
        track = track[1]  # Extrack actual df from tuple

        row = [{'track':list(set(track['track']))[0], 'Start_frame':min(track['tframe']), 'End_frame':max(track['tframe']), 'Parent':0}]
        CTB_df = CTB_df.append(row, ignore_index=True)
        CTB_df.to_csv(output, index=False, sep=' ',header=False)

