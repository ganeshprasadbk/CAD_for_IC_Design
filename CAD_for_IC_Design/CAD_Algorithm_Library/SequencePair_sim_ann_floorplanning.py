
def SequencePair_sim_ann_floorplanning(sequence_pair, dimension_dict, lamda=0.85, P=0.95, time_bound=60):
    global flag
    import SequencePair_floorplanning as spfp
    import random
    import math
    import time
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatch
    
    def perform_M1(seq_pair, dim_dict):
        pos_seq = list(seq_pair[0])
        itemstobeswapped = random.sample(pos_seq, 2)
        index1 = pos_seq.index(itemstobeswapped[0])
        index2 = pos_seq.index(itemstobeswapped[1])
        pos_seq[index1], pos_seq[index2] = pos_seq[index2], pos_seq[index1]
        pos_seq_str = ''.join(pos_seq)
        return (pos_seq_str, seq_pair[1]), dim_dict

    def perform_M2(seq_pair, dim_dict):
        pos_seq = list(seq_pair[0])
        neg_seq = list(seq_pair[1])
        itemstobeswapped = random.sample(pos_seq, 2)
        index00 = pos_seq.index(itemstobeswapped[0])
        index01 = pos_seq.index(itemstobeswapped[1])
        index10 = neg_seq.index(itemstobeswapped[0])
        index11 = neg_seq.index(itemstobeswapped[1])
        pos_seq[index00], pos_seq[index01] = pos_seq[index01], pos_seq[index00]
        neg_seq[index10], neg_seq[index11] = neg_seq[index11], neg_seq[index10]
        pos_seq_str = ''.join(pos_seq)
        neg_seq_str = ''.join(neg_seq)
        return (pos_seq_str, neg_seq_str), dim_dict

    def perform_M3(seq_pair, dim_dict):
        dim_dict_copy = dim_dict.copy()
        key = random.choice(list(dim_dict_copy.keys()))
        rev_value = tuple(reversed(dim_dict_copy[key]))
        dim_dict_copy.update({key: rev_value})
        return seq_pair, dim_dict_copy

    def set_initial_temperature(seq_pair_T, dim_dict_T):
        area_0, _, _, _, _, _, _, _, _ = spfp.SequencePair_floorplanning(seq_pair_T, dim_dict_T)
        sp_1, dim_dict_T_1 = perform_M1(seq_pair_T, dim_dict_T)
        area_1, _, _, _, _, _, _, _, _ = spfp.SequencePair_floorplanning(sp_1, dim_dict_T_1)
        sp_2, dim_dict_T_2 = perform_M2(sp_1, dim_dict_T_1)
        area_2, _, _, _, _, _, _, _, _ = spfp.SequencePair_floorplanning(sp_2, dim_dict_T_2)
        sp_3, dim_dict_T_3 = perform_M3(sp_2, dim_dict_T_2)
        area_3, _, _, _, _, _, _, _, _ = spfp.SequencePair_floorplanning(sp_3, dim_dict_T_3)

        avg = (abs(area_1 - area_0) + abs(area_2 - area_1) + abs(area_3 - area_2)) / 3
        To = (-avg) / (math.log(P))
        return To
    
    def merge_dict(lb_dict,d_dict):
        merged_dict = dict.fromkeys(lb_dict)
        for i in merged_dict.keys():
            merged_dict.update({i:[lb_dict[i],d_dict[i][0],d_dict[i][1]]})
        return merged_dict

    def draw_floorplan(dictionary,area_title,wx,hy,wait):
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
        if wait==0:
            plt.pause(2)
            plt.close()
        return

    n = len(sequence_pair[0])
    sp = sequence_pair
    best_sp = sequence_pair
    dim = dimension_dict.copy()
    best_dim = dim.copy()
    initial_area, initial_width, initial_height, initial_dim, initial_left_bottom_corners, \
    initial_left, initial_right, initial_above, initial_below \
        = spfp.SequencePair_floorplanning(sequence_pair, dimension_dict)
    print('\nInitial_area is %s' % initial_area)
    area = initial_area
    best_area = initial_area
    best_width = initial_width
    best_height = initial_height
    best_dim = initial_dim
    best_left_bottom_corners = initial_left_bottom_corners
    best_left_of_dict = initial_left
    best_right_of_dict = initial_right
    best_above_of_dict = initial_above
    best_below_of_dict = initial_below
    draw_floorplan(merge_dict(best_left_bottom_corners,best_dim),best_area,best_width,best_height,0)
    
    T = set_initial_temperature(sequence_pair, dimension_dict)
    print('Initial Temperature is set to %s' % T)
    MT = 1
    Reject = 0
    epsilon = 0.1 * T
    timebound_1 = time.time() + time_bound
    while not (Reject / MT >= P or T < epsilon or time.time() > timebound_1):
        timebound_2 = time.time() + time_bound / 2
        MT = 1
        uphill = 0
        while not ((uphill > n and MT > 2 * n) or time.time() > timebound_2):
            # print(timebound, time.time(), (uphill > n) or (MT > 2 * n) or (time.time() > timebound))
            new_sp, new_dim_after_move = random.choice([perform_M1(sp, dim), perform_M2(sp, dim), perform_M3(sp, dim)])
            # print('sp = %s' % sp)
            MT += 1
            # print('MT = %s, uphill = %s' % (MT, uphill))
            new_area, new_width, new_height, new_dim, new_left_bottom_corners, left, right, above, below \
                      = spfp.SequencePair_floorplanning(new_sp, new_dim_after_move)
            delta_cost = new_area - area
            # print(delta_cost)
            # print('T = %s' % T)
            if (delta_cost < 0) or (random.uniform(0, 1) < math.exp(-(delta_cost / T))):
                if (delta_cost > 0): uphill += 1
                sp = new_sp
                dim = new_dim
                if new_area < best_area:
                    best_sp = new_sp
                    best_area = new_area
                    best_width = new_width
                    best_height = new_height
                    best_dim = new_dim
                    best_left_bottom_corners = new_left_bottom_corners
                    best_left_of_dict = left
                    best_right_of_dict = right
                    best_above_of_dict = above
                    best_below_of_dict = below
                    print('BEST Floorplanning till now..%s, Area = %s ' % (best_sp, best_area))
                    draw_floorplan(merge_dict(best_left_bottom_corners,best_dim),best_area,best_width,best_height,0)
            else:
                Reject += 1
                # print('Reject =%s' % Reject)
        T = lamda * T
        # print('T = %s' % T)
        
    print('Approx. %d seconds remaining' % (timebound_1 - time.time()))
    print('Simulation is completed successfully')
    draw_floorplan(merge_dict(best_left_bottom_corners,best_dim),best_area,best_width,best_height,1)
    return best_sp, best_area, best_width, best_height, best_dim, best_left_bottom_corners, \
           best_left_of_dict, best_right_of_dict, best_above_of_dict, best_below_of_dict

###Sample Input
##sp = ('17452638', '84725361')
##dd = {'1':(2,4), '2':(1,3), '3':(3,3), '4':(3,5), '5':(3,2), '6':(5,3), '7':(1,2), '8':(2,4)}
###import SequencePair_floorplanning as spfp
###a,w,h,d,lb,left,right,above,below = spfp.SequencePair_floorplanning(sp,dd)
##bsp,a,w,h,d,lb,left,right,above,below = SPfp_sim_ann.SequencePair_sim_ann_floorplanning(sp,dd)

