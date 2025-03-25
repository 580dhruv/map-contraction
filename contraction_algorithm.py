# importing necessary libraries
import random
# method to load the data from the given txt file                      # return the listed data
def load_data(file_name):
    adjacency_list = {}
    with open(file_name, 'r') as file:
        for line in file:
            values = list(map(int, line.strip().split()))
            node = values[0]  # First value is the node
            neighbors = values[1:]  # Remaining values are neighbors
            adjacency_list[node] = neighbors
    return adjacency_list

# method to separate the listed data into necessary adjacency list for Karger's algorithm(contraction algorithm)
def create_list(data):
    # initializing variables
    edges_list = []
    edge_vertice_dict = {}
    vertices_edge_dict = {}
    count = 1
    # adding vertices to vertices_list using list comprehension
    vertices_list = [row for row in data.keys()]
    # adding edges to edges_list corresponding edge with its incident vertex-pair to the edge-vertice dict.
    for vertice in vertices_list:
        for connected_vertice in data[vertice]:
            if vertice< connected_vertice:
                edges_list.append(count)                                    # appending the count which keeps count of the vertices added in
                edge_vertice_dict[count] = [vertice,connected_vertice]      # appending the vertice with its other connected vertices
                count+=1                                                    # incrementing count by 1
    # adding the vertice with its corresponding incident edges on itself(outgoing and incoming edges)
    for edge in edge_vertice_dict:
        for vertice in edge_vertice_dict[edge]:
            if vertice not in vertices_edge_dict:       # checking whether the vertice is not present in the vertice_edge_dict
                vertices_edge_dict[vertice] = [edge]        # creating its list of its incident edges on that vertice
            else:
                vertices_edge_dict[vertice].append(edge)    # assigning incident edges to it's corresponding vertice
    return vertices_list,edges_list,edge_vertice_dict,vertices_edge_dict
# method to contract the input graph till 2 vertices are left in the original
def contracting_graph(vertices_list,edges_list,edge_vertice_dict,vertices_edge_dict):
    # initializing variables
    selected_edge = []        # keeps track of the visited
    # iterating through the graph till 2 vertices are left in the input graph to get a unique cut
    while len(vertices_list)>2:                                              # continue if there are more than 2 vertices
        picked_edge = edges_list[random.randint(0,len(edges_list)-1)]          # pick a remaining edge (u,v) uniformly at random
        if picked_edge not in selected_edge:               # adding the choosen edge to the list so it doesnt get repeated.
            selected_edge.append(picked_edge)                                           # appending the randomly selected edge in the selected list
            selected_vertex_1, selected_vertex_2 = edge_vertice_dict[picked_edge]       # fetching the vertice pair which this edge connects to
            # merge the selected vertice-pair(u,v) into a single vertex
            vertices_list,edge_vertice_dict,vertices_edge_dict=merge_picked_vertices(picked_edge,selected_vertex_1,selected_vertex_2,edges_list,vertices_list,edge_vertice_dict,vertices_edge_dict)
            edges_list, edge_vertice_dict, vertices_edge_dict=remove_self_loops(edges_list,edge_vertice_dict,vertices_edge_dict)       # removing self-loops
    return len(edges_list),edges_list,edge_vertice_dict,vertices_list,vertices_edge_dict,selected_edge
# method which merges the (u,v) pair vertices to be one and arranging the edges between them and the vertices this pair is connected to
def merge_picked_vertices(picked_edge,selected_vertex_1,selected_vertex_2,edges_list,vertices_list,edge_vertice_dict,vertices_edge_dict):

    # assigning the min(index/numbered) and max(index/numbered) out of (u,v)
    minimum_indexed_vertice,maximum_indexed_vertice = min(selected_vertex_1,selected_vertex_2),max(selected_vertex_1,selected_vertex_2)
    # arranging the edges inside the pair (u,v) vertice and removing the which is picked randomly
    vertices_edge_dict[minimum_indexed_vertice] += [edge for edge in vertices_edge_dict[maximum_indexed_vertice] if ((not edge  in vertices_edge_dict[minimum_indexed_vertice]) and (not edge==picked_edge))]
    vertices_edge_dict[minimum_indexed_vertice].pop(vertices_edge_dict[minimum_indexed_vertice].index(picked_edge))
    # iterating through vertices and its corresponding edges dictionary
    for vertice in vertices_edge_dict:
        if picked_edge in vertices_edge_dict.values():      # validating whether picked edges is present in all the vertices corresponding edge list
            print('picked_edge :',picked_edge)
            print('vertices_edge_dict',vertices_edge_dict)
            # and if there removing it from its corresponding vertex's edge list
            vertices_edge_dict[vertice] = vertices_edge_dict[vertice].pop(vertices_edge_dict[vertice].index(picked_edge))
    # removing the maximum numbered/index vertice out of (u,v) pair as it is merged with the minimum numbered vertex
    vertices_list.remove(maximum_indexed_vertice)
    vertices_edge_dict.pop(maximum_indexed_vertice)
    # iterating through the edge and it's corresponding vertex pair as value
    for edge,vertice in edge_vertice_dict.items():
        if maximum_indexed_vertice in vertice:      # validating whether the maximum numbered/index vertex is present in the vertice list
            edge_vertice_dict[edge].append(minimum_indexed_vertice)     # creating a self loop on the minimum numbered/indexed vertex
            edge_vertice_dict[edge].remove(maximum_indexed_vertice)     # removing the maximum numbered/indexed vertex as it is merged
    # removing the picked edge on which (u,v) is merged on
    edges_list,edge_vertice_dict = remove_picked_edge(edges_list,edge_vertice_dict,picked_edge,selected_vertex_1,selected_vertex_2)
    return vertices_list,edge_vertice_dict,vertices_edge_dict
# method which removes the picked edge from the edge lists and edge_vertices dictionary passed ,as vertices (u,v) are merged on it
def remove_picked_edge(edges_list,edge_vertice_dict,picked_edge,selected_vertex_1,selected_vertex_2):
    edges_list.remove(picked_edge)      # removing picked edge from the edge list
    edge_vertice_dict.pop(picked_edge)  # removing picked edge from the edge and its corresponding vertices dictionary
    return edges_list,edge_vertice_dict
# method which removes the self loops
def remove_self_loops(edges_list,edge_vertice_dict,vertices_edge_dict):
    # iterating through edge and its corresponding vertices dictionary as list to remove unnecessary changes to the original one while iterating through
    for edge,vertice_pair in list(edge_vertice_dict.items()):
        if vertice_pair[0]==vertice_pair[1]:    # validating whether vertices are same in a certain edge's corresponding vertices list
            del edge_vertice_dict[edge]             # removing if present from the edge_vertice dictionary
            edges_list.remove(edge)                 # removing from the edges list
            if vertice_pair[0] in vertices_edge_dict.keys():    # validating whether that repeated vertex is in vertex and its corresponding dictionary
                vertices_edge_dict[vertice_pair[0]].pop(vertices_edge_dict[vertice_pair[0]].index(edge))    # remove if present
    return edges_list,edge_vertice_dict,vertices_edge_dict
# method which shows all the details while the process is working showing its changes through each iteration
def details(iteration,cut,vertices_list,edges_list,edge_vertice_dict,vertices_edge_dict,selected_edges):
    print('_'*100)
    print("Iteration :",iteration)
    print("Selected_edges :",selected_edges)
    print('Cut :',cut)
    print("edges_list :",edges_list)
    print("edge_vertice_dict :",edge_vertice_dict)
    print("vertices_list :", vertices_list)
    print("vertices_edge_dict :",vertices_edge_dict)
# method which shows all the stored history regarding the cuts made during the iterations
def show_history(min_cut_history):
    print("-"*1000)
    print("****HISTORY****")
    # iterating through the history of cuts
    for cut,history in min_cut_history.items():
        print("Cut :", cut, ":: History :", history)
# method which runs that contraction algorithm many times to differentiate to get a cut which uses minimum numbered edges to get it
def contraction_epochs(data,epochs = 1):
    # initializing variables
    min_cut_history = {}
    min_cut = len(data)
    # iterating through the epochs
    for iteration in range(epochs):
        print(iteration)
        vertices_list, edges_list, edge_vertice_dict, vertices_edge_dict = create_list(data)    # calling the create_list method
        # calling the contracting_graph method
        cut,edges_list,edge_vertice_dict,vertices_list,vertices_edge_dict,selected_edges = contracting_graph(vertices_list, edges_list, edge_vertice_dict, vertices_edge_dict)
        details(iteration,cut,vertices_list,edges_list,edge_vertice_dict,vertices_edge_dict,selected_edges)     # calling the details method
        if cut<min_cut:      # validating whether the cut found is minimum or not of all
            min_cut=cut         # assigning if it is minimum of all
        if not cut in min_cut_history:      # validating whether the cut found is not in history
            min_cut_history[cut] = [edges_list]     # storing the cut and its details if it is validated
        else:
            min_cut_history[cut] += [edges_list]    # adding new details to that certain cut
    show_history(min_cut_history)       # calling the show_history method
    return min_cut

# loading the data in the dock
data = load_data('adjacency_list.txt')
# calling the contraction epochs method
min_cut = contraction_epochs(data)
print("FINAL MIN-CUT :",min_cut)
