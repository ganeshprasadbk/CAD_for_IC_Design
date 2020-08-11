def Gordian_placement(nets_dictionary,IO_pin_location_dict,cell_size_dict,chip_size,alpha):
    import networkx as nx
    import numpy as np
    import math
    import pprint 
    from qpsolvers import solve_qp
    import matplotlib.pyplot as plt
    import warnings

    
    def form_DAG_from_net_dict(nets_dictionary):
        g_dict = {}
        for i in nets_dictionary:
            g_dict.update({nets_dictionary[i][0]:nets_dictionary[i][1:]})
        for i in g_dict.keys():
            for j in nets_dictionary.keys():
                if i in nets_dictionary[j]:
                    g_dict[i].extend(nets_dictionary[j])
                    g_dict[i] = list(dict.fromkeys(g_dict[i]))
                    g_dict[i].remove(i)
                    g_dict[i].sort()
        g_nx = nx.Graph(g_dict)
        return g_dict,g_nx
            
    def assign_edge_weight():
        'Function to calculate edge weight and to add it as edge attributes'

        edge_list = list(g__nx.edges())
        for i in edge_list:
            wt = 0
            for j in nets_dictionary.values():
                if set(list(i)).issubset(j):
                    wt += 2/len(j)
            g__nx.add_edge(i[0], i[1], weight=round(wt,4))
        return

    def adjacency_matrix(x,y):
        try:
            adjacency = g__nx[x][y]['weight']
        except:
            adjacency = 0
        return adjacency

    def pin_connection_matrix(x):
        pin_connection_list = []
        for i in pins:
            pin_connection_list.append(adjacency_matrix(x,i))
        pin_connection_value = sum(pin_connection_list)
        return pin_connection_value

    def degree_matrix(x,y):
        if x==y:
            adjacency_x = 0
            for i in movable_nodes:
                adjacency_x +=  adjacency_matrix(x,i)
            degree = adjacency_x + pin_connection_matrix(x)
        else:
            degree = 0
        return degree

    def laplacian_matrix(x,y):
        laplacian = degree_matrix(x,y)-adjacency_matrix(x,y)
        return laplacian

    def fixed_pin_vectors():
        dx = []
        dy = []
        for i in movable_nodes:
            dx_row = []
            dy_row = []
            for j in pins:
                dx_row.append(-(adjacency_matrix(i,j)*IO_pin_location_dict[j][0]))
                dy_row.append(-(adjacency_matrix(i,j)*IO_pin_location_dict[j][1]))
            dx.append(sum(dx_row))
            dy.append(sum(dy_row))
        return dx,dy

    def partition(lis,ratio,level):
        size = math.ceil(len(lis)*ratio)
        list_A = lis[:size]
        list_B = lis[size:]
        return list_A,list_B

    def placement(level):
        n = len(movable_nodes)
        C = np.zeros((n,n))
        k = list(enumerate(movable_nodes))
        for i in k:
            for j in k:
                C[i[0]][j[0]] = laplacian_matrix(i[1],j[1])
        d_x,d_y = fixed_pin_vectors()
        d__x = np.array(d_x)
        d__y = np.array(d_y)
        G = np.identity(n)*-1
        h = np.array([0]*n)
        A = np.zeros((2**(level),len(movable_nodes)))
        ux = np.array([0]*(2**(level)))
        uy = np.array([0]*(2**(level)))
        if level==1:
            ux = np.array([chip_size[0]/4, chip_size[0]*3/4])
            uy = np.array([chip_size[0]/2, chip_size[0]/2])
            p0 = {}
            p1 = {}
            for i,j in zip(level_0_partition_0,level_0_partition_1):
                p0.update({i:cell_size_dict[i]})
                p1.update({j:cell_size_dict[j]})
                
            for i in movable_nodes:
                if i in p0.keys():
                    A[0][movable_nodes.index(i)] = p0[i]/sum(p0.values())
                if i in p1.keys():
                    A[1][movable_nodes.index(i)] = p1[i]/sum(p1.values())
            
        if level==2:
            ux = np.array([chip_size[0]/4, chip_size[0]/4, chip_size[0]*3/4, chip_size[0]*3/4])
            yoo = (chip_size[1]*len(level_1_partition_0)/(len(level_1_partition_0) + len(level_1_partition_1)))/2 
            yol = (chip_size[1]*len(level_1_partition_1)/(len(level_1_partition_0) + len(level_1_partition_1)))/2 + chip_size[1]*len(level_1_partition_0)/(len(level_1_partition_0) + len(level_1_partition_1))
            ylo = (chip_size[1]*len(level_1_partition_2)/(len(level_1_partition_2) + len(level_1_partition_3)))/2
            yll = (chip_size[1]*len(level_1_partition_3)/(len(level_1_partition_2) + len(level_1_partition_3)))/2 + chip_size[1]*len(level_1_partition_2)/(len(level_1_partition_2) + len(level_1_partition_3))
            uy = np.array([ yoo, yol , ylo, yll])
            p0 = {}
            p1 = {}
            p2 = {}
            p3 = {}
            for i in movable_nodes:
                if i in level_1_partition_0: p0.update({i:cell_size_dict[i]})
                if i in level_1_partition_1: p1.update({i:cell_size_dict[i]})
                if i in level_1_partition_2: p2.update({i:cell_size_dict[i]})
                if i in level_1_partition_3: p3.update({i:cell_size_dict[i]})

            for i in movable_nodes:
                if i in p0.keys():
                    A[0][movable_nodes.index(i)] = p0[i]/sum(p0.values())
                if i in p1.keys():
                    A[1][movable_nodes.index(i)] = p1[i]/sum(p1.values())
                if i in p2.keys():
                    A[2][movable_nodes.index(i)] = p2[i]/sum(p2.values())
                if i in p3.keys():
                    A[3][movable_nodes.index(i)] = p3[i]/sum(p3.values())

                    
        x = [round(i,2) for i in list(solve_qp(C.astype(np.double), d__x.astype(np.double), G.astype(np.double),
                                                 h.astype(np.double), A.astype(np.double), ux.astype(np.double)))]
        y = [round(i,2) for i in list(solve_qp(C.astype(np.double), d__y.astype(np.double), G.astype(np.double),
                                                 h.astype(np.double), A.astype(np.double), uy.astype(np.double)))]
        return x,y,dict(zip(movable_nodes,tuple(zip(x,y))))

    def draw_graph(nx_graph,node_posi,label,placement_level):
        fig, ax = plt.subplots()
        color_map = []
        for node in nx_graph:
            if node in IO_pin_location_dict.keys():
                color_map.append('red')
            else: color_map.append('green')  
        nx.draw_networkx(g__nx,node_color = color_map,pos=node_posi)
        plt.title(label+' Chip Size 4x4', fontdict=None, loc='center', pad=None)
        plt.grid(b=False, which='major', color='#111111', linestyle='-', alpha=0.13)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
        plt.axvspan(0, 0, color='black', alpha=0.9)
        plt.axhspan(0, 0, color='black', alpha=0.9)
        plt.axvspan(chip_size[0], chip_size[0], color='black', alpha=0.9)
        plt.axhspan(chip_size[1], chip_size[1], color='black', alpha=0.9)
        ax.set_xlim((-0.5, chip_size[0]+0.5))
        ax.set_ylim((-0.5, chip_size[1]+0.5))
        ax.set_aspect('equal')
        if placement_level==1:
            plt.axvspan(chip_size[0]/2, chip_size[0], color='yellow', alpha=0.5)
        if placement_level==2:
            plt.axvspan(chip_size[0]/2, chip_size[0], color='yellow', alpha=0.5)
            oo = chip_size[1]*len(level_1_partition_0)/(len(level_1_partition_0) + len(level_1_partition_1))
            plt.axhspan(0, oo, color='cyan', alpha=0.5)
            
        plt.show(block=False)
        #plt.show()
        #plt.pause(5)
        #plt.close()
        return

    warnings.filterwarnings("ignore")
    g__dict,g__nx = form_DAG_from_net_dict(nets_dictionary)
    assign_edge_weight()
    #print(list(g__nx.edges(data='weight')))
    pins = list(IO_pin_location_dict.keys())
    movable_nodes = [i for i in g__dict.keys() if i not in pins]

    x0,y0,node_pos_0 = placement(level=0)
    print('\nNodal positions after Level 0 Placement')
    pprint.pprint(node_pos_0)
    node_pos_0.update(IO_pin_location_dict)
    draw_graph(g__nx,node_pos_0,'Placement Level 0',0)

    node_arrangement_level_0 = [i[0] for i in sorted(dict(zip(movable_nodes,x0)).items(), key=lambda kv: kv[1])]
    level_0_partition_0,level_0_partition_1 = partition(node_arrangement_level_0,alpha,1)

    x1,y1,node_pos_1 = placement(level=1)
    print('\nNodal positions after Level 1 Placement')
    pprint.pprint(node_pos_1)
    node_pos_1.update(IO_pin_location_dict)
    draw_graph(g__nx,node_pos_1,'Placement Level 1',1)

    node_arrangement_level_1_0_dict = {}
    node_arrangement_level_1_1_dict = {}
    for i in level_0_partition_0:
        node_arrangement_level_1_0_dict.update({i:node_pos_1[i][1]})
    for i in level_0_partition_1:
        node_arrangement_level_1_1_dict.update({i:node_pos_1[i][1]})
    node_arrangement_level_1_0 = [i[0] for i in sorted(node_arrangement_level_1_0_dict.items(), key=lambda kv: kv[1])]
    node_arrangement_level_1_1 = [i[0] for i in sorted(node_arrangement_level_1_1_dict.items(), key=lambda kv: kv[1])]
    level_1_partition_0,level_1_partition_1 = partition(node_arrangement_level_1_0,alpha,2)
    level_1_partition_2,level_1_partition_3 = partition(node_arrangement_level_1_1,alpha,2)


    x2,y2,node_pos_2 = placement(level=2)
    print('\nNodal positions after Level 2 Placement')
    pprint.pprint(node_pos_2)
    node_pos_2.update(IO_pin_location_dict)
    draw_graph(g__nx,node_pos_2,'Placement Level 2',2)
    return x2,y2

###Sample Input
##nets = { 'n1':  ['w1',  'a',    'b'],
##             'n2':  ['w2',  'a',    'e'],
##             'n3':  ['w3',  'b',    'c',    'd'],
##             'n4':  ['w4',  'c',    'd'],
##             'n5':  ['a',   'z1',   'e',    'f'],
##             'n6':  ['b',   'f'],
##             'n7':  ['c',   'f',    'g'],
##             'n8':  ['d',   'j'],
##             'n9':  ['e',   'h'],
##             'n10': ['f',   'h',    'i'],
##             'n11': ['g',   'i',    'j'],
##             'n12': ['h',   'z2'],
##             'n13': ['i',   'z3'],
##             'n14': ['j',   'z4']}
##
##IO_pin_location = {'w1': (0,1),
##                    'w2': (0,2),
##                    'w3': (0,3),
##                    'w4': (1,4),
##                    'z1': (2,0),
##                    'z2': (3,0),
##                    'z3': (4,1),
##                    'z4': (4,2)}
##
##chip_siz = (4,4)
##cell_siz_dict = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1 }
##balance_factor= 0.5     #Area balance factor
##
##x_pos,y_pos = Gordian_placement(nets,IO_pin_location,cell_siz_dict,chip_siz,balance_factor)
