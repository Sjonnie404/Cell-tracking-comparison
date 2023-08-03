#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:22:15 2023

@author: lucas
"""


import pandas as pd
import numpy as np
import os
import sys
from PIL import Image


if len(sys.argv)==5:
    filename = sys.argv[1]
    output = sys.argv[2]
    x_size = int(sys.argv[3])
    y_size = int(sys.argv[4])
    
else:
    # filename="arg_20220107_LifeAct_nTnG_6um_straight_channels_1h.csv"
    filename="C:\\Users\\shane\\Documents\\Minor_internship_data\\viterbi-code\\testing\\track_projects\\tcells-6um-1\\tracks\\v1.5\\ARG_tracks.csv"
    output = "C:\\Users\\shane\\Documents\\Minor_internship_data\\viterbi-code\\testing\\track_projects\\tcells-6um-1\\tracks\\v1.5\\filtered_arg.csv"
    x_size = 1376
    y_size = 1104
    



df = pd.read_csv(filename)
df.columns =  ["Frame","Position Y","Position X","ID"] 




""" Comenzar desde ID=1. Necesario para pasos siguientes """

df["ID"] = df["ID"]+1



""" Swap x and y (CP and TM)"""

a = list(df["Position Y"])
df["Position Y"] = df["Position X"]
df["Position X"] = a



""" Delete out of boundaries """

df=df.loc[(df["Position X"]>=0) & (df["Position X"]<x_size) & (df["Position Y"]>=0) & (df["Position Y"]<y_size), :]



""" discontinued tracks """

to_correct = []

for t, track in df.groupby("ID"):
    if (max(track["Frame"])-min(track["Frame"]) >= track.shape[0]):
        to_correct.append(t)


for t in to_correct:
    track=df.loc[df["ID"]==t,:]
    sizes = []
    size=1
    for i,f in enumerate(list(track["Frame"])[0:-1]):
        if list(track["Frame"])[i+1]-f==1:
            size+=1
        else:
            sizes.append(size)
            size = 1
    sizes.append(size)
    
    # print(sizes)
    pos_longest = sizes.index(max(sizes))
    ini_longest = 0
    for sub_len in sizes[0:pos_longest]:
        ini_longest += sub_len
    # print(ini_longest)
    
    
    """ By now only deletes all disconected sub_tracks except le longest"""
    indx = track.index
    indexes_bad_1 = list(indx[0:ini_longest+1])
    indexes_bad_2 = list(indx[ini_longest+max(sizes):])
    
    df = df.drop(indexes_bad_1)
    df = df.drop(indexes_bad_2)
    
df.to_csv(output,header=False,index=False)
    
    


    
