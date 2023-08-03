#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:40:47 2023

@author: lucas
"""





from pathlib import Path
import pandas as pd
import numpy as np
import os
import sys


from Tracks_to_masks_tif import position2mask
from tracks_to_format import make_track_file

WORKDIR = Path.cwd()
WORKDIR = Path(WORKDIR / '..')
CUR_PROJECT = 'tcells-30um-1'
TRACK_VERSION = 'v2.1'
SOFTWARE = ['in-house', 'Trackmate', 'CellProfiler', 'ground-truth']  # TODO: Could possible be looped when using all software versions
SOFTWARE = SOFTWARE[0]

SAFE_FILE = True

df = pd.DataFrame()
# Note: Path is fixed for WIP project directory format, can be changed
# Pathlib module is used to designated paths OS independent.
if SOFTWARE == 'in-house':
    # df = pd.read_csv(Path(WORKDIR / 'testing' / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'NED_tracks.csv'))
    filepath_res = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'NED_NHI_cleaned_tracks.csv')
    CTB_dir = 'CTB_GT_IH'
elif SOFTWARE == 'Trackmate':
    # df = pd.read_csv(Path(WORKDIR / 'testing' / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'TM_ARTIF_tracks.csv'))
    filepath_res = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'TM_ARTIF_cleaned_tracks.csv')
    CTB_dir = 'CTB_GT_TM'
elif SOFTWARE == 'CellProfiler':
    # df = pd.read_csv(Path(WORKDIR / 'testing' / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'CP_ARTIF_tracks.csv'))
    filepath_res = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'CP_ARTIF_cleaned_tracks.csv')
    CTB_dir = 'CTB_GT_CP'
elif SOFTWARE == 'ground-truth':
    filepath_res = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'NED_cleaned_tracks.csv')
    CTB_dir = 'CTB_GT_GT'

filepath_gt = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION / 'NED_cleaned_tracks.csv')


print(df)

x_size = 1376
y_size = 1104

work_dir = Path(WORKDIR / 'track_projects' / CUR_PROJECT / 'tracks' / TRACK_VERSION)

# dir_res = "./03_RES/"
# dir_gt = "./03_GT/TRA/"

Path(work_dir / CTB_dir / "01_RES").mkdir(parents=True, exist_ok=True)
Path(work_dir / CTB_dir / "01_GT" / "TRA").mkdir(parents=True, exist_ok=True)
dir_res = Path(work_dir / CTB_dir / "01_RES")
dir_gt = Path(work_dir / CTB_dir / "01_GT" / "TRA")

name_res = "mask"
name_gt = "man_track"


# os.makedirs(dir_res,exist_ok=True)
# os.mkdir("01_GT")
# os.makedirs(dir_gt,exist_ok=True)


#  Create all the .tif files needed
position2mask(filepath_gt, x_size, y_size, dir_gt, name_gt)
position2mask(filepath_res, x_size, y_size, dir_res, name_res)


""" create"""
gt_tracks = os.path.join(dir_gt, "man_track.txt")
res_tracks = os.path.join(dir_res, "res_track.txt")

print('>\t Generating ground truth track files...')
make_track_file(filepath_gt,gt_tracks)
print('>\t Generating results track files...')
make_track_file(filepath_res,res_tracks)
print('>\t Finished generating track files!')
