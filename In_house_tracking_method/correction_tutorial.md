

# Track correction Webapp tutorial

### Background
Repository that holds all the information and scripts used for the results discussed in the paper: <br> *'Integrating Human Interaction For Improved Accuracy in Cell Tracking Methods'*

This paper is about the comparison of cell tracking software: Trackmate & Cellprofiler, against our own methods. Using our own videos.

#### Startup

Before starting the webapp, users needs to provide data.
- Frames of the video should be saved to `example-data/frames/`
- Positions file of the video should be saved to `example-data/data/`
- When data is loaded, user should make sure required python packages (requirements.txt) are installed. (running python in a virtual environment is highly advised). 
- After successfully loading python and datafiles, the server can be started by running `frontend/run.sh`

#### How to use the webapp
The blue squares represent frames of the video and change dynamically with the loaded video. These squared can be clicked to jump to a specific frame. The user can also use the arrow keys to move a single frame left or right. 
Below the squares are the buttons; ‘accept’, to accept the currently selected track and save it to the output file (key-shortcut ‘a’) , ‘delete detection’, to delete currently selected detection (yellow outlined circle, key-shortcut ‘d’) and ‘delete connection’,  to delete the edge between the currently selected detection (yellow outline) and the next detection (key-shortcut ‘c’). 
User can also create new detections by holding the ‘shift’ key and clicking on the frame (no on screen button shown). Next to the button, information about the graph and currently selected detection can be found. Big, outlined, white circles represent all detections in the frame (that have not been accepted yet). 
Yellow outline represents currently selected detection and small, white, filled circles, linked with a white edge represent future detections of the currently selected track. Only the currently  
selected track is displayed for clarity.