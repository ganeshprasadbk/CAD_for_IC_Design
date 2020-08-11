
def SequencePairFloorPlanning(sequence_pair,dimension_dict):
    
    import networkx as nx
    import matplotlib.pyplot as plt
    import string
    import pprint
    import operator
    import matplotlib.patches as mpatch
    
    left_of_dict = {}

    def left_of(x):
        pos_seq = list(sequence_pair[0])
        neg_seq = list(sequence_pair[1])
        temp_0 = pos_seq[0:pos_seq.index(x)]
        temp_1 = neg_seq[0:neg_seq.index(x)]
        leftof = list(set(temp_0).intersection(set(temp_1)))
        leftof.sort()
        left_of_dict.update({x:leftof})
        return leftof

    right_of_dict = {}

    def right_of(x):
        pos_seq = list(sequence_pair[0])
        neg_seq = list(sequence_pair[1])
        temp_0 = pos_seq[pos_seq.index(x):]
        temp_0.remove(x)
        temp_1 = neg_seq[neg_seq.index(x):]
        temp_1.remove(x)
        rightof = list(set(temp_0).intersection(set(temp_1)))
        rightof.sort()
        right_of_dict.update({x:rightof})
        return rightof

    above_of_dict = {}

    def above_of(x):
        pos_seq = list(sequence_pair[0])
        neg_seq = list(sequence_pair[1])
        temp_0 = pos_seq[0:pos_seq.index(x)]
        temp_1 = neg_seq[neg_seq.index(x):]
        temp_1.remove(x)
        aboveof = list(set(temp_0).intersection(set(temp_1)))
        aboveof.sort()
        above_of_dict.update({x:aboveof})
        return aboveof

    below_of_dict = {}

    def below_of(x):
        pos_seq = list(sequence_pair[0])
        neg_seq = list(sequence_pair[1])
        temp_0 = pos_seq[pos_seq.index(x):]
        temp_0.remove(x)
        temp_1 = neg_seq[0:neg_seq.index(x)]
        belowof = list(set(temp_0).intersection(set(temp_1)))
        belowof.sort()
        below_of_dict.update({x:belowof})
        return belowof

    def HCG():
        parent_of = left_of_dict.copy()
        children_of = right_of_dict.copy()
        children_of.update({'source':[]})
        for i in parent_of:
            if parent_of[i]==[]:
                children_of['source'].append(i)
                
        for i in children_of:
            if children_of[i]==[]:
                children_of[i].append('target')
                
        hcg = nx.DiGraph(children_of)
        weighted_hcg = add_node_weight(hcg,'HCG')
        return weighted_hcg

    def VCG():
        parent_of = below_of_dict.copy()
        children_of = above_of_dict.copy()
        children_of.update({'source':[]})
        for i in parent_of:
            if parent_of[i]==[]:
                children_of['source'].append(i)
                
        for i in children_of:
            if children_of[i]==[]:
                children_of[i].append('target')
                
        vcg = nx.DiGraph(children_of)
        weighted_vcg = add_node_weight(vcg,'VCG')
        return weighted_vcg

    def add_node_weight(nx_graph,graph_type):
        nodes = list(nx_graph.nodes())
        if graph_type=='HCG':
            for i in nodes:
                if i in dimension_dict.keys():
                    nx_graph.nodes[i]['weight'] = dimension_dict[i][0]
                else:
                    nx_graph.nodes[i]['weight'] = 0
        else:
            for i in nodes:
                if i in dimension_dict.keys():
                    nx_graph.nodes[i]['weight'] = dimension_dict[i][1]
                else:
                    nx_graph.nodes[i]['weight'] = 0
        return nx_graph

    def longest_path(nx_graph):
        all_simple_paths = nx.all_simple_paths(nx_graph,'source','target')
        weight_dict = {}
        for i in all_simple_paths:
            weight = 0
            for j in i:
                weight = weight + nx_graph.nodes[j]['weight']
            weight_dict.update({tuple(i):weight})
        longest_path = max(weight_dict, key=weight_dict.get)
        longest_path_length = max(weight_dict.values())
        return longest_path,longest_path_length

    def x_y_co_ordinates(block,nx_graph_h,nx_graph_v):
        all_simple_path_h = nx.all_simple_paths(nx_graph_h,'source',block)
        all_simple_path_v = nx.all_simple_paths(nx_graph_v,'source',block)
        w_dict_h = {}
        for i in all_simple_path_h:
            w_x = 0
            for j in i:
                w_x = w_x + nx_graph_h.nodes[j]['weight']
            w_x = w_x - nx_graph_h.nodes[block]['weight']
            w_dict_h.update({tuple(i):w_x})
        longest_path_s_to_x = max(w_dict_h, key=w_dict_h.get)
        x = max(w_dict_h.values())
        w_dict_v = {}
        for i in all_simple_path_v:
            w_y = 0
            for j in i:
                w_y = w_y + nx_graph_v.nodes[j]['weight']
            w_y = w_y - nx_graph_v.nodes[block]['weight']
            w_dict_v.update({tuple(i):w_y})
        longest_path_s_to_y = max(w_dict_v, key=w_dict_v.get)
        y = max(w_dict_v.values())
        return (x,y)

    def get_left_bottom_corner():
        left_bottom = {}
        for i in dimension_dict:
            xy = x_y_co_ordinates(i,hcg,vcg)
            left_bottom.update({i:xy})
        return left_bottom

    def merge_dict(lb_dict,d_dict):
        merged_dict = dict.fromkeys(lb_dict)
        for i in merged_dict.keys():
            merged_dict.update({i:[lb_dict[i],d_dict[i][0],d_dict[i][1]]})
        return merged_dict

    def draw_floorplan(dictionary,area_title,wx,hy):
        fig, ax = plt.subplots()
        rectangles = {}
        for keys in dictionary:
            rectangles.update({keys : mpatch.Rectangle(dictionary[keys][0], dictionary[keys][1], dictionary[keys][2], \
                                                      alpha=0.45, fill=True, facecolor='yellow', edgecolor = 'black', linewidth=1.25)})

        for r in rectangles:
            ax.add_artist(rectangles[r])
            rx, ry = rectangles[r].get_xy()
            cx = rx + rectangles[r].get_width()/2.0
            cy = ry + rectangles[r].get_height()/2.0
            ax.annotate(r, (cx, cy), color='black', weight='bold', fontsize=15, ha='center', va='center')

        label = 'Area is %s = %s (W)x %s (H)'%(area_title,wx,hy)
        plt.title(label, fontdict=None, loc='center', pad=None)
        plt.grid(b=False, which='major', color='#111111', linestyle='-', alpha=0.105)
        plt.minorticks_on()
        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.1)
        ax.set_xlim((0, wx))
        ax.set_ylim((0, hy))
        ax.set_aspect('equal')
        #plt.show()
        plt.show(block=False)
        #plt.pause(2)
        #plt.close()
        return

    for i in dimension_dict:
        left_of(i)
        right_of(i)
        above_of(i)
        below_of(i)

    hcg = HCG()
    hcg_longest_path,hcg_longest_path_length = longest_path(hcg)
    vcg = VCG()
    vcg_longest_path,vcg_longest_path_length = longest_path(vcg)
    Area, Width, Height = hcg_longest_path_length*vcg_longest_path_length,hcg_longest_path_length,vcg_longest_path_length
    left_bottom_corners = get_left_bottom_corner()
    print('\nLeft_of:')
    pprint.pprint(left_of_dict)
    print('\nRight_of:')
    pprint.pprint(right_of_dict)
    print('\nAbove:')
    pprint.pprint(above_of_dict)
    print('\nBelow:')
    pprint.pprint(below_of_dict)
    print('\nArea = %s, Width = %s, Height = %s'%(Area, Width, Height))
    print('\nLeft Bottom corners of each block is:')
    pprint.pprint(left_bottom_corners)

    ##nx.draw_networkx(hcg)
    ##plt.show()
    ##
    ##nx.draw_networkx(vcg)
    ##plt.show()
    draw_floorplan(merge_dict(left_bottom_corners,dimension_dict),Area,Width,Height)
    return Area, Width, Height, dimension_dict, left_bottom_corners,\
           left_of_dict, right_of_dict, above_of_dict, below_of_dict



##
###Sample Input
##sp = ('a745b638', '847b536a')
##dd = {'a':(2,4), 'b':(1,3), '3':(3,3), '4':(3,5), '5':(3,2), '6':(5,3), '7':(1,2), '8':(2,4)}
##a,w,h,d,lb,left,right,above,below = SequencePairFloorPlanning(sp,dd)
