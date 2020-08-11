

def L_Steiner_routing(node_dict):
    import networkx as nx
    import matplotlib.pyplot as plt
    import pprint
    import math
    import operator
    import random

    def join_nodes(list_1,list_2):
        temp_tree_dict = {}
        d = math.inf
        for i in list_1:
            for j in list_2:
                new_d = abs(node_dict[i][0]-node_dict[j][0])+abs(node_dict[i][1]-node_dict[j][1])
                if new_d<d:
                    d = new_d
                    temp_tree_dict.clear()
                    temp_tree_dict.update({(i,j):(d,-abs(node_dict[i][1]-node_dict[j][1]),-max(node_dict[i][0],node_dict[j][0]))})
                if new_d==d:
                    temp_tree_dict.update({(i,j):(d,-abs(node_dict[i][1]-node_dict[j][1]),-max(node_dict[i][0],node_dict[j][0]))})

        sorted_temp_tree_dict = dict(sorted(temp_tree_dict.items(), key=operator.itemgetter(1)))
        try:
            key = list(sorted_temp_tree_dict.keys())[0]
            value = sorted_temp_tree_dict[key]
            tree_dict.update({key:value})
            tree_nodes.append(list(sorted_temp_tree_dict.keys())[0][1])
            non_tree_nodes.remove(list(sorted_temp_tree_dict.keys())[0][1])
            nx_Graph.add_edge(key[0], key[1])
            nx_DiGraph.add_edge(key[0], key[1])
        except:
            None

    def level_sort(nxdigraph):
        level_dict = {}
        nx_dict = nx.to_dict_of_lists(nxdigraph)
        height = nx.dag_longest_path_length(nxdigraph)
        src_node = list(nx.topological_sort(nx_DiGraph))[0]
        for i in list(nxdigraph.nodes()):
            if nx_DiGraph.out_degree(i) != 0:
                l = list(nx.all_simple_paths(nxdigraph,src_node,i))
                level = len([item for sublist in l for item in sublist])
                level_dict.update({i:level})
        level_list = [i[0] for i in sorted(level_dict.items(), key = lambda x : x[1], reverse=True )]
        return level_list

    graph = dict.fromkeys(node_dict,[])
    nx_Graph = nx.Graph(graph)
    nx_DiGraph = nx.DiGraph(graph)
##    nx.draw_networkx(nx_Graph,pos=node_dict)
##    plt.show()
##    plt.show(block=False)
##    plt.pause(2)
##    plt.close()
    tree_dict = {}
    tree_nodes= []
    non_tree_nodes = list(node_dict.keys())
    root_node = random.choice(non_tree_nodes)
    non_tree_nodes.remove(root_node)
    tree_nodes.append(root_node)

    while non_tree_nodes != []:
        join_nodes(tree_nodes,non_tree_nodes)
        nx.draw_networkx(nx_DiGraph, pos=node_dict)
        plt.show(block=False)
        plt.pause(3)
        plt.close()
    nx.draw_networkx(nx_DiGraph, pos=node_dict)
    plt.show(block=False)
    rooted_tree_dict = nx.to_dict_of_lists(nx_DiGraph)
    bottom_up_traversal_list = level_sort(nx_DiGraph)
    return


###Sample input
##node_location_dict = {'a': (1,5),'b': (4,4),'c': (2,8),'d': (3,7),'e': (6,9),'f': (7,5),'g': (8,1),'h': (10,2),'i': (10,10)}
##L_Steiner_routing(node_location_dict)
