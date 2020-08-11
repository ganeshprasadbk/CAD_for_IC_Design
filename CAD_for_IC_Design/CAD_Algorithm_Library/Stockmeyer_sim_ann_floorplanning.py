def Stockmeyer_sim_ann_floorplanning(polish_expression, dimensions,lamda=0.85, P=0.95, time_bound=60):
    import random
    import Stockmeyer_floorplanning as SMfp
    import math
    import time
    import pprint
    
    def perform_M1(polish_exp):

        def possible_M1_moves(pol_exp):
            m1 = {}
            count = 0
            for ii, j in zip(pol_exp, 'H' + pol_exp):
                if ii not in ['H', 'h,', 'V', 'v'] and j not in ['H', 'h,', 'V', 'v']:
                    count = count + 1
                    m1.update({count: [ii, j]})
            return m1

        pe = list(polish_exp)
        M1 = possible_M1_moves(polish_exp)
        if (len(M1) < 1):
            str_pe = polish_exp
        else:
            random_no = random.randint(1, len(M1))
            item_1 = M1[random_no][0]
            item_2 = M1[random_no][1]
            item_1_index = pe.index(item_1)
            item_2_index = pe.index(item_2)
            pe[item_1_index], pe[item_2_index] = pe[item_2_index], pe[item_1_index]
            str_pe = ''
            for i in pe:
                str_pe += i
        return str_pe

    def perform_M2(polish_exp):
        pe = dict(enumerate(polish_exp))
        chain_pos = {}
        for i in pe.keys():
            if pe[i] in ['H','h','V','v']:
                if pe[i-1] not in ['H','h','V','v']:
                    chain_pos.update({i:[pe[i]]})
                    for j in list(pe.keys())[i+1:]:
                        if pe[j] in ['H','h','V','v']:
                            chain_pos[i].append(pe[j])
                        else:
                            break
        for i in chain_pos:
            chain_pos.update({i:''.join(chain_pos[i])})
        chosen_chain_key = random.choice(list(chain_pos.keys()))
        transtable = str.maketrans('hHvV','vVhH')
        chain_pos.update({chosen_chain_key:chain_pos[chosen_chain_key].translate(transtable)})
        l = chosen_chain_key + len(chain_pos[chosen_chain_key])
        new_polish_exp = polish_exp[:chosen_chain_key] + chain_pos[chosen_chain_key] + polish_exp[l:]
        return new_polish_exp

    def perform_M3(polish_exp):
        operandator_pair = dict(enumerate(list(zip(list(polish_exp), [''] + list(polish_exp)))))
        #pprint.pprint(operandator_pair)
        for i in list(operandator_pair.keys()):
            if (not (((operandator_pair[i][0] in ['H', 'h', 'V', 'v']) and (
                    operandator_pair[i][1] not in ['H', 'h', 'V', 'v'])) or (
                             (operandator_pair[i][0] not in ['H', 'h', 'V', 'v']) and (
                             operandator_pair[i][1] in ['H', 'h', 'V', 'v'])))):
                del operandator_pair[i]

        for i in list(operandator_pair.keys()):
            pexp = list(polish_exp)
            pexp[i - 1], pexp[i] = pexp[i], pexp[i - 1]
            str_pexp = ''
            for j in pexp:
                str_pexp += j
            if (check_balloting_property(str_pexp) == False) or (check_normality_property(str_pexp) == False):
                del operandator_pair[i]

        pe = list(polish_exp)
        if (len(operandator_pair) < 1):
            str_pe = polish_exp
        else:
            M3 = random.choice(list(operandator_pair))
            #print(operandator_pair[M3][0],operandator_pair[M3][1])
            pe[M3 - 1], pe[M3] = pe[M3], pe[M3 - 1]
            str_pe = ''
            for j in pe:
                str_pe += j
        return str_pe

    def check_balloting_property(polex):
        no_of_operands = 0
        no_of_operators = 0
        ballot = []
        for i in polex:
            if i in ['H', 'h', 'V', 'v']:
                no_of_operators += 1
            else:
                no_of_operands += 1
            ballot.append((no_of_operands, no_of_operators))
        for i in ballot:
            if i[0] == i[1]:
                return False
            else:
                pass
        return True

    def check_normality_property(polex):
        pe_0 = list(polex)
        pe_1 = [''] + list(polex)
        pe_0_1 = list(zip(pe_0, pe_1))
        for i in pe_0_1:
            if (set(i) == set(['H']) or set(i) == set(['V']) or set(i) == set(['h']) or set(i) == set(['v']) or set(
                    i) == set(['H', 'h']) or set(i) == set(['V', 'v'])):
                return False
            else:
                pass
        return True
        
    def set_initial_temperature(polish_exp):
        _,_, area_0, _, _ = SMfp.Stockmeyer_floorplanning(polish_exp, dimensions, 1)
        pe_1 = perform_M1(polish_exp)
        _,_, area_1, _, _ = SMfp.Stockmeyer_floorplanning(pe_1, dimensions, 1)
        pe_2 = perform_M2(polish_exp)
        _,_, area_2, _, _ = SMfp.Stockmeyer_floorplanning(pe_2, dimensions, 1)
        pe_3 = perform_M3(polish_exp)
        _,_, area_3, _, _ = SMfp.Stockmeyer_floorplanning(pe_3, dimensions, 1)
        
        avg = (abs(area_1 - area_0)+abs(area_2 - area_1)+abs(area_3 - area_2))/3
        To = (-avg)/(math.log(P))
        return To

    def merge_dict_n_list(dic,lis):
        dic_copy = {}
        for i,j in list(zip(list(dic.keys()),lis)):
            dic_copy.update({i:list([dic[i],j[0],j[1]])})
        return dic_copy

    def draw_floorplan(dictionary,area_title,wx,hy,wait):
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatch

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
    
    n = len(polish_expression)
    pe = polish_expression
    best_pe = polish_expression
    dim = dimensions.copy()
    initial_dim ,left_bottom_corners, initial_area, initial_width, initial_height = SMfp.Stockmeyer_floorplanning(pe, dimensions, True)
    best_dim = initial_dim
    area = initial_area
    print('\nInitial_area is %s'%initial_area)
    best_area = area
    best_left_bottom_corners = left_bottom_corners
    best_width = initial_width
    best_height = initial_height
    draw_floorplan(merge_dict_n_list(best_left_bottom_corners,best_dim),best_area,best_width,best_height,0)
    T = set_initial_temperature(polish_expression)
    print('Initial Temperature is set to %s'%T)
    MT = 1
    Reject = 0
    epsilon = 0.1*T
    timebound_1 = time.time() + time_bound
    while not(Reject / MT >= P or T < epsilon or time.time()>timebound_1):
        timebound_2 = time.time() + time_bound/2
        MT = 1
        uphill = 0
        used = 0
        while not ((uphill > n and MT > 2 * n) or time.time()>timebound_2):
            #print(timebound, time.time(), (uphill > n) or (MT > 2 * n) or (time.time() > timebound))
            new_pe = random.choice([perform_M1(pe), perform_M2(pe), perform_M3(pe)])
            #print('pe = %s' % pe)
            #print('new_pe = %s' % new_pe)
            MT += 1
            #print('MT = %s, uphill = %s' % (MT, uphill))
            new_dim,new_left_bottom_corners,new_area,new_width,new_height = SMfp.Stockmeyer_floorplanning(new_pe, dim, 0)
            delta_cost = new_area - area
            #print(delta_cost)
            #print('T = %s' % T)
            if (delta_cost < 0) or (random.uniform(0, 1) < math.exp(-(delta_cost / T))):
                if (delta_cost > 0): uphill += 1
                pe = new_pe
                dim = new_dim
                if new_area < best_area:
                    best_pe = new_pe
                    best_left_bottom_corners = new_left_bottom_corners
                    best_area = new_area
                    best_dim = new_dim
                    best_width = new_width
                    best_height = new_height
                    print('BEST Floorplanning till now..%s, Area = %s, with Dimensions %s ' % (best_pe, best_area, best_dim))
                    draw_floorplan(merge_dict_n_list(best_left_bottom_corners,best_dim),best_area,best_width,best_height,0)
                else:
                    Reject += 1
                    #print('Reject =%s' % Reject)
        T = lamda * T
        #print('T = %s' % T)
        print('Approximately %d seconds remaining'%(timebound_1-time.time()))
    print('Done with Simulation\n')
    draw_floorplan(merge_dict_n_list(best_left_bottom_corners,best_dim),best_area,best_width,best_height,1)
    return best_pe, best_area, best_dim, best_left_bottom_corners, best_width, best_height


####Sample Test Inputs
###Sample Polish Expressions;'32H6V7V4V185HVH' '37H51V82HV4V6VH','25V1H374VH6V8VH','25V1H374VH6V8VH',
###12H6H58H7H43HVH [(4, 2), (3, 1), (3, 3), (3, 5), (2, 3), (5, 3), (2, 1), (2, 4)]
##dimensions = [(4, 2), (3, 1), (3, 3), (3, 5), (2, 3), (5, 3), (2, 1), (2, 4)]
##                    # sample Dimensions for 8 block; [(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]
##                    #[(3, 5), (2, 3), (3, 6), (5, 2), (6, 2), (1, 5), (8, 3), (6, 3)]
##rigid_orientation = 1
##
##p, a, d, l, w, h = Stockmeyer_sim_ann_floorplanning('12H6H58H7H43HVH', dimensions,lamda=0.95,P=0.99,time_bound=200)
###print(p, a, d, l, w, h)

