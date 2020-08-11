#############################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------#
#                                   PYTHON IMPLEMENTATION OF EIG PARTITIONING ALGORITHM                                     #
#                                                                                                        -GANESH PRASAD B K #
#                                                                                                            (2018H1230151G)#
#___________________________________________________________________________________________________________________________#
#---------------------------------------------------------------------------------------------------------------------------#
#############################################################################################################################

def EIG_bipartitioning(nets_dict,acceptable_partition_size):
    'Function to perform EIG partitioning given the undirected graph'
    'It takes partition size constraint from the user'
    
    import numpy as np
    import networkx as nx
    import networkx.algorithms as nxalg
    from itertools import combinations
    import matplotlib.pyplot as plt
    import pprint
    from operator import itemgetter
    import warnings
    warnings.filterwarnings("ignore")
    
##    def warn(*args, **kwargs):
##        pass
##    import warnings
##    warnings.warn = warn
    
    def form_DiGraph_dict(nets_dict):
        nx_graph = nx.Graph()
        for i in nets_dict:
            edges = combinations(nets_dict[i],2)
            for each_edge in edges:
                nx_graph.add_edge(each_edge[0],each_edge[1])
        Graph_dict = nx.convert.to_dict_of_lists(nx_graph)
        nx.draw_networkx(nx_graph,pos=pos_maker(nx_graph))
        plt.show(block= False)
        return nx_graph,Graph_dict
  
    def letters_to_numbers_dict(letter_dict):
        'Function to perform conversion from lettered dictionary to number dictionary'
        'It just replaces the letters by a number corresponding to its position in the given dictionary'
        'This numbered dictionary is later useful in Adjacency matrix, Degree matrix & Laplacian matrix' 
        number_dict = {}
        num_list = list(enumerate(letter_dict))
        for i in letter_dict: 
            for k in num_list: 
                if i==k[1]:
                    number_dict[k[0]] = []
                    for j in letter_dict[i]:
                        for m in num_list:
                            if j==m[1]:
                                number_dict[k[0]].append(m[0])
        return number_dict

    def letters_to_numbers_dict_values(letter_dict):
        'Function to perform conversion from lettered dictionary to number dictionary'
        'Here only values (but not keys) are converted into numbers'
        'It just replaces the letters by a number corresponding to its position in the given dictionary'
        'This numbered dictionary is later useful in weight & cutsize calculation'
        number_dict_values = {}
        num_list = list(enumerate(uG_dict)) 
        for i in letter_dict:
            number_dict_values[i]=[]
        for i in letter_dict:
            for j in letter_dict[i]:
                for k in num_list:
                    if k[1]==j:
                        number_dict_values[i].append(k[0])
                        
            number_dict_values[i].sort()
        return number_dict_values

    def weight():
        'Function to calculate and assign weight for all the edges'
        for i in edge_list:
            wt = 0
            for j in nets_dict.values():
                if (set(i).issubset(j)):
                    wt = wt + 1/(len(j)-1)
            g.add_edge(i[0],i[1],weight=round(wt,2))
        return

    def weight_num():
        'Function to calculate and assign weight for all the edges'
        for i in edge_list_num:
            wt = 0
            for j in nets_num.values():
                if (set(i).issubset(j)):
                    wt = wt + 1/(len(j)-1)
            g_num.add_edge(i[0],i[1],weight=round(wt,2))
        return

    def adjacency_matrix():
        'Function to calculate Adjacency matrix'
        n = len(uG_num.keys())
        matrix = np.zeros((n, n))
        for i, j, k in list(g_num.edges(data='weight')):
            matrix[i][j] = k
            matrix[j][i] = k
        return matrix

    def degree_matrix():
        'Function to calculate Degree matrix'
        n = len(uG_num.keys())
        matrix = np.zeros((n, n))
        for i in nodes_num:
            matrix[i][i] = g_num.degree(i,'weight')
        return matrix

    def node_ordering():
        'Function to order nodes based on the eigen vector of the second smallest eigen value of the Laplacian matrix'
        temp_eigen_value,temp_eigen_vector = np.linalg.eig(Q)
        eigen_values = ['%.4f' % elem for elem in temp_eigen_value]
        scnd_smllst_egn_val_indx = eigen_values.index(sorted(eigen_values)[1])
        #print('The Second smallest Eigen Value is %s\n'%(sorted(eigen_values)[1]))
        eigen_vector = []
        for i in temp_eigen_vector:
            eigen_vector.append(round((i[scnd_smllst_egn_val_indx]),4))
        #print('and the coressponding Eigen Vector is %s\n'%eigen_vector)
        nodes_n_eigen_vector = dict(zip(nodes,eigen_vector))
        #print('The nodes are placed on the number line in the range [-1,1] '\
        #      '& their position on the number line is given by\n%s\n'%nodes_n_eigen_vector)
        node_ordering_temp = sorted(nodes_n_eigen_vector.items(), key=lambda kv: kv[1])
        node_ordering = tuple([x for x in node_ordering_temp for x in x[0]])
        return node_ordering

    def ratio_cut(partition_0,partition_1):
        'Function to calculate ratio cut'
        ratio = (nx.cut_size(g,partition_0,partition_1,'weight'))/(len(partition_0)*len(partition_1))
        return ratio

    def partitioning():
        'Function to perform partitioning'
        partition_list = []
        partition_show_case_list = []
        for i in range(1,len(Z)):
            Pa = []
            for j in range(i):
                Pa.append(Z[j])
                Pb = list(set(nodes)-set(Pa))
            cutsize = str(round(nx.cut_size(g,Pa,Pb,'weight'),4))
            cut_ratio = str(round(ratio_cut(Pa,Pb),5))
            partition_list.append([Pa,Pb,[cutsize],[cut_ratio]])
            partition_show_case_list.append([['P_A: %s'%Pa,'P_B: %s'%Pb,'Cutsize = %s'%cutsize,'Ratio cut = %s'%cut_ratio]])
        return partition_list,partition_show_case_list
       
    def balanced_partitioning():
        'Function to produce partition of equal size only if the number of nodes are even'
        length = len(uG_dict.keys())/2
        for i in partioning_info:
            if (len(i[0])==length):
                return i
            
    def final_partiotioning():
        'Function to perform final partioning based on user-input size constraint for partitions and minimum ratio cut'
        max_size = max([x for y in acceptable_partition_size for x in y])
        #print('max_size = %s'%max_size)
        partioning_info_copy=partioning_info.copy()
        for i in partioning_info_copy:
            if (len(i[0])>int(max_size) or len(i[1])>int(max_size)):
                partioning_info.remove(i)
        finalpartition = min_list_of_lists(partioning_info)
        return finalpartition


    def min_list_of_lists(outer_list):
        'Function to get list from the lists of list based on one particular element of a lis which will be minimum'
        inner_list_min_value_elements = []
        for i in outer_list:
            inner_list_min_value_elements.append(list(enumerate(i))[-1][1])
            #print(inner_list_min_value_elements)
        index =  min(enumerate(inner_list_min_value_elements), key=itemgetter(1))[0]
        #print(list(enumerate(inner_list_min_value_elements)))
        return outer_list[index]   


    def pos_maker(nx_graph):
        pos_dict = {}
        pos_list = list(nx_graph.nodes())
        pos_list.sort()
        for i in pos_list:
            k = pos_list.index(i)
            if (k<=len(pos_list)/4):
                y = k
                if (k%2==0): x = 0
                else: x = 1
            elif (k>len(pos_list)/4 and k<=len(pos_list)/2):
                y = k-len(pos_list)/4-1
                if (k%2==0): x = 2
                else: x = 3
            elif (k>len(pos_list)/2 and k<=len(pos_list)*3/4):
                y = k-len(pos_list)/2-1
                if (k%2==0): x = 4
                else: x = 5
            else:
                y = k-len(pos_list)*3/4-1
                if (k%2==0): x = 6
                else: x = 7
            pos_dict.update({i:(x,y)})
        #pprint.pprint(pos_dict)
        return pos_dict

    
    nx_Graph,uG_dict = form_DiGraph_dict(nets_dict)
    uG_num = letters_to_numbers_dict(uG_dict)
    #pprint.pprint(uG_num)
    #print()

    nets_num = letters_to_numbers_dict_values(nets_dict)

    nodes = list(uG_dict.keys())
    nodes_num = list(uG_num.keys())

    g = nx.Graph(uG_dict)
    edge_list = list(g.edges())
    g.add_edges_from(g.edges())
    clique_list = list(nx.find_cliques(g))
    #print(clique_list)
    #print()
    
    g_num = nx.Graph(uG_num)
    edge_list_num = list(g_num.edges())
    g_num.add_edges_from(g_num.edges())
    clique_list_num = list(nx.find_cliques(g_num))

    weight()
    #pprint.pprint(list(g.edges(data='weight')))
    weight_num()
    #pprint.pprint(list(g_num.edges(data='weight')))


    #print('\nThe undirected graph entered by the user is')
    #pprint.pprint(uG_dict)                                                                                                             #Prints undirected graph in the form of dictionary
    #print('\nThe hyperedges entered by the user is')
    #pprint.pprint(nets_dict)                                                                                                           #Prints undirected graph in the form of dictionary
    #print('\nThe ADJACENCY MATRIX(A) is, A = ')
    A = adjacency_matrix()
    #pprint.pprint(A)
    #print('\nThe DEGREE MATRIX(D) is, D = ')
    D = degree_matrix()
    #pprint.pprint(D)
    #print('\nThe LAPLACIAN MATRIX(Q=D-A) is, Q = ')
    Q = D - A
    #print(Q)
    #print()

    Z = node_ordering()
    #print('The ordered node-list for partitioning based on the above eigen vector is\n%s\n'%(Z,))

    print('Summary of EIG algorithm:')
    partioning_info,partioning_show_case_info = partitioning()
    print(*partioning_show_case_info,sep='\n')

    if (len(uG_dict.keys())%2)==0:
        balanced_partition = balanced_partitioning()
        print('\nThe perfectly balanced partitioning solution is :\n1st PARTITION = %s'\
          '\n2nd PARTITION = %s\nCutsize = %s\nRatio cut = %s'%(balanced_partition[0],\
                                                                balanced_partition[1],\
                                                                balanced_partition[2],\
                                                                balanced_partition[3]))

    print('\nThe acceptable partition size\\s as entered by the user is\\are %s'%acceptable_partition_size)
    final_partition = final_partiotioning()
    print('\nThe final partitioning solution considering both area '\
          'constraint and ratio cut is :\n1st PARTITION = %s'\
          '\n2nd PARTITION = %s\nCutsize = %s\nRatio cut = %s'%(final_partition[0],\
                                                                final_partition[1],\
                                                                final_partition[2],\
                                                                final_partition[3]))
    return balanced_partition, final_partition
    


