
def FlowMap_clustering(nets_dict,pin_constraint=3):
    import networkx as nx
    import matplotlib.pyplot as plt
    import operator
    import pprint
    import random

    def form_DiGraph_dict(nets_dict):
        DiGraph_dict = {}
        for i in nets_dict:
            DiGraph_dict.update({nets_dict[i][0]:nets_dict[i][1:]})
        nxDiGraph = nx.DiGraph(DiGraph_dict)
        return DiGraph_dict,nxDiGraph

    def form_PI(nx_DiGraph):
        'Function to form a list of primary input nodes'
        pi = []
        for i in nx_DiGraph.nodes():
            if nx_DiGraph.in_degree(i)==0:
                pi.append(i)
        pi.sort()
        return pi

    def form_PO(nx_DiGraph):
        'Function to form a list of primary output nodes'
        po = []
        for i in nx_DiGraph.nodes():
            if nx_DiGraph.out_degree(i)==0:
                po.append(i)
        po.sort()
        return po

    def cluster(nx_DiGraph,x):
        p = 0
        if (x in primary_input_nodes):
            p = 0
            return
        else:
            ancestors = nx.ancestors(nx_DiGraph,x)
            #print('ancestors = %s' %ancestors)
            ancestors_wo_PI = [x for x in ancestors if x not in  primary_input_nodes]
            #print('ancestors_wo_PI = %s' %ancestors_wo_PI)
            if(ancestors_wo_PI==[]):
                p = p + 1
                #print('p = %s' %p)
                Xv = [x]
                #print('Xv = %s'%Xv)
                label_dict.update({x:p})
            else:
                predecessors = list(nx.DiGraph.predecessors(nx_DiGraph,x))
                #print('predecessors = %s' %predecessors)
                p = int(highest_label_predecessor(predecessors))
                #print('p = %d' %p)
                q = cluster_with_same_p(nx_DiGraph,x,p)
                #print('q = %s'%q)
                cluster_in = [x for x in cluster_input(nx_DiGraph,q) if x not in q]
                #print('cluster_input = %s' %set(cluster_input))

                if(len(cluster_in)<=pin_constraint):
                    p = p
                    #print('p = %s' %p)
                    Xv = q
                    #print('Xv = %s'%Xv)
                else:
                    p = p + 1
                    #print('p = %s' %p)
                    Xv = [x]
                    #print('Xv = %s'%Xv)
                label_dict.update({x:p})
            return {x:Xv}

    def highest_label_predecessor(list_x):
        label_list = []
        for i in list_x:
            #print('i = %s' %i)
            label_list.append(label_dict.get(i))
        highest_label = max(label_list)
        #print('label_list = %s' %label_list)
        #print('highest_label = %s' %highest_label)
        return highest_label

    def cluster_with_same_p(nx_DiGraph,x,p):
        collapsed_cluster = []
        for i in nx.ancestors(nx_DiGraph,x):
            if (label_dict.get(i)==p):
                collapsed_cluster.append(i)
        collapsed_cluster = collapsed_cluster + [x]
        #print('collapsed_cluster = %s'%collapsed_cluster)
        return collapsed_cluster

    def cluster_input(nx_DiGraph,x):
        if type(x)!= list:
            cluster = cluster_dict[x]
        else:
            cluster = x
        clusterinput_temp = []
        for i in cluster:
            clusterinput_temp.extend(nx_DiGraph.predecessors(i))
        clusterinput_temp = list(dict.fromkeys(clusterinput_temp))
        clusterinput = [i for i in clusterinput_temp if i not in cluster]
        return clusterinput
    
    def sorting_list_from_dict(lis,dictionary):                                 	#Sub-routine to sort a list based on the 'key-value' pairs in dictionary
        new_dict = {}
        sorted_list = []
        for i in lis:                                                           	#looping through each element of list
            if i in dictionary:
                new_dict[i] =  dictionary[i]
        sorted_dict = \
            sorted(new_dict.items(), key=lambda i:i[1], reverse=True)           	#returns a sorted tuple containing keys and values
        for i in sorted_dict:                                                   	#extracting sorted keys as elements of lists
            sorted_list.append(i[0])
        return sorted_list

    def pos_maker(nx_graph):
        pos_dict = {}
        for i in nx_graph.nodes():
            k = list(nx_graph.nodes()).index(i)
            if (k<=len(list(nx_graph.nodes()))/4):
                y = k
                if (k%2==0): x = 0
                else: x = 1
            elif (k>len(list(nx_graph.nodes()))/4 and k<=len(list(nx_graph.nodes()))/2):
                y = k-len(list(nx_graph.nodes()))/4-1
                if (k%2==0): x = 2
                else: x = 3
            elif (k>len(list(nx_graph.nodes()))/2 and k<=len(list(nx_graph.nodes()))*3/4):
                y = k-len(list(nx_graph.nodes()))/2-1
                if (k%2==0): x = 4
                else: x = 5
            else:
                y = k-len(list(nx_graph.nodes()))*3/4-1
                if (k%2==0): x = 6
                else: x = 7
            pos_dict.update({i:(x,y)})
        #pprint.pprint(pos_dict)
        return pos_dict

    def mapping():
        L = form_PO(nx_DAG)
        J = form_PI(nx_DAG)
        s = []
        while L!=[]:
            s.append(L[0])
            item_2b_remvd_L = L[0]
            L.remove(L[0])
            cluster_input_wo_pi_nodes = [i for i in cluster_input(nx_DAG,item_2b_remvd_L) if i in J]
            if cluster_input_wo_pi_nodes==[]:
                L.extend(cluster_input(nx_DAG,item_2b_remvd_L))
            L = list(dict.fromkeys(L))
            s = list(dict.fromkeys(s))
            L.sort()
            s.sort()
        return s

    def merge_dicts(*dicts):
        d = {}
        for dict in dicts:
            for key in dict:
                try:
                    d[key].append(dict[key])
                except KeyError:
                    d[key] = [dict[key]]
        return d

    def get_values_for_list_from_dict(list_x,dict_x):
        dict_y = {}
        for i in list_x:
            k = dict_x.get(i)
            dict_y.update({i:k})
        return dict_y
    
    DAG,nx_DAG = form_DiGraph_dict(nets_dict)
    primary_input_nodes = form_PI(nx_DAG)
    #print(primary_input_nodes)
    primary_output_nodes = form_PO(nx_DAG)
    #print(primary_output_nodes)
    t = list(nx.topological_sort(nx_DAG))
    t.sort()
    #print(t)
    T = [i for i in t if i not in primary_input_nodes]
    #print(T)

    label_dict = {}
    for i in t:
        label_dict[i]= int('0')
        
    cluster_dict = {}
    for i in T:
        cluster_dict.update(cluster(nx_DAG,i))
        cluster_dict[i].sort()

    S = mapping()
    
    label_dict_wo_pi_nodes = label_dict.copy()
    for i in primary_input_nodes:
       del label_dict_wo_pi_nodes[i]
       
    label_n_cluster = merge_dicts(label_dict_wo_pi_nodes,cluster_dict)
    LUTs = get_values_for_list_from_dict(S,cluster_dict)
    max_delay = max(list(label_dict.values()))
    nx.draw_networkx(nx_DAG,pos=pos_maker(nx_DAG))
    plt.show(block = False)
    #plt.pause(5)
    #plt.close()

    print('The maximum delay is %s which is also the highest label value'%max_delay)
    print('\nLabel and Cluster information : ')
    pprint.pprint(label_n_cluster)
    print('\nLUTs are')
    pprint.pprint(LUTs)
    return max_delay,label_n_cluster,LUTs
