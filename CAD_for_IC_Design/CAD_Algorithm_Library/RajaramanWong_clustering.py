def RajaramanWong_clustering(nets_dict,node_delay_dict,clustering_size_limit=3,inter_cluster_delay=3):
    
    import networkx as nx
    import matplotlib.pyplot as plt
    import operator
    import pprint
    import random
    
    def form_DiGraph_dict(nets_dict,node_delay_dict):
        DiGraph_dict = {}
        for i in nets_dict:
            DiGraph_dict.update({nets_dict[i][0]:nets_dict[i][1:]})
        nxDiGraph = nx.DiGraph(DiGraph_dict)
        for i in node_delay_dict:
            nxDiGraph.nodes[i]['weight'] = node_delay_dict[i]
        return DiGraph_dict,nxDiGraph

    def form_PI(nx_graph):
        'Function to form a list of primary input nodes'
        pi = []
        for i in nx_graph.nodes():
            if nx_graph.in_degree(i)==0:
                pi.append(i)
        pi.sort()
        return pi

    def form_PO(nx_graph):
        'Function to form a list of primary output nodes'
        po = []
        for i in nx_graph.nodes():
            if nx_graph.out_degree(i)==0:
                po.append(i)
        po.sort()
        return po

    def get_Gv(nx_graph,x):
        'Function to get subgraph Gv for a node rooted at v'
        Gv_x =  list(nx.ancestors(nx_graph,x)) + list(x)
        Gv_x.sort()
        return Gv_x

    def delta_x_v(nx_graph,src,tar):
        'Function to calculate maximum delay between from node x to v'
        delta = 0
        all_simple_paths = list(nx.all_simple_paths(nx_graph,src,tar))
        all_simple_paths_dict = {}
        for i in all_simple_paths:
            k = 0
            for j in i:
                k = k + node_delay_dict[j]
            all_simple_paths_dict[str(i)]=k
            delta = max(all_simple_paths_dict.values())-node_delay_dict[src]
        return delta

    label_dict = {}
    S = {}
    cluster_dict = {}  
    def label(nx_graph,x):
        'Function to calculate l(a)'
        lab = 0
        Gv = get_Gv(nx_graph,x)
        if x in primary_input_nodes:
            lab =  node_delay_dict[x]
        else:
            lvx = []
            temp = {}
            for i in Gv[:-1]:
                lvx = (label_dict[i] + delta_x_v(nx_graph,i,x))
                temp.update({i:lvx})
            S.update({x:sort_dict_key_by_value(temp)})
            l1 = 0
            if not set(temp.keys()).isdisjoint(primary_input_nodes):
                for m in [k for k in list(temp.keys()) for l in primary_input_nodes]:
                    if temp[m]>l1:
                        l1 = temp[m]
                        
            for j in range(0,clustering_size_limit):
                try:
                    cluster_dict[x].append(S[x][0])
                    S[x].remove(S[x][0])
                except:
                    pass
                
            if S[x]==[]:
                l2 = 0
            else:
                l2 = temp[S[x][0]] + inter_cluster_delay
            lab = max(l1,l2)
            cluster_dict[x].sort()
        return label_dict.update({x:lab})

    def cluster_input(nx_graph,x):
        cluster = cluster_dict[x]
        clusterinput_temp = []
        for i in cluster:
            clusterinput_temp.extend(nx_graph.predecessors(i))
        clusterinput_temp = list(dict.fromkeys(clusterinput_temp))
        clusterinput = [i for i in clusterinput_temp if i not in cluster]
        return clusterinput

    def clustering():
        L = form_PO(nx_DAG)
        s = []
        while L!=[]:
            s.append(L[0])
            item_2b_remvd_L = L[0]
            L.remove(L[0])
            if cluster_input(nx_DAG,item_2b_remvd_L)!=[]:
                L.extend(cluster_input(nx_DAG,item_2b_remvd_L))
            L = list(dict.fromkeys(L))
            s = list(dict.fromkeys(s))
            L.sort()
            s.sort()
        return s

    def sort_dict_key_by_value(dictionary):
        sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1))
        sorted_key_list = []
        for i in sorted_dictionary:
            sorted_key_list.append(i[0])
        sorted_key_list.reverse()
        return sorted_key_list

    def pos_maker(nx_graph):
        pos_dict = {}
        for i in nx_graph.nodes():
            k = ord(i)-97
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
    
    DAG,nx_DAG = form_DiGraph_dict(nets_dict,node_delay_dict)
    #pprint.pprint(DAG)
    primary_input_nodes = form_PI(nx_DAG)
    #print(primary_input_nodes)
    primary_output_nodes = form_PO(nx_DAG)
    #print(primary_output_nodes)
    t = list(nx.topological_sort(nx_DAG))
    t.sort()
    #print(t)
    T = [i for i in t if i not in primary_input_nodes]
    #print(T)

    Gv_dict = {}
    for i in t:
        Gv_dict.update({i:get_Gv(nx_DAG,i)})
        cluster_dict.update({i:[i]})
    #pprint.pprint(Gv_dict)

    for i in t:
        label(nx_DAG,i)
    #pprint.pprint(label_dict)
    #pprint.pprint(cluster_dict)

    label_cluster_dict = {}
    for i in label_dict:
        label_cluster_dict.update({i:[label_dict[i],cluster_dict[i]]})
    #pprint.pprint(label_cluster_dict)

    roots = clustering()
    final_clusters_dict = {}
    for i in roots:
        final_clusters_dict.update({i:cluster_dict[i]})
    #pprint.pprint(final_clusters_dict)

    highest_label_node = max(label_dict, key=label_dict.get)
    #print(highest_label_node)
    maximum_delay = label_dict[highest_label_node] 
    #print(maximum_delay)

    nx.draw_networkx(nx_DAG,pos=pos_maker(nx_DAG))
    plt.show(block=False)
    #plt.pause(5)
    #plt.close()

    print('\nThe maximum delay is %s which is also the highest label value'%maximum_delay)
    print('\nLabel and Cluster information : ')
    pprint.pprint(label_cluster_dict)
    print('\nFinal clusters are')
    pprint.pprint(final_clusters_dict)
    return maximum_delay,label_cluster_dict,final_clusters_dict


