#############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------#
#                                   PYTHON IMPLEMENTATION OF FBB PARTITIONING ALGORITHM                                     #
#                                                                                                        -GANESH PRASAD B K #
#                                                                                                            (2018H1230151G)#
#___________________________________________________________________________________________________________________________#
#---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################
###                                                 PACKAGES USED IN THE PROGRAM                                          ###
#############################################################################################################################
import numpy as np
import networkx as nx
import networkx.algorithms as nxalg
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import preflow_push
import pprint
from operator import itemgetter
import matplotlib.pyplot as plt
import itertools
#############################################################################################################################
#############################################################################################################################


#############################################################################################################################
###                                                PROGRAM BEGIN FROM HERE                                                  #
#############################################################################################################################
"""
no_of_nodes = int(input('Enter the total number of nodes in the undirected graph: '))          	                            #prompting user to input total number of nodes in undirected graph

print(' ')                                                                  	                                            #New line

DAG = {}                                                                    	                                            #initializing DAG as dictionary where keys are Parent nodes and its values are coressponding children

for i in range(no_of_nodes):                                                 	                                            #looping to take parent & children nodes of undirected graph from user
    Parent_node_Children_node = input('enter the parent node first & '\
                                'then its children: ').split()
    DAG[Parent_node_Children_node[0]] = Parent_node_Children_node[1:]
print(' ')

no_of_nets = int(input('Enter the total number of nets in the undirected graph: '))
print(' ')                                                                  	                                            #New line

nets = {}                                                                    	                                            #initializing DAG as dictionary where keys are Parent nodes and its values are coressponding children

for i in range(no_of_nets):                                                 	                                            #looping to take parent & children nodes of undirected graph from user
    nets_n_nodes = input('enter the name of the net first & '\
                                'then nodes connected by it: ').split()
    nets[nets_n_nodes[0]] = nets_n_nodes[1:]


"""

#Sample Input
#to run the program with the following inputs comment all the lines above except packages and uncomment DAG & nets

DAG  =  {'a': ['f', 'd'],                                                                                                   #To use Sample input, uncomment ths section and comment out above section from 'Label'
         'b': ['d', 'e', 'g'],
         'c': ['e'],
         'd': ['f', 'g'],
         'e': ['g', 'i'],
         'f': ['h'],
         'g': ['h', 'i'],
         'h': [],
         'i': []}

nets =  {'n1': ['a', 'd', 'f'],
         'n2': ['b', 'd', 'e', 'g'],
         'n3': ['c', 'e'],
         'n4': ['d', 'f', 'g'],
         'n5': ['e', 'g', 'i'],
         'n6': ['f', 'h'],
         'n7': ['g', 'h', 'i']}

g = nx.DiGraph(DAG)

print('The graph entered by the user is')
pprint.pprint(DAG)
print()
print('The net list entered by the user is')
pprint.pprint(nets)
print()

def node_list_generation():
    'Function to generate nodes from net_list'
    
    temp_node_list = []
    for i in nets.keys():
        temp_node_list.extend(nets[i])
    temp_node_list = list(dict.fromkeys(temp_node_list))
    temp_node_list.sort()
    return temp_node_list

def partition_sizing():
    'Function to decide partition sizing'
    
    if((len(node_list))%2==0):
        source_part_size = len(node_list)/2
        sink_part_size = len(node_list)/2
    else:
        source_part_size = (len(node_list)+1)/2
        sink_part_size = (len(node_list)-1)/2
    return source_part_size,sink_part_size

def net_based_flow_network(nets_dict):
    'Function to convert net list into net based flow graph'
    
    inverse = {}
    inverse_sorted = {}
    for key in nets_dict:                   # Go through the list that is saved in the dict:
        for item in nets_dict[key]:         # Check if in the inverted dict the key exists
            if item not in inverse:         # If not create a new list
                inverse[item] = [key] 
            else: 
                inverse[item].append(key)
    for key, value in sorted(inverse.items()):
        inverse_sorted[key]=value
    inverse_sorted.update(nets_dict.copy())
    return inverse_sorted

def primary_nodes():
    'Function to find Primary input & output nodes'
    
    pi_nodes = []
    po_nodes = []
    for i in nt_bsd_flw_ntwrk.keys():
        if g.in_degree(i)==0:
            pi_nodes.append(i)
        if g.out_degree(i)==0:
            po_nodes.append(i)            
    return pi_nodes,po_nodes

def choose_source_sink_nodes():
    'Function to choose one of the primary input nodes and one of the primary output nodes'
    
    pi_node = 'a'
    po_node = 'i'
    return pi_node,po_node

def cut_net(nxgraph):
    'Function to find cut net'
    
    nxgraph_copy = nxgraph.copy()
    plt.show()
    cut_net_list=[]
    nxgraph_nets = list(net_extraction_from_net_node_list(nxgraph_copy.nodes()))
    r = 0
    while cut_net_list==[]:
        'looping till we get cut nets'
        cut_net_list.clear()
        r = r + 1
        #print('r = %s'%r)
        node_name_tup = list(itertools.combinations(nxgraph_nets, r))
        node_name_list = [list(elem) for elem in node_name_tup]
        #print('node_name_list = %s'%node_name_list)
        for i in node_name_list:
            for j in i:
                nxgraph_copy.remove_node(j)
            if 's' not in nx.ancestors(nxgraph_copy,'t'):
                #print('s not in ancestors of t')
                print('Cut net = %s'%i)
                cut_net_list.extend(i)
                temp_partition = list(nx.connected_components(nxgraph_copy.to_undirected()))
                if(nx.number_connected_components(nxgraph_copy.to_undirected())==2):
                    part_0 = node_extraction_from_net_node_list(list(temp_partition[0]))
                    part_1 = node_extraction_from_net_node_list(list(temp_partition[1]))
                else:
                    part_0 = node_extraction_from_net_node_list(list(temp_partition[0])+list(temp_partition[-1]))
                    part_1 = node_extraction_from_net_node_list(list(temp_partition[1]))
                #print(nx.number_connected_components(nxgraph_copy.to_undirected()))
                return cut_net_list,part_0,part_1
            nxgraph_copy = nxgraph.copy()
        cut_net_list.clear()
    
def node_extraction_from_net_node_list(NET_node_LIST):
    'Function to extract only nodes from net_node_list'
    
    NODE_LIST = NET_node_LIST.copy()
    for i in nets.keys():
        if i in NET_node_LIST:
            NODE_LIST.remove(i)
    NODE_LIST.sort()
    return NODE_LIST

def net_extraction_from_net_node_list(net_NODE_LIST):
    'Function to extract only nets from net_node_list'

    NET_LIST = []
    for i in nets.keys():
        if i in net_NODE_LIST:
            NET_LIST.append(i)
    NET_LIST.sort()
    return NET_LIST

def update_dict(dictionary,src,tar):
    'Function to update dictionary by collapsing those nodes merged into "source_partition" into "s" and those nodes merged into "sink_partition" into "t"'
    
    updated_dict = dictionary.copy()
    for i in updated_dict.keys():
        if (src in updated_dict[i]):
            if ('s' not in updated_dict[i]):
                updated_dict[i].append('s')
            updated_dict[i].remove(src)
        if (tar in updated_dict[i]):
            if ('t' not in updated_dict[i]):
                updated_dict[i].append('t')
            updated_dict[i].remove(tar)
    if src in updated_dict.keys():
        updated_dict['s'] = updated_dict[src].copy()
        del updated_dict[src]
    if tar in updated_dict.keys():
        updated_dict['t'] = updated_dict[tar].copy()
        del updated_dict[tar]
    return updated_dict

def merging_node_selection(CUTNETlist):
    'Function to choose which node to be merged and to what it should be marged'
    'It is decided based on the size of souce and sink partition'
    
    merger_selection = []
    for i in CUTNETlist:
        merger_selection.extend(nets[i])
        #print('merger_selection = %s'%merger_selection)
    for i in merger_selection:
        if ((i in s) or (i in t)):
            merger_selection.remove[i]
    merger_selection = list(dict.fromkeys(merger_selection))
    merger_selection.sort()
    if len(source_partition)<len(sink_partition):
        print('merger_selection = %s'%merger_selection)
        print('sink_partition = %s'%sink_partition)
        print()
        node_to_be_merged = list(set(merger_selection).intersection(set(sink_partition)))
        #src_node = node_to_be_merged[0]
    else:
        node_to_be_merged = list(set(merger_selection).intersection(set(source_partition)))
        #tar_node = node_to_be_merged[0]
    node_to_be_merged.sort()
    return node_to_be_merged[0]


node_list = node_list_generation()
nt_bsd_flw_ntwrk = net_based_flow_network(nets)
dG = nx.DiGraph(nt_bsd_flw_ntwrk)
uG = nx.Graph(nt_bsd_flw_ntwrk)
pos ={'s':[-1,4] ,'a': [0,4],'b': [0,2],'c': [0,0],'d': [2,3],'e': [3,1],'f': [4,4],'g': [5,2],'h': [6,3],'i': [6,1],'n1': [1,4],'n2': [1,2],'n3': [1,0],'n4': [3,3],'n5': [4,1],'n6': [5,4],'n7': [6,2], 't':[8,2]}
primary_input_nodes,primary_output_nodes = primary_nodes()
src_node,tar_node = choose_source_sink_nodes()
source_partition_size,sink_partition_size = partition_sizing()
source_partition = []
sink_partition = []
s=[]
t=[]
latest_dictionary = nt_bsd_flw_ntwrk.copy()

while ((len(source_partition)+len(s)-1)<source_partition_size or (len(sink_partition)+len(t)-1)<source_partition_size):
    #print(src_node,tar_node)
    print()
    if src_node not in s:
        s.append(src_node)
        print('s=%s'%s)
    if tar_node not in t:
        t.append(tar_node)
        print('t=%s'%t)
    latest_dictionary = update_dict(latest_dictionary,src_node,tar_node)
    latest_uG = nx.Graph(latest_dictionary)
    latest_dG = nx.DiGraph(latest_dictionary)
    nx.draw_networkx(latest_uG,pos=pos)
    plt.show()
    cutnet, part0, part1 = cut_net(latest_dG)
    max_flow_value = len(cutnet)
    print('max_flow_value = %s'%max_flow_value)
    print()
    if 's' in part0:
        source_partition = part0.copy()
        sink_partition = part1.copy()
    else:
        source_partition = part1.copy()
        sink_partition = part0.copy()
    #print('source_partition = %s'%source_partition)
    #print('sink_partition = %s'%sink_partition)
    node_selection = merging_node_selection(cutnet)
    if len(source_partition)<len(sink_partition):
        src_node = node_selection
    else:
        tar_node = node_selection
    s_part = (list((set(source_partition)|set(s))-set('s')))
    s_part.sort()
    t_part = (list((set(sink_partition)|set(t))-set('t')))
    t_part.sort()
    print('The source partition is %s '%s_part)
    print('The sink partition is %s '%t_part)

    #break























