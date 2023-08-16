# Cell tracking comparison

### Background
Repository that holds all the information and scripts used for the results discussed in the paper: <br>*'Integrating Human Interaction For Improved Accuracy in Cell Tracking Methods'*

This paper is about the comparison of cell tracking software: Trackmate & Cellprofiler, against our own methods. Using our own videos.

#### Abstract:
Tracking cell microscopy video’s is a challenging and time consuming task. We present our own user-friendly method to perform (semi) automated cell tracking. With this tool the user is able to visualize and correct tracks instantly when needed. Furthermore, we also compare our method with free, most commonly utilized tracking software. Our results show that we are not only able to perform on par with the other methods, but can outperform these sophisticated methods with a simpler algorithm. Resulting in faster tracking, and real time calculation when manually screening the tracks.

### Tracks generation

#### in-house method
All scripts can be found in the `In_house_tracking_method` folder. Video files can be found [here](https://computational-immunology.org/hfsp/).
Tracking can only be performed on .png or .jpg images. .CZI files can be converted using the `phase_1_czi_jpg_and_raw_stardist.py` script. Automatic tracking can be performed using the `phase_2_do_tracking.ipynb` file.
Manually correcting the tracks can be done using the `phase_3` folder. Please put the `tracks.csv` file in the `data` folder, and paste the images into the `frames` folder for visual representation. Webapp can be started byrunning the run.sh file. A flask server will be started which can be accessed trough the internet browser, which can be accessed trough [here](http://127.0.0.1:5001) (localhost:5001).

The corrected tracks will be in the `data` folder. When the user accepts a track, it's automatically saved to a dedicated `sessions` file. Before the users starts the webapp, the newly created session files (that have been created after the previous restart) will be added to the corrected_track.csv file. With this the user is protected from unexpected server failure.

A tutorial for the track correction webapp, can be found [here](https://github.com/Sjonnie404/Cell-tracking-comparison/blob/main/In_house_tracking_method/correction_tutorial.md).

#### Trackmate
Trackmate is a plugin for the ImageJ application, which can be downloaded [here](https://imagej.net/software/fiji/downloads).
The installation steps for installing the Trackmate plugin can be found [here](https://imagej.net/plugins/trackmate/). 
A tutorial (including a list of used parameters) can  be found [here](https://github.com/Sjonnie404/Cell-tracking-comparison/blob/main/Other_tracking_methods/usage-tutorial.md)

#### CellProfiler
Cellprofiler can be downloaded from this [link](https://cellprofiler.org/releases).
The project file that includes the used parameters `Tracking_project.cpproj` can be found in the `Other_tracking_methods` folder

### Comparative analysis
Comparative analysis scripts can be found in the `Comparative_analysis`folder.

- The notebook `Tack_files_comparisons.ipynb` holds the code to generative the 'track index vs. track lengths' plots (like Figure 2 in the paper).
- The folder `cell_tracking_benchmark_convertion` holds the python files to clean the tracks (this should be ran prior to CTB conversion) and the conversion to CTB files format.
- The latter can be initiated by running `prepare_files.py` after specifying the tracking file path.
- After the files have been converted to the CTB format, the user should install the Cell Tracking Challenge plugin for Fii/ImageJ, an installation tutorial can be found [here](https://github.com/CellTrackingChallenge/fiji-plugins).
- With this plugin, the user is able to generate the used DET, TRA, CT & TF measurements used in the paper.

