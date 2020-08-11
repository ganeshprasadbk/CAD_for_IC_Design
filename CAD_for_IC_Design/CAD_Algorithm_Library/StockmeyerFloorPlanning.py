
def StockmeyerFloorPlanning(polish_expression,dimensions,rigid_orientation):
    'Function to perform Stockmeyer Algorithm for floor planning'
    'It takes Polish expression and dimesions of each block as inputs'
    'It also asks whether the orientation of blocks is fixed or not'
    
    final_dimensions = {}           #Dictionary to hold the final dimensions of each block where keys are the block numbers and coressponding values are its dimensions in the format--> w,h
    temp_final_dimensions = {}
    
    import string
    import pprint
    
    def get_dimensions():
        'Funct'
        dim_dict = {}
        for i in polish_expression:
            for j in enumerate(dimensions):
                if i == str(j[0] + 1):
                    dim_dict.update({(int(i)): j[-1]})
                    break
        dim_dict_sort = sorted(dim_dict.items(), key=lambda k: k[0])
        dim_dict.clear()
        for i in dim_dict_sort:
            dim_dict.update({i[0]: i[-1]})
        return dim_dict


    def read_PE():
        'Function to read the given Polish expression and to form a binary tree dictionary'
        d = {}
        l = list(polish_expression)
        count = 0
        while 'H' in l or 'V' in l:
            if ('H' in l or 'V' in l):
                if ('H' in l): h_index = l.index('H')
                else: h_index = len(l)+1
                if ('V' in l): v_index = l.index('V')
                else: v_index = len(l)+1
                if h_index < v_index:
                    index = h_index
                else:
                    index = v_index
                d.update({(string.ascii_lowercase[count]): [l[index - 2], l[index - 1], l[index]]})
                del l[index - 2]
                del l[index - 2]
                del l[index - 2]
                l.insert(index - 2, string.ascii_lowercase[count])
                count = count + 1
        return d

    def get_left_child(x):
        'Function to get the left child given a node x'
        node_inf = read_PE()
        left_child = node_inf[x][0]
        return left_child
        
    def get_right_child(x):
        'Function to get the right child given a node x'
        node_inf = read_PE()
        right_child = node_inf[x][1]
        return right_child

    def get_L(x):
        'Function to get the orientaion/s of left child for given a node x'
        dim = get_dimensions()
        node_info = read_PE()
        L = ()
        if node_info[x][0] in '1234567890':
            if node_info[x][-1] == 'V':
                (wl, hl) = (dim[int(node_info[x][0])])
                if rigid_orientation == 0:
                    if (wl < hl):
                        L = ((wl, hl), (hl, wl))
                    elif (wl > hl):
                        L = ((hl, wl), (wl, hl))
                    else:
                        L = ((wl, hl),)
                else:
                    L = (wl, hl)
            if node_info[x][-1] == 'H':
                (wl, hl) = (dim[int(node_info[x][0])])
                if rigid_orientation == 0:
                    if (wl < hl):
                        L = ((hl, wl), (wl, hl))
                    elif (wl > hl):
                        L = ((wl, hl), (hl, wl))
                    else:
                        L = ((wl, hl),)
                else:
                    L = (wl, hl)
        else:
            if rigid_orientation == 0:
                L = temp_final_dimensions[node_info[x][0]]
            else:
                L = final_dimensions[node_info[x][0]]
                
        if type(L)==dict:
            if node_info[x][-1]=='V':
                sorted_L = (sorted(L.items(), key=lambda kv:kv[1][0]))
                L = tuple([i[1] for i in sorted_L])
                #print('L = {}'.format(L))
            if node_info[x][-1]=='H':
                sorted_L = (sorted(L.items(), key=lambda kv:kv[1][1]))
                L = tuple([i[1] for i in sorted_L])
                #print('L = {}'.format(L))
        return L


    def get_R(x):
        'Function to get the orientaion/s of right child for given a node x'
        dim = get_dimensions()
        node_info = read_PE()
        R = ()
        if node_info[x][1] in '1234567890':
            if node_info[x][-1] == 'V':
                (wr, hr) = (dim[int(node_info[x][1])])
                if rigid_orientation == 0:
                    if (wr < hr):
                        R = ((wr, hr), (hr, wr))
                    elif (wr > hr):
                        R = ((hr, wr), (wr, hr))
                    else:
                        R = ((wr, hr),)
                else:
                    R = (wr, hr)
            if node_info[x][-1] == 'H':
                (wr, hr) = (dim[int(node_info[x][1])])
                if rigid_orientation == 0:
                    if (wr < hr):
                        R = ((hr, wr), (wr, hr))
                    elif (wr > hr):
                        R = ((wr, hr), (hr, wr))
                    else:
                        R = ((wr, hr),)
                else:
                    R = (wr, hr)
        else:
            if rigid_orientation == 0:
                R = temp_final_dimensions[node_info[x][1]]
            else:
                R = final_dimensions[node_info[x][1]]
                
        if type(R)==dict:
            if node_info[x][-1]=='V':
                sorted_R = (sorted(R.items(), key=lambda kv:kv[1][0]))
                R = tuple([i[1] for i in sorted_R])
                #print('R = {}'.format(R))
            if node_info[x][-1]=='H':
                sorted_R = (sorted(R.items(), key=lambda kv:kv[1][1]))
                R = tuple([i[1] for i in sorted_R])
                #print('R = {}'.format(R))
                
        return R

    def dim(x):
        'Function to get the dimensions of x'
        L = get_L(x)
        LC = get_left_child(x)
        R = get_R(x)
        RC = get_right_child(x)
        node_info = read_PE()
        if rigid_orientation == 1:
            if node_info[x][-1] == 'V':
                d = ((L[0] + R[0]), max(L[1], R[1]))
            if node_info[x][-1] == 'H':
                d = (max(L[0], R[0]), (L[1] + R[1]))
            #print('L = {}'.format(L))
            #print('R = {}'.format(R))
            #print('D = {}'.format(d))
            return final_dimensions.update({x: d})
        else:
            flag = 0
            d = {}
            if node_info[x][-1] == 'V':
                d.update({'%s%s0%s0'%(x,LC,RC): ((L[0][0] + R[0][0]), max(L[0][1], R[0][1]))})
                i = 0
                j = 0
                k = 1
                while flag == 0:
                    if (L[i][1] > R[j][1]):
                        i += 1
                    elif (L[i][1] < R[j][1]):
                        j += 1
                    else:
                        i += 1
                        j += 1
                    try:
                        d.update({'%s%s%s%s%s'%(x,LC,i,RC,j): ((L[i][0] + R[j][0]), max(L[i][1], R[j][1]))})
                        k += 1
                    except:
                        flag = 1
                        break

            if node_info[x][-1] == 'H':
                d.update({'%s%s0%s0'%(x,LC,RC): (max(L[0][0], R[0][0]), (L[0][1] + R[0][1]))})
                i = 0
                j = 0
                k = 1
                while flag == 0:
                    if (L[i][0] > R[j][0]):
                        i += 1
                    elif (L[i][0] < R[j][0]):
                        j += 1
                    else:
                        i += 1
                        j += 1
                    try:
                        d.update({'%s%s%s%s%s'%(x,LC,i,RC,j): (max(L[i][0], R[j][0]), (L[i][1] + R[j][1]))})
                        k += 1
                    except:
                        flag = 1
                        break
            #print('L = {}'.format(L))
            #print('R = {}'.format(R))
            #print('D = {}'.format(d))
            temp_final_dimensions.update({x: d})
            return d

    def calculate_final_area():
        'Function to calculate the minimum total area after all setting all blocks'
        area = 0
        if rigid_orientation == 1:
            for i in read_PE().keys():
                #print('-----%s-----'%i)
                dim(i)
            #print(final_dimensions)
            width = final_dimensions[list(final_dimensions.keys())[-1]][0]
            height = final_dimensions[list(final_dimensions.keys())[-1]][1]
            area = final_dimensions[list(final_dimensions.keys())[-1]][0] * \
                   final_dimensions[list(final_dimensions.keys())[-1]][1]
        if rigid_orientation == 0:
            top_cell_dim_dict = temp_final_dimensions[list(temp_final_dimensions.keys())[-1]]
            areas_dict = {}
            for i in top_cell_dim_dict:
                areas_dict.update({i:(top_cell_dim_dict[i][0]*top_cell_dim_dict[i][1])})
            min_area_key = min(areas_dict, key=areas_dict.get)
            (width,height)= temp_final_dimensions[list(temp_final_dimensions.keys())[-1]][min_area_key]
            area = width*height
        #print(final_dimensions)
        return area,width,height

    def trace_back(x):
        'Function to choose the orientations of each block that corresponds to minimum total area'
        top_cell_dim = temp_final_dimensions[x]
        W = final_dimensions[x][0]
        H = final_dimensions[x][1]
        key = [i for i, j in top_cell_dim.items() if j==(W,H)]
        l_child = get_left_child(x)
        l_child_dim = get_L(key[0][0])[int(key[0][2])]
        r_child = get_right_child(x)
        r_child_dim = get_R(key[0][0])[int(key[0][4])]
        final_dimensions.update({l_child:l_child_dim})
        final_dimensions.update({r_child:r_child_dim})
        return

    left_bottom_corners = {}
    temp_left_bottom_corners = {}
    def find_left_bottom_corner(block):
        nodalinfo = read_PE()
        if block==list(final_dimensions.keys())[-1]:
            parent_x = 0
            parent_y = 0
            temp_left_bottom_corners.update({block:(parent_x,parent_y)})
            left_child = nodalinfo[block][0]
            right_child = nodalinfo[block][1]
            direction = nodalinfo[block][-1]
            if direction in ['h','H']:
                temp_left_bottom_corners.update({right_child:(parent_x,parent_y)})
                left_child_x = parent_x
                try:
                    left_child_y = parent_y + final_dimensions[right_child][1]
                except:
                    left_child_y = parent_y + temp_final_dimensions[int(right_child)][1]
                temp_left_bottom_corners.update({left_child:(left_child_x,left_child_y)})
            else:
                temp_left_bottom_corners.update({left_child:(parent_x,parent_y)})
                try:
                    right_child_x = parent_x + final_dimensions[left_child][0]
                except:
                    right_child_x = parent_x + temp_final_dimensions[int(left_child)][0]
                right_child_y = parent_y
                temp_left_bottom_corners.update({right_child:(right_child_x,right_child_y)})
        else:
            parent_x = temp_left_bottom_corners[block][0]
            parent_y = temp_left_bottom_corners[block][1]
            temp_left_bottom_corners.update({block:(parent_x,parent_y)})
            left_child = nodalinfo[block][0]
            right_child = nodalinfo[block][1]
            direction = nodalinfo[block][-1]
            if direction in ['h','H']:
                temp_left_bottom_corners.update({right_child:(parent_x,parent_y)})
                left_child_x = parent_x
                try:
                    left_child_y = parent_y + final_dimensions[right_child][1]
                except:
                    left_child_y = parent_y + temp_final_dimensions[int(right_child)][1]
                temp_left_bottom_corners.update({left_child:(left_child_x,left_child_y)})
            else:
                temp_left_bottom_corners.update({left_child:(parent_x,parent_y)})
                try:
                    right_child_x = parent_x + final_dimensions[left_child][0]
                except:
                    right_child_x = parent_x + temp_final_dimensions[int(left_child)][0]
                right_child_y = parent_y
                temp_left_bottom_corners.update({right_child:(right_child_x,right_child_y)})
        return
    
    def sort_dict_keywise(dictionary):
        'Function to sort a dictionary based on its keys'
        temp = sorted(dictionary.items(), key=lambda s: s[0])
        dictionary_1 = dict(zip([i[0] for i in temp],[i[1] for i in temp]))
        return dictionary_1

    def draw_floorplan(dictionary,area_title,wx,hy):
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
        #plt.pause()
        #plt.close()
        return

    def merge_dict_n_list(dic,lis):
        dic_copy = {}
        for i,j in list(zip(list(dic.keys()),lis)):
            dic_copy.update({i:list([dic[i],j[0],j[1]])})
        return dic_copy
    
    dimension_dict = get_dimensions()
    #print('The given dimension of')
    #for i in dimension_dict:
        #print('block %s is %s'%(i,dimension_dict[i]))
    node_information = read_PE()
    #print('The nodal information as read from the given polish expression is')
    #pprint.pprint(node_information)
    if rigid_orientation==0:
        for i in node_information.keys():
            #print('-----%s------'%i)
            dim(i)
        #print('------------')
        #print('The below dictionary shows the nodes with all possible arientations')
        #pprint.pprint(temp_final_dimensions)
        
    Area,Width,Height = calculate_final_area()
    #print('\nTotal Area is %s = %s(width) x %s(height) \n'%(Area,Width,Height))

    if rigid_orientation==0:
        final_dimensions.update({list(temp_final_dimensions.keys())[-1]:(Width,Height)})
        for i in reversed(list(temp_final_dimensions.keys())):
            trace_back(i)
        for_sorting = final_dimensions.copy()
        final_dimensions = sort_dict_keywise(for_sorting)
        print('')
        for i in final_dimensions:
            if i not in string.ascii_lowercase:
                if final_dimensions[i]==dimension_dict[int(i)]:
                    print('The dimension of block %s is %s which is same as initial'%(i,final_dimensions[i]))
                else:
                    print('The dimension of block %s was %s and is now changed to %s '%(i,dimension_dict[int(i)],final_dimensions[i]))
            else:
                print('The dimension of node %s is %s '%(i,final_dimensions[i]))
    else:
        temp_final_dimensions = get_dimensions()
        #final_dimensions.update(temp_final_dimensions)


    for i in reversed(list(final_dimensions.keys())):
        try:
            find_left_bottom_corner(i)
        except:
            #sorted_left_bottom_corners = sort_dict_keywise(temp_left_bottom_corners)
            pass
    sorted_left_bottom_corners = sort_dict_keywise(temp_left_bottom_corners)
    for i in list(sorted_left_bottom_corners.keys()):
        if str(i) not in string.ascii_lowercase:
            left_bottom_corners.update({i:sorted_left_bottom_corners[i]})

    if rigid_orientation==0:
        final_dimension_list = []
        for i in final_dimensions:
            if str(i).isdigit():
                final_dimension_list.append(final_dimensions[i])
    else:
        final_dimension_list = dimensions.copy()

    print('\nArea = %s'%Area)
    print('Width = %s'%Width)
    print('Height = %s'%Height)
    #print('Left bottom Corners of the blocks are')
    #pprint.pprint(left_bottom_corners)
    draw_floorplan(merge_dict_n_list(left_bottom_corners,final_dimension_list),Area,Width,Height)
    return final_dimension_list,left_bottom_corners,Area,Width,Height


##
###Sample Input    
##pex = '32H6V7V4V185HVH'
##d = [(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]
##fd,lbc,a,w,h=StockmeyerFloorPlanning(pex,d,1)


