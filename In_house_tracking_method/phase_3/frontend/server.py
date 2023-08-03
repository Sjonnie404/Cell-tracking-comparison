import pandas.errors
from flask import Flask, send_from_directory, redirect, url_for, request
from os import listdir
from datetime import datetime
from pathlib import Path  # Using the pathlib library make for cross-platform compatible filepaths.
import shutil
import pandas as pd

from tracking import generate_graph, generate_track, generate_tracks
app = Flask(__name__)

# Predefined variables
SCORE_FUNC="squared"
MAX_SCORE=40*40
G = None
DATA = []
N_TRACKS = 0
# Extracts the current date and time from the user PC, and formats to string, e.g.: 11-Nov-h19-m57
TIMESTAMP = datetime.now().strftime("%d-%b-%Y-h%H-m%M")
AUTO_prev_session_check = True

# Predefined paths
DATA_FILE = "NED_tracks.csv"
WORK_DIR = Path.cwd()  # Gets 'frontend' dir as working directory
FRAMES_DIR = Path(WORK_DIR / '..' / 'example-data' / 'frames')
DETECTIONS_FILE = Path(WORK_DIR / '..' / 'example-data' / 'data' / DATA_FILE)
SESSION_FILE = Path(WORK_DIR / '..' / 'example-data' / 'data' /f'session_{TIMESTAMP}.csv')

# Backup datafile check
# Always making sure there's a backup of the original data file
ORIGINAL_DATA_FILE = list(Path(WORK_DIR / '..' / 'example-data' / 'data').glob('ORIG_*.csv'))
if len(ORIGINAL_DATA_FILE) > 1:
	print('>\tMultiple backup files detected, please fix manually.')
elif len(ORIGINAL_DATA_FILE) == 1:
	print('>\tBackup of datafile has already been created.')
elif len(ORIGINAL_DATA_FILE) < 1:
	shutil.copyfile(DETECTIONS_FILE, Path(WORK_DIR / '..' / 'example-data' / 'data' / f'ORIG_{DATA_FILE}'))
	print('>\tCreated backup of datafile.')

# Previous session check
if AUTO_prev_session_check:
	try:
		# Checks for multiple session files in the `data` folder
		session_files = list(Path(WORK_DIR / '..' / 'example-data' / 'data').glob('session*.csv'))
		if len(session_files) != 0:
			print('>\tPrevious session file detected, subtracting tracks from data file.')
			data_file = pd.read_csv(DETECTIONS_FILE)

			for i, session_file_path in enumerate(session_files):
				session_name = session_file_path.stem  # takes the filename from the path
				try:
					session_file = pd.read_csv(session_file_path, header=None)
				except pandas.errors.EmptyDataError:  # When session file is empty, remove to reduce file clutter
					session_file_path.unlink()
					print(f'>\tEmpty session file, removed {session_name}.')
					continue

				print(f'>\tPerforming track subtraction on {session_name}')
				print(f'>\tDF size before subtraction:\t{data_file.shape[0]}')
				# <-- Taken from R code
				session_file.columns = ['tframe', 'x', 'y', 'track_no']
				merged_df = pd.merge(data_file, session_file, on=["x", "y", "tframe"], how='outer')
				merged_df = merged_df[merged_df['track_no'].isnull()].drop('track_no', axis=1)
				# --> Taken from R code
				data_file = merged_df  # Need to reassign the same variable so all sessions are subtracted from the same file

				print(f'>\tDF size after subtraction:\t{data_file.shape[0]}')
				shutil.move(session_file_path, Path(WORK_DIR / '..' / 'example-data' / 'data' / 'previous_sessions' / f'{session_name}.csv'))

			data_file.to_csv(Path(WORK_DIR / '..' / 'example-data' / 'data' / DATA_FILE))
	except:  # Broad except to make sure the user can always use the flask application.
		print('>\tSomething went wrong with the automated track subtraction.')
		print('>!!!\tPlease note that previous tracks have NOT been subtracted.')
	print('\n\n')
else:
	print('>\tAutomatic previous session file check has been disabled.')

df = pd.read_csv(DETECTIONS_FILE)
for _, dft in df.groupby('tframe'):
	positions = []
	for _,row in dft.iterrows():
		positions.append((row['x'], row['y']))
	DATA.append(positions)
f = open(SESSION_FILE,"w")
f.write("")
f.close()


@app.route('/')
def index():
	return redirect('static/index.html')


@app.route('/detections/')
def detections():
	df = pd.read_csv(DETECTIONS_FILE)
	d = dict()
	for i,r in df.iterrows():
		i = int(r['tframe'])
		if i not in d:
			d[i]=[]
		d[i].append((int(r['y']),int(r['x'])))  # Only changes the view of the data, not the saved data itself
	return dict(detections=d)


@app.route('/frames/')
def frames():
	frames = [l for l in listdir( FRAMES_DIR ) if l.endswith(".jpg")]
	# sort the jpg file names by their names (as numbers) rather than lexicographically
	if not frames:	# If no images are found, check if there's .png images
		frames = [l for l in listdir( FRAMES_DIR ) if l.endswith(".png")]

	frames.sort(key = lambda x: int(x.split('.')[0]))
	return dict(frames=frames)

def safeindex(l,i):
	try:
		return l.index(i)
	except ValueError: 
		return -1

def track_to_posarray( trackp ):
	track = [-1] * len( DATA )
	for n in trackp:
		if G.nodes[n]["type"]=="D":
			track[G.nodes[n]["time_point"]] = G.nodes[n]["idx"]
	return track

def send_track():
	track = track_to_posarray( generate_track( G ) )
	return dict(track=track,
		npos=G.number_of_nodes()-2-2*(len(DATA)-1),
		nconn=G.number_of_edges()-2*(len(DATA)))


@app.route('/accept-track/', methods=['POST'])
def accept_track():
	global N_TRACKS
	N_TRACKS += 1
	track = track_to_posarray( generate_track( G ) )
	f = open(SESSION_FILE, "a")
	for i,p in enumerate(track):
		if p >= 0:
			# These have been swapped due to line 102 also swapping X & Y for better visualizations
			f.write(f"{i},{DATA[i][p][1]},{DATA[i][p][0]},{N_TRACKS}\n")
	f.close()
	generate_tracks( G, DATA, max_num=1, debug=False )
	return send_track()

@app.route('/delete-detection/', methods=['POST'])
def delete_detection():
	content = request.json
	t = content["frame"]
	i = content["index"]
	n = f"D_{t}_{i}"
	print( f"deleting detection {n}")
	G.remove_node( n )
	return send_track()

@app.route('/add-detection/', methods=['POST'])
def add_detection():
	print("add detection called")
	content = request.json
	t = content["frame"]
	new_detection = content["detection"]
	idx_new_det = content["detectionindex"]
	n =  f"D_{t}_{idx_new_det}"
	print( f"adding detection D_{t}_{idx_new_det}")
	G.add_node(n, x = new_detection[1], y=new_detection[0],  time_point = t, idx = idx_new_det, type = 'D')
	print(new_detection[1],new_detection[0])
	# add the new detection to the DATA subarray corresponding to the current frame
	DATA[t].append([new_detection[1], new_detection[0]])
	return ('', 204)

# push current segment(not the suggested one, accepted by pressing A, but the one with registered changes)
@app.route('/push-segment/', methods=['POST'])
def push_segment():
	content = request.json
	s = content["segment"]
	nodes_of_segment=[]
	print(s)
	#print(G.nodes)
	if len(s)>1:
		for i in range(len(s)-1):
			if s[i] == -1 : continue
			if s[i+1] == -1 : continue
			n1 = f"D_{i}_{s[i]}"
			n2 = f"D_{i+1}_{s[i+1]}"
			# add node names to list
			if n1 not in nodes_of_segment:
				nodes_of_segment.append(n1)
			if n2 not in nodes_of_segment:
				nodes_of_segment.append(n2)					
			#print( f"{n1},{n2} before" )
			print( list(G.successors( n1 )) )
			nb = [(n1,ss) for ss in G.successors(n1) if (G.nodes[ss]["type"] in ["D","X"])]
			G.remove_edges_from(nb)
			G.add_edge(n1, n2, weight = 0)
			print( "after" )
			print( list(G.successors( n1 )) )
	print(nodes_of_segment)		
	global N_TRACKS
	N_TRACKS += 1
	track = track_to_posarray(nodes_of_segment)
	print(track)
	f = open(SESSION_FILE, "a")
	for i,p in enumerate(track):
		if p >= 0:
			f.write(f"{i},{DATA[i][p][0]},{DATA[i][p][1]},{N_TRACKS}\n")
	f.close()
	generate_tracks( G, DATA, max_num=1, debug=False )
	return send_track()

@app.route('/delete-connection/', methods=['POST'])
def delete_connection():
	content = request.json
	t1 = content["frame1"]
	i1 = content["index1"]
	t2 = content["frame2"]
	i2 = content["index2"]
	n1 = f"D_{t1}_{i1}"
	n2 = f"D_{t2}_{i2}"
	print( f"deleting connection ({n1},{n2})")
	G.remove_edge( n1, n2 )
	return send_track()

@app.route('/accept-segment/', methods=['POST'])
def accept_segment():
	content = request.json
	s = content["segment"]
	print(G.nodes)
	if len(s)>1:
		for i in range(len(s)-1):
			if s[i] == -1 : continue
			if s[i+1] == -1 : continue
			n1 = f"D_{i}_{s[i]}"
			n2 = f"D_{i+1}_{s[i+1]}"
			print( f"{n1},{n2} before" )
			print( list(G.successors( n1 )) )
			nb = [(n1,ss) for ss in G.successors(n1) if (G.nodes[ss]["type"] in ["D","X"])]
			G.remove_edges_from(nb)
			G.add_edge(n1, n2, weight = 0)
			print( "after" )
			print( list(G.successors( n1 )) )
	return send_track()

@app.route('/track/')
def track0():
	return redirect(url_for('track',i=0))


def build_graph():
	global G, N_TRACKS
	#G = generate_graph(DATA, max_score=1000, score_func='squared')
	G = generate_graph(DATA, max_score=MAX_SCORE, score_func=SCORE_FUNC)
	N_TRACKS = 0


@app.route('/track/<int:i>')
def track(i=0):
	#if i > 0:
	#	generate_tracks(g, data, max_num=i, debug=False)
	#tracks = list(map( lambda l: safeindex(l,1), 
	#	generate_tracks(g, data, max_num=1, debug=False) ))
	if G is None or i>0:
		build_graph()
	generate_tracks( G, DATA, max_num=i, debug=False )
	return send_track()

@app.route('/frame/<path:path>', methods=['GET'])
def frame(path):
    return send_from_directory( FRAMES_DIR, path )
