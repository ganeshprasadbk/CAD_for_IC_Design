#############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------#
#                                       PYTHON IMPLEMENTATION OF KERNIGHAN-LIN ALGORITHM                                    #
#                                                                                                        -GANESH PRASAD B K #
#                                                                                                            (2018H1230151G)#
#___________________________________________________________________________________________________________________________#
#---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################
###                                                 PACKAGES USED IN THE PROGRAM                                          ###
#############################################################################################################################
#from numpy import *                                                                
#from collections import *
import pprint

#############################################################################################################################
#############################################################################################################################

def KerninghanLin_Bipartitioning(Graph_dict,net_dict,partition_A,partition_B,no_of_pass):
    
    import random as rnd
    import networkx as nx
    import numpy
    import collections
    import networkx.algorithms as nxalg
    import networkx.algorithms.community  as com
    import matplotlib.pyplot as plt

    import operator
    from operator import itemgetter
    import pprint
    import warnings
    warnings.filterwarnings("ignore")
    
    'Function to perform partitioning using Kernighan & Lin Algorithm'
    'Graph_dict is the dictionary where parent nodes and children nodes form key-value pairs'
    'Partition_A & Partition_B are the initial partitions. If not provided then the function will choose'
    'random partitions by itself'
    'no_of_pass is the total number of times KL algorithm need to be run'

    if partition_A == None:
        partition_A = rnd.sample(Graph_dict.keys(),int(len(Graph_dict.keys())/2))
        partition_B = list(set(Graph_dict.keys())-set(partition_A))

    def Kerninghan_Lin_single_pass(Graph_dict,net_dict,partition_A,partition_B):
        'Function to perform KL algorithm partitioning for single pass'
        
        g = nx.Graph(Graph_dict)                                                                                            #Feeding dictionary of graph to form a undirected graph                                                       	                            #converting dictionary of DAG into network graph using networkx library

        def edge_weight():
            'Function to calculate edge weight and to add it as edge attributes'
            
            edge_list = list(g.edges())
            for i in edge_list:
                wt = 0
                for j in net_dict.values():
                    if set(list(i)).issubset(j):
                        wt = wt + 1/(len(j)-1)
                g.add_edge(i[0], i[1], weight=wt)
            return 

        edge_weight()                                                                                                       #Calling edge_weight() to create edges with weights and then add it to 'g' as edge attributes
        #print(list(g.edges(data='weight')))

        def cost(x):
            'Function to calculate Cost of each node'
            'This function first detects to which partition (A or B) the given node belongs to'
            'and then calculates its external cost and internal cost'
            'Formula: Total cost = External cost - Internal cost'
            
            if x in partition_A:
                int_list = partition_A
                ext_list = partition_B
            else:
                int_list = partition_B
                ext_list = partition_A
                
            int_cost_x = 0
            ext_cost_x = 0
            mod_int_list = list((set([m for n in list(g.edges(x)) for m in n])-set(x))&set(int_list))
            mod_ext_list = list(set([m for n in list(g.edges(x)) for m in n])&set(ext_list))
            
            for i in mod_int_list:
                int_cost_x = int_cost_x + g[x][i].get('weight')
                
            
            for i in mod_ext_list:
                ext_cost_x = ext_cost_x + g[x][i].get('weight')
                
            cost_x = ext_cost_x - int_cost_x
            
            return cost_x

        def gain(x,y):
            'Function to calculate Gain for a pair of nodes(x,y)'
            'This function makes use of cost() function'
            
            if (set([x,y]).issubset(set(partition_A)) | set([x,y]).issubset(set(partition_B))):
                #print(x,y,partition_A,partition_B)
                return
            elif (x in locked_nodes or y in locked_nodes):
                return
            else:
                if (x,y) in g.edges():
                    c = g[x][y].get('weight')                                                                               #If there exist an edge between x & y then c = edge weight of edge between x and y 
                else:
                    c = 0                                                                                                   #else c = 0
                gain = cost(x) + cost(y) - 2*c
                return {(x,y):gain}

        def swap(x,y):
            'Function to perform swapping of nodes between partitions'
            'once the node pair with maximum gain is found out'
            
            if x in partition_A:
                partition_A.insert(partition_A.index(x),y)
                partition_A.remove(x)
                partition_B.insert(partition_B.index(y),x)
                partition_B.remove(y)
            else:
                partition_A.insert(partition_A.index(y),x)
                partition_A.remove(y)
                partition_B.insert(partition_B.index(x),y)
                partition_B.remove(x)
            #cut_size_list.append([partition_A,partition_B,(nx.cut_size(g,partition_A,partition_B,weight='weight'))])
            return Gain_dict.clear()                                                                                        #Clearing the Gain_dict once the swapping is done

        def min_list_of_lists(outer_list):
            inner_list_min_value_elements = []
            for i in outer_list:
                inner_list_min_value_elements.append(list(enumerate(i))[-1][1])
                #print(inner_list_min_value_elements)
            index =  min(enumerate(inner_list_min_value_elements), key=itemgetter(1))[0]
            #print(index)
            return outer_list[index]

        Gain_dict = {}                                                                                                      #Initializing a Dictionary to store gain where its keys are node pairs and its values are corresponding gain
        locked_nodes = []                                                                                                   #List to store locked nodes. These nodes are not considered while calculating maximum gain before swapping
        swap_count = 1
        cut_size_list = [[partition_A,partition_B,'initial partition',(nx.cut_size(g,partition_A,partition_B,weight='weight'))]]                             #Dictionary to store Partitions as keys and its cut size as its values
        
        while set(Graph_dict.keys())!=set(locked_nodes):                                                                    #Looping till all the nodes get locked
            for i in partition_A:
                for j in partition_B:
                    #print('i,j = %s %s' %(i,j))
                    gain_temp = gain(i,j)
                    #print(gain_temp)
                    if gain_temp != None:
                        Gain_dict.update(gain_temp)
            print('Gain for Swap %d ='%swap_count)
            pprint.pprint(Gain_dict)
            print('')
            max_Gain_pair = max(Gain_dict.items(), key=operator.itemgetter(1))[0]
            #print(max_Gain_pair)
            swap(max_Gain_pair[0],max_Gain_pair[1])
            locked_nodes.extend([max_Gain_pair[0],max_Gain_pair[1]])
            #print('locked_nodes = %s'%locked_nodes)
            cut_size_list.append([partition_A,partition_B,max_Gain_pair,(nx.cut_size(g,partition_A,partition_B,weight='weight'))])
            #print('----%s'%cut_size_list)
            swap_count = swap_count + 1
            #for i in cut_size_list:
                #print(i)

##        for i in cut_size_list:
##            print(i)
##        print(cut_size_list)

        nx.draw_networkx(g)                                                         	                                    #Plotting a pictorial graph for user verification
        plt.show(block=False)								    	                                    #Displays DAG entered by the user

        return min_list_of_lists(cut_size_list)

    for i in range(no_of_pass):                                                                                             #Running KL algorithm for 'no_of+pass' times as input by the user
        print('-----------------------------Pass no %d Starts from here---------------------------------------' %(i+1))
        KL_output = Kerninghan_Lin_single_pass(uG,nets,partition_A,partition_B)
        print('KL output = %s'%KL_output)
        print('Partition_A = %s'%KL_output[0])
        print('partition_B = %s'%KL_output[1])
        print('Gain = %s'%KL_output[3])
        print('-----------------------------Pass no %d Ends here----------------------------------------------' %(i+1))
    return
#############################################################################################################################
###                                                PROGRAM BEGIN FROM HERE                                                  #
#############################################################################################################################

uG = {'a':['e','c'],'b':['c','d'],'c':['e','f','d'],'d':['f'],'e':['f','g'],'f':['g','h'],'g':['h'],'h':[]}

nets = {'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['d', 'f'],'n5': ['e', 'g'],'n6': ['f', 'g', 'h']}


##partition_0 = ['a','b','d','e']
##partition_1 = ['c','f','g','h']
##passes = 1
##
##print('\nThe uG entered by the user is')
##pprint.pprint(uG)                                                                                                           #Prints undirected graph in the form of dictionary
##print('\nThe netlist entered by the user is')
##pprint.pprint(nets)                                                                                                         #Prints nets & nodes in the form of dictionary
##print()
##print('1st partition is %s '%partition_0)
##print('2nd partition is %s '%partition_1)
##print('The KL algorithm will run for %d times'%passes)

#KerninghanLin_Bipartitioning(uG,nets,partition_0,partition_1,passes)

