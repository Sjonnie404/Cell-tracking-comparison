import networkx as nx
import math

# a basic score function to be used when generating edges
def calculate_score(x1,y1,x2,y2,score):
    if score == 'linear':
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    elif score == 'squared':
        return (x1-x2)**2 + (y1-y2)**2
    elif score == 'constant':
        return 1
    else:
        return None   

# this function generates a graph, where nodes correspond to detections in frames (time points)
def generate_graph(points, max_score, score_func):
    # this is the number of frames (time points)
    t_max = len(points)
    # if the points list is empty, return an empty list
    if t_max == 0:
        return []
    # if max_score is 0, then an empty list is returned
    if max_score == 0:
        return []
    # if an invalid value is assigned to score_func, then an empty list is returned
    if score_func not in ['linear', 'squared']:
        return []
    # declare a directed graph
    G = nx.DiGraph()  
    # add start and end nodes
    G.add_node('S', type = 'S')
    G.add_node('T', type = 'T')

    # iterate over frames(time points) and detections contained in those and generate nodes
    for t, pt in enumerate(points):
        # generate the 'not-yet-present'- nodes (last one is Y_t_max-2, hence the if-statement needed)
        if t < t_max - 1:
            G.add_node(f"Y_{t}", time_point = t, type = 'Y')

        # generate the 'migrated-out-of-frame-or-dead'-nodes (first one is X1, X0 doesn't exist, as we dont take cells which were dead at the start of detection)
        if t > 0:
            G.add_node(f"X_{t}", time_point = t, type = 'X')

        # add the detection nodes contained in frame t
        for i, pti in enumerate(pt):
            G.add_node(f"D_{t}_{i}", time_point = t, idx = i, type = 'D')

    # add edges
    # add edges between the start node and the nodes in the first (in Python 0th) frame
    for i, _ in enumerate(points[0]):
        G.add_edge("S", f"D_{0}_{i}", weight=max_score)

    # add edge from S to Y0 (for the case where no entering into a frame is allowed - otherwise an edge from S to all Yn's would be added)
    # weight = max_score+1, so that 'priority' is given to existing detections
    G.add_edge("S", f"Y_{0}", weight=max_score+1)

    # add edges between nodes in the last frame and the end node
    for j, _ in enumerate(points[-1]):
        G.add_edge(f"D_{t_max-1}_{j}", "T", weight = max_score)    
    
    # add node from last X-node to T
    G.add_edge(f"X_{t_max-1}", "T", weight = max_score)    

    # add edges between Ds, Ys and Xs
    for t in range(t_max-1):
        for i in range(len(points[t])):
            # add edges between D_t_i's and D_t+1_j's (detections in two consecutive frames)
            for j in range(len(points[t+1])):
                # calculate distance between nodes and only assign edge if score <= max_score
                # coordinates of D_t_i
                x1 = points[t][i][0]
                y1 = points[t][i][1]
                # coordinates of D_t+1_j
                x2 = points[t+1][j][0]
                y2 = points[t+1][j][1]
                # calculate score, using the score function
                score = calculate_score(x1, y1, x2, y2, score_func)
                # add edge between D_t_i and D_t+1_j
                # check for existence of D nodes necessary, as we use the initial detection list to calculate edges between nodes,
                # even if nodes have been deleted when shortest path is found
                if score <= max_score and f"D_{t}_{i}" in G.nodes() and f"D_{t+1}_{j}" in G.nodes() :
                    G.add_edge(f"D_{t}_{i}", f"D_{t+1}_{j}", weight = score)

            # add edges between D_t's and X_t+1's, with weight = max_score+1
            G.add_edge(f"D_{t}_{i}", f"X_{t+1}", weight = max_score+1)

        for k in range(len(points[t+1])):
            # add edge between Yt and D_t+1's, with weight = max_score+1
            G.add_edge(f"Y_{t}", f"D_{t+1}_{k}", weight = max_score+1)

            # add edges between X_t's and D_t+1's, thus allowing the skipping of a frame and going back into a following frame
            #G.add_edge(f"X_{t}", f"D_{t+1}_{k}", weight = max_score+1)


        # add edges between Y's, with weight = max_score+2, so that the D nodes are considered 'more favourable'
        # if-statement necessary as we dont have a node Y_t_max-1
        if t < t_max-2:
            G.add_edge(f"Y_{t}", f"Y_{t+1}", weight = max_score+2)  

        # add edges between X's, with weight = max_score + 2 ('encouraging' the generation of tracks which go back from X to D??)
        # or should it be just a max_score? How to decide on an adequate value?
        
        if t > 0:
            G.add_edge(f"X_{t}", f"X_{t+1}", weight = max_score)
 
    return G

def generate_track(graph):
    shortest_path = None
    try:
        shortest_path = nx.shortest_path(graph, 'S', 'T', 'weight')
    except nx.exception.NetworkXNoPath:
        pass
    if all(graph.nodes[n]['type'] != 'D' for n in shortest_path[1:-1]):
        shortest_path = None
    if shortest_path is not None:
        return shortest_path[1:-1]
    else:
        return None

# TO DO: reconsider how to approach this
def generate_tracks(graph, detections, max_num=math.inf, debug = False):
    if graph == nx.null_graph:
        return []
    elif not('S' in graph.nodes()) or not('T' in graph.nodes()):    
        return []
    else:
        tracks = []
        for d in detections:
            tracks.append([None]*len(d))
        current_track = 1   
    # iterate while there are still D nodes in the list of nodes
    # check if the graph has D nodes - if not, return an empty list
        if len([n for n in graph.nodes.data('type') if n[1] == 'D']) == 0:
            return []
    # else generate shortest_paths until the shortest path doesn't contain any D nodes
        else:
            # initialize first shortest path (which is guaranteed to contain a D, as getting to a D node is less expensive than Y's and X's)
            while current_track <= max_num:
                path = generate_track(graph)
                if path is None:
                    break
                if debug:
                    print(path)
                for p in path:
                    if graph.nodes[p]['type'] == 'D':
                        t = graph.nodes[p]["time_point"]
                        i = graph.nodes[p]["idx"]
                        tracks[t][i] = current_track
                current_track = current_track+1
                graph.remove_nodes_from([n for n in path if graph.nodes[n]['type'] == 'D'])
            return tracks

#x = [[(0,0),(0,1)], [(1,0), (3,5)]]
#g = generate_graph(x, max_score=2, score_func='linear')
#print(g.nodes['X_1']['type'])
#print([n for n in list(g.nodes()) if g.nodes[n]['type'] == 'D'])
#g.remove_nodes_from([n for n in g.nodes if g.nodes[n]['type'] == 'D'])
#print(g.nodes)
#for n in g.nodes():
# print(g.nodes[n]['type'])
#print(nx.shortest_path(g, 'S', 'T'))
#t = generate_tracks(g, x)
#print(t)

       
# Qs: 
# 1. What should the weight function be?
# 2. Should max_score be a compulsory parameter? If the default is None,
#    then what weight should be given to the edge (Y_t, Y_t+1)
# 3. What does it mean for a set of tracks to be complete? If detections could be used multiple times,
#    how does the algorithm stop? If the algorithm punishes multiple uses of a detection, what is a good value for the 'punishment'?
# 4. Should the weights from Y_t to Y_t+1 be a lot harsher if a cell is unlikely to appear in the middle of an image
#    for the first time? How would the weights be defined? Perhaps an include_in_frame_migration parameter? What if its value is false? 

# the algorithm would stop when it becomes too expensive to add a new track (and only a track of Yt's is added)
# add a class for the score function
# contract graphs
# take some actual data
# add X nodes !!!! -> for tuesday
# rewrite score function as a class?

# Qs for Tuesday 5.07

# 1. Should the weights between X's be 0? Otherwise a cell is punished for disappearing?
# 2. Should we allow X nodes to be connected back to D nodes? - no, at least according to paper
