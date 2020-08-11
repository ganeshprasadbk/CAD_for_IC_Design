#######################################################################################################################
#---------------------------------------------------------------------------------------------------------------------#
#                               PYTHON IMPLEMENTATION OF FIDUCCIA & MATTHEYSES ALGORITHM                              #
#                                                                                       -GANESH PRASAD B K            #
#                                                                                        (2018H1230151G)              #
#_____________________________________________________________________________________________________________________#
#---------------------------------------------------------------------------------------------------------------------#
#######################################################################################################################

def Fiduccia_Mattheyses_single_pass(Hypergraph_dict,partition_A,partition_B,size_constraint):
    import pprint
    import math
    from operator import itemgetter
    
    'This function performs Fiduccia & Mattheyses bi-partioning algorithm on the given hypergraph for once'
    'It takes hyeredges entered as python dictionary as input where the nets and nodes connected by it form--'
    '--key-value pairs'
    
    nodes = list(set([x for y in Hypergraph_dict.values() for x in y]))
    nodes.sort()                                                                                                        #List containing the nodes in lexicographical order
    print(' ')                                                                  	                                #New line
    print('\nThe Hypergraph entered by the user is')
    pprint.pprint(Hypergraph_dict)                                                                                      #Prints Hypergraph in the form of dictionary
    print('The initial partitions entered by the user is %s & %s'%(partition_A,partition_B))
    print('The size constraint entered by the user is [%s:%s]'%(size_constraint[0],size_constraint[1]))
    partition_A_size = size_constraint[0]
    partition_B_size = size_constraint[1]

    print('####################################################################################################')
    print('\n==========================FIDUCCIA & MATTHEYSES Bipartitioning Algorithm==========================')
    print('\n_________________________________________PASS STARTS HERE_________________________________________')

    def neighbours(x):
        'Function to find neighbouring nodes based on given'
        'Hypergraph dictionary'
        
        neighbour_list = []                                                                                             #Initialization of empty list to store neighbouring nodes
        for i in Hypergraph_dict.keys():
            if x in Hypergraph_dict[i]:
                neighbour_list.append(Hypergraph_dict[i])
        neighbour_list_flattened = list(set([x for y in \
                                    neighbour_list for x in y])-set(x))
        neighbour_list_flattened.sort()
        return neighbour_list_flattened

    def nets(x):
        'Function that returns list of hyperedges(nets) for a given node "x"'
        nets_list = []
        for i in Hypergraph_dict.keys():
            if x in Hypergraph_dict[i]:
                nets_list.append(i)
        return nets_list


    def deg(x):
        'Function that returns the degree for a node x'
        
        hyperedges_incident_on_x = []
        for i in Hypergraph_dict.keys():
            if x in Hypergraph_dict[i]:
                hyperedges_incident_on_x.append(i)
        return len(hyperedges_incident_on_x)

    def max_deg():
        'Function to calculate Maximum degree among the given nodes'
        
        P = []
        for i in nodes:
            P.append(deg(i))
        return max(P)

    Pmax = max_deg()                                                                                                    #Pmax is calculated as max. degree
    locked_nodes = []                                                                                                   #Initialization of empty list to store locked nodes--
                                                                                                                        #--nodes which are moved once are locked and stored in locked_nodes list
    def FS(x):
        'Function to calculate FS(node)'
        
        if x in partition_A:
            partition = partition_B
        else:
            partition = partition_A
        #print(partition)
        fs = 0
        #print(list(nets(x)))
        for i in list(nets(x)):
            net_neigh = list(set(Hypergraph_dict[i])-set(x))
            #print(net_neigh)
            if set(net_neigh).issubset(partition):
                fs = fs + 1
        return fs

    def TE(x):
        'Function to calculate TE(node)'
        
        if x in partition_A:
            partition = partition_A
        else:
            partition = partition_B
        #print(partition)
        te = 0
        #print(list(nets(x)))
        for i in list(nets(x)):
            net_neigh = list(set(Hypergraph_dict[i]))
            #print(net_neigh)
            if set(net_neigh).issubset(partition):
                te = te + 1
        return te

    Gain_dict= {}                                                                                                       #Dictionary to store Gain of each node where nodes are keys and their gains are corresponding values
    def gain(x):
        'Function to calculate Gain of a node'
        
        GAIN = FS(x)-TE(x)
        return Gain_dict.update({x:GAIN})

    def update_gain_dict():
        'Function to calculate and update gain of each node after each move'
        
        for i in nodes:
            if i not in locked_nodes:
                gain(i)
        return
    update_gain_dict()

    Gain_bucket = {}
    def create_gain_bucket():
        'Function to create A GAIN BUCKET'
        
        for i in range(-Pmax,(Pmax+1)):
            Gain_bucket.update({i:[]})
        return
    create_gain_bucket()

    def update_gain_bucket():
        'Function to update the GAIN BUCKET after each move'
        
        for i in Gain_dict.keys():
            j = Gain_dict[i]
            if ((i not in Gain_bucket[j])and(i not in locked_nodes)):
                Gain_bucket[j].append(i)

        for i in Gain_bucket:
            Gain_bucket[i].sort()
        return
    update_gain_bucket()

    def rmve_neigh_of_x_from_gain_bucket(x):
        'Function to remove neighbours of x from gain bucket'
        
        for i in neighbours(x):
            for j in Gain_bucket.keys():
                if x in Gain_bucket[j]:
                    Gain_bucket[j].remove(x)
                if i in Gain_bucket[j]:
                    Gain_bucket[j].remove(i)
        del Gain_dict[x]

    def move(x):
        'Function to move nofde from one partition to another '
        
        if x in partition_A:
            partition_B.append(x)
            partition_B.sort()
            partition_A.remove(x)
            partition_A.sort()
        else:
            partition_A.append(x)
            partition_A.sort()
            partition_B.remove(x)
            partition_B.sort()
        locked_nodes.append(x)
        return

    def to_be_moved():
        'Function to check whether a MOVE is legal or not (ie.,whether a node can be moved are not)'
        'This function takes into account, pin(size) constraint, max gain from BUCKET structure for gain'
        'and then returns the node that can be moved'
        
        to_be_MOVED = '0'
        flag = 0
        for i in  list(reversed(list(Gain_bucket.keys()))):
            #print(i)
            if Gain_bucket[i]!=[]:
                #print(Gain_bucket[i])
                for j in Gain_bucket[i]:
                    to_be_MOVED = j
                    #print(to_be_MOVED)
                    if ((to_be_MOVED not in locked_nodes)and(check_size_constraint(to_be_MOVED))):
                        #print(check_size_constraint(to_be_MOVED))
                        flag = 1
                        #print('flag')
                        break
            if (flag==1):
                break
            else:
                continue
        return j

    def check_size_constraint(x):
        'Function to check if a "move" violates the size constraint are not'
        'It returns True if size constraint is met otherwise false'
        
        temp_part_A = partition_A.copy()
        temp_part_B = partition_B.copy()
        #print('%s %s'%(temp_part_A,temp_part_B))
        if x in temp_part_A:
            temp_part_B.append(x)
            temp_part_B.sort()
            temp_part_A.remove(x)
            temp_part_A.sort()
        else:
            temp_part_A.append(x)
            temp_part_A.sort()
            temp_part_B.remove(x)
            temp_part_B.sort()
        #print('%s %s'%(temp_part_A,temp_part_B))
        if((len(temp_part_A)>max(partition_A_size,partition_B_size))|\
           (len(temp_part_B)>max(partition_A_size,partition_B_size))):  
            return False
        else:
            return True

    def cut_size(partition_0,partition_1):
        'Function to return cutsize fiven 2 partitions'
        
        cut = 0
        for i in Hypergraph_dict:
            if (set(Hypergraph_dict[i]).issubset(partition_0) or \
                set(Hypergraph_dict[i]).issubset(partition_1)):
                cut = cut;
            else:
                cut = cut + 1
        return cut

    Cut_Size_list = []                                                                                                      #List to store partitions, cell tht has been moved & cut size for all MOVES
    Cut_Size_Show_case_list = []
    Cut_Size_list.append([partition_A.copy(),partition_B.copy(),[cut_size(partition_A,partition_B)]])
    Cut_Size_Show_case_list.append([['initial partition'],partition_A.copy(),\
                                    partition_B.copy(),['Cutsize = %s'%cut_size(partition_A,partition_B)]])                 #List to store (and print for user verification )partitions, cell tht has been moved & cut size for all MOVES

    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
    move_count = 0                                                                                                          #setting move count to zero in the begining of each pass
    while(set(nodes)!=set(locked_nodes)):                                                                                   #Looping through all the nodes ie., till all the nodes get locked
        move_count = move_count + 1                                                                                         #increamenting move_count
        print('----------------------------------------------%s MOVE----------------------------------------'\
              '------'%ordinal(move_count))
        k = to_be_moved()                                                                                                   #First get the node to be moved and store it in a variable
        print('PARTITIONS: %s , %s'%(partition_A,partition_B))
        print('Cell that is going to be moved is %s'%k)
        move(k)                                                                                                             #Perform MOVE operation
        print('PARTITIONS after moving cell %s is %s , %s'%(k,partition_A,partition_B))
        for i in neighbours(k):
            gain(i)                                                                                                         #Calculate GAIN for each cell
        rmve_neigh_of_x_from_gain_bucket(k) 
        update_gain_dict()                                                                                                  #Updating the Gain dictionary
        update_gain_bucket()                                                                                                #Updating the GAIN BUCKET
        print('Gain "BUCKET":')
        for i in Gain_bucket:
            print('      %s : %s'%(i,Gain_bucket[i]))                                                                       #Printing the GAIN BUCKET
        #pprint.pprint(Gain_bucket)
        cutsize = cut_size(partition_A,partition_B)                                                                         #Calculating the cutsize for new partitions
        temp_part_A = partition_A.copy()
        temp_part_B = partition_B.copy()
        print(temp_part_A)
        print('Cutsize = %s'%cutsize)
        print('Locked cells after %s move = %s'%(ordinal(move_count),locked_nodes))
        Cut_Size_list.append([partition_A.copy(),partition_B.copy(),[k],[cutsize]])                                         #Appending the Cut_Size_list with new partitions and cutsize information
        Cut_Size_Show_case_list.append([['after %s move'%ordinal(move_count)],partition_A.copy(),\
                                        partition_B.copy(),['cell moved: %s'%k],['Cutsize = %s'%cutsize]])
        print()

    def min_list_of_lists(outer_list):
        'Function that returns list of lists based the values in the lists of lists of list(3D List)'
        
        inner_list_min_value_elements = []
        for i in outer_list:
            inner_list_min_value_elements.append(list(enumerate(i))[-1][1])
            #print(inner_list_min_value_elements)
        index =  min(enumerate(inner_list_min_value_elements), key=itemgetter(1))[0]
        #print(index)
        return outer_list[index]

    print('-----------------------------------------All MOVES Completed----------------------------------------')
    print()
    print('Summary of this Single Pass of FM:')
    for i in Cut_Size_Show_case_list:
        print(i)

    FM_Single_pass_output = min_list_of_lists(Cut_Size_list)
    print(FM_Single_pass_output)
    print('\nThe partitions for this pass are %s & %s with minimum cutsize equals to %s'%\
          (FM_Single_pass_output[0],FM_Single_pass_output[1],FM_Single_pass_output[2]))
    print('\n__________________________________________PASS ENDS HERE___________________________________________')
    print('###################################################################################################')
    return FM_Single_pass_output


def Fiduccia_Mattheyses_bipartitioning(Hypergraph_dict,partition_A,partition_B,size_constraint):
    'Function to perfom FM  algorithm untill a minimum cut size obtained'
    
    min_cut1 = Fiduccia_Mattheyses_single_pass(Hypergraph_dict,partition_A,partition_B,size_constraint)
    min_cut2 = Fiduccia_Mattheyses_single_pass(Hypergraph_dict,min_cut1[0],min_cut1[1],size_constraint)

    if min_cut1[-1]>min_cut2[-1]:
        partition_A = min_cut2[0].copy()
        partition_B = min_cut2[1].copy()
        Fiduccia_Mattheyses(Hypergraph_dict,partition_A,partition_B,size_constraint)
    return min_cut1
###############################################################################################################################
###                                     PROGRAM BEGIN FROM HERE                                                             ###
###############################################################################################################################
###Sample Input
##Hypergraph = {'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['g', 'f', 'h'],'n5': ['d', 'f'],'n6': ['g', 'e']}
##size_constr = (3,5)
##partition_0 = ['a','c','d','g']
##partition_1 = ['b','e','f','h']
##
##f = FiducciaMattheyses_bipartitioning(Hypergraph,partition_0,partition_1,size_constr)
##print('\nThe final partitions after all passes are %s & %s with minimum cutsize equals to %s'%(f[0],f[1],f[2]))
