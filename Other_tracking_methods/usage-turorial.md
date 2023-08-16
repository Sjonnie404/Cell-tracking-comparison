# Written tutorial to replicate tracks in Trackmate and CellProfiler

We assume you have followed and successfully installed the programs, using the information on the main git readme.


## Trackmate
- Before running the plugin, the user should import the image sequence to Fiji. This can be achieved by selecting  `File → Import → Image Sequence...` and select the folder containing all (masked) frames. Leave all other parameters as is.
- Since our images are RGB (even though the masks are black and white), we have to convert them to greyscale. This can be achieved by `Image → Color → RGB to Luminance`. When this conversion is finished, a new window with a greyscale image sequence will appear.  The original image sequence can be closed, because we don't need it anymore. Make sure you select the greyscale image sequence again by clicking on it before proceeding to the next step.
1.  To start the tracking go to `Plugins → Tracking→ Trackmate`.
2.  A popup will appear, asking to swap Z and T, click `Yes`.  Next, the trackmate window will appear with the actual plugin. Only change parameters that are discussed, leave all else as is.
3. To actually swap Z and T, click `→Next`.
4.  Select `Mask detector` and click `→Next`.
5. Make sure `Simplify contours` is checked, and click `→Next`.
6. Wait for the detections to complete, and click `→Next`.
7. The next page will be "Initial thresholding", please make sure all spots are selected, and press `→Next`.
8. Wait for the 'set filters on spots' to finish and click `→Next`.
9. Then, select `Simple Lap tracker` from the dropdown menu, and click `→Next`.
10. Make sure to set the parameters as follows:
	- `Linking max distance` to 15.0 pixel
	- `Gap-closing max distance` to 30.0 pixel
	- `Gap-closing max frame gap` to 2
	- click `→Next`.
11. Wait for the tracking to complete, and click `→Next`.
12. On the 'Set filters on tracks' page, leave all as is, and click `→Next`.
13. The next page is the 'Display options' page, click the `Tracks` button.
14. This opens the new window 'Track tables', click the `Export to CSV` button.

Before we can use the tracks they need to be pre-processed.
From this CSV file, we extract multiple columns and rename these with new column headers:
- Frame -> tframe
- X (pixel) -> x
- Y (pixel) -> y
- Track ID -> track

- Next, x and y need to be rounded to full pixel values.
- Because the track IDs will be incoded into the later generated .TIFF files, we must change the Track ID starting index from 0 to 1.


## CellProfiler
In CellProfiler open the downloaded `Tracking_project.ccproj` file which can be found in the same directory as this tutorial.

1. Import the directoy with the (masked) frames from the desired video. NOTE: it is very important that the directory, containing the frames is uploaded (instead of only the frames).
- Do this:
	- dir/
		- frame000.png
		- frame001.png
		- etc. etc.
- Dont do this:
	- frame000.png
	- frame001.png
	- etc. etc.

2. Next, click the `Metadata` module in the left column, leave parameters as is, and click `Update`. Make sure that each framefile is assigned to it's unique 'FrameNumber', and that all frames in the 'Run' column have the same value.
3. Click on `ExportToSpreadsheet` in the left column and make sure to correctly specify the output directory
4. (Optional) Click on  `SaveImages` in the left column and make sure to check the checkbox left of it's text. Make sure to specify the correct output directory for the tracked images. (This is not used in the analysis, thus optional).
5
Before we can use the tracks they need to be pre-processed.
From the CSV file, we extract multiple columns and rename these with new column headers:
- ImageNumber -> tframe
- Location_Center_X -> x
- Location_Center_Y -> y
- TrackObjects_Label -> track

- Next, x and y need to be rounded to full pixel values.
- CellProfiler's starting index from the frames is 1, to make this uniform with the other methods the starting index should be changed to 0.



### Conclusion
When following these two tutorials, the same results can be generated as used in the paper.