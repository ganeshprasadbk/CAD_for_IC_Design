####################################################################################
#----------------------------------------------------------------------------------#
#         PYTHON IMPLEMENTATION OF MODIFIED HYPEREDGE-COARSENING ALGORITHM         #
#                                                               -GANESH PRASAD B K #
#                                                               (2018H1230151G)    #
#__________________________________________________________________________________#
#----------------------------------------------------------------------------------#
####################################################################################

def ModifiedHyperEdgeCoarsening_clustering(hypergraph_dict,node_delay_dict):
    'Function to perform Modified HyperEdge-Coarsening Clustering'
    import pprint

    nodes = list(set([x for y in hypergraph_dict.values() for x in y]))
    nodes.sort()

    def neighbours(x):
        'Function to find the neighbours of a node'    
        neighbour_list = []
        for i in hypergraph_dict.keys():
            if x in hypergraph_dict[i]:
                neighbour_list.append(hypergraph_dict[i])
        neighbour_list_flattened = list(set([x for y in neighbour_list for x in y])-set(x))
        neighbour_list_flattened.sort()
        return neighbour_list_flattened

    def weight(x,y):
        'Function to fnd the weight of the edges'    
        w = 0
        for i in hypergraph_dict.keys():
            if x in hypergraph_dict[i]:
                if y in hypergraph_dict[i]:
                    net = i
                    h = h_cal(net)
                    w = 1/(h - 1)
        return w

    def h_cal(net):
        'Function to calculate |h| value used in Weight calculation'    
        h = 0
        net_nodes = hypergraph_dict[net]
        for i in net_nodes:
            h = h + node_delay_dict[i]
        return h

    def list_flattener(list_x):
        'Function to flatten the list of lists'    
        flattened_list = [x for y in list_x for x in y]
        return flattened_list

    net_size_unsorted = {}
    for i in hypergraph_dict:
        net_size_unsorted[i] = h_cal(i)
    net_size = dict(sorted(net_size_unsorted.items(), key=lambda x: x[1]))

    marked_nodes = []
    cluster_dict = {}
    uncovered_nodes = []
    
    def cluster(x):
        'Function to form cluster'
        if x not in marked_nodes:
            cluster_list = []
            marked_nodes_temp = []
            neighbour_list = neighbours(x)
            neighbour_list_wo_marked_nodes = [y for y in neighbour_list if y not in marked_nodes]
            wt = 0
            for i in neighbour_list_wo_marked_nodes:
                wt_temp = weight(x,i)
                if(wt_temp>wt):
                    wt = wt_temp
                    cluster_list = [x,i]
                    marked_nodes_temp = [x,i]
        else:
            return
        if(cluster_list!=[]):
            cluster_dict.update({'cluster(%d)'%(len(cluster_dict)+1):cluster_list})
        else:
            return
        marked_nodes.extend(marked_nodes_temp)
        marked_nodes.sort()
        return cluster_list

    Final_cluster = {}
	
    def final_clustering(net):
        'Function to perform final clustering'
        node_list = hypergraph_dict[net]
        cluster_level = []
        for i in node_list:
            cluster_level.append(get_key_from_value(cluster_dict,i))
        final = list(set(list_flattener(cluster_level)))
        final.sort()
        if len(final)>1:
            Final_cluster.update({net:final})
        else:
            Final_cluster.update({net:None})
        return

    def get_key_from_value(dictionary,value):
        'Function to get key from value of a dictionary'
        key_list = []
        for i in dictionary.keys():
            value_list = dictionary[i]
            if value in value_list:
                key_list.append(i)
        return key_list


    def skip_net(net):
        a = hypergraph_dict.get(net)
        b = marked_nodes
        any_in = any(i in b for i in a)
        if any_in:
            return True
        else:
            return False
            
    for i in net_size:
        for j in hypergraph_dict[i]:
            if j not in marked_nodes:
                if skip_net(i):
                    uncovered_nodes.append(j)
                else:
                    cluster(j)
    uncovered_nodes_sorted = list(set(uncovered_nodes))
    uncovered_nodes_sorted.sort()

    for i in uncovered_nodes_sorted:
        cluster(i)
        
    updated_uncovered_nodes = list(set(uncovered_nodes_sorted)-set(marked_nodes))

    for i in updated_uncovered_nodes:
        cluster_dict.update({'cluster(%d)'%(len(cluster_dict)+1):[i]})

    for i in hypergraph_dict.keys():
            final_clustering(i)

    print('\nModified Hyperedge coarsening result:\n')
    pprint.pprint(cluster_dict)
    print('\nNetlist transformation based on HEC result.:\n')
    pprint.pprint(Final_cluster)

    return cluster_dict,Final_cluster


###Sample Test Case
##hg  = {'n1': ['a', 'c', 'e'],
##       'n2': ['b', 'c', 'd'],
##       'n3': ['c', 'e', 'f'],
##       'n4': ['d', 'f'],
##       'n5': ['e', 'g'],
##       'n6': ['f', 'g', 'h']}
##import pprint
##print('The hypergraph_dict entered by the user is')
##pprint.pprint(hg)                                                                  
##nod_delay = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}
##cl_dict,f_cl = ModifiedHyperEdgeCoarsening_clustering(hg,nod_delay)
##print('\nModified Hyperedge coarsening result:\n')
##pprint.pprint(cl_dict)
##print('\nNetlist transformation based on HEC result.:\n')
##pprint.pprint(f_cl)
