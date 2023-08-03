import pandas as pd
import numpy as np
import sys
first_inFile = sys.argv[1]
second_inFile = sys.argv[2]
outFile = sys.argv[3]

first_track_file = pd.read_csv(first_inFile, header=None)
# extract max track from first file to add to track ids of second_file
max_track_first_file = np.max(first_track_file.iloc[:,-1:])
second_track_file = pd.read_csv(second_inFile, header=None)

# add max track num from first file to second file track column
second_track_file.iloc[:,-1] = second_track_file.iloc[:,-1] + int(max_track_first_file)
# merge first and second trackfile
print(first_track_file.shape[0])

# print(first_track_file)
# print('-'*80)
# print(second_track_file)
# exit()

print(second_track_file.shape[0])
new_file = pd.concat([first_track_file, second_track_file])
print(new_file.shape[0])
# save merdges dfs as csv
print(new_file)
# exit()
new_file.to_csv(path_or_buf=outFile, sep=',', na_rep='', header=False, index=False)
