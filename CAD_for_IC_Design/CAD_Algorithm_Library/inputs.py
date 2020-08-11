import RajaramanWong_clustering as RWc
import FlowMap_clustering as FMc
import EdgeCoarsening_clustering as ECc
import HyperEdgeCoarsening_clustering as HECc
import ModifiedHyperEdgeCoarsening_clustering as MHECc
import KerninghanLin_Bipartitioning as KLbp
import FiducciaMattheyses_bipartitioning as FMbp
import EIG_bipartitioning as EIGbp
import Stockmeyer_sim_ann_floorplanning as SMfp_sim_ann
import StockmeyerFloorPlanning as smfp
import Stockmeyer_floorplanning as SMfp
import SequencePair_sim_ann_floorplanning as SPfp_sim_ann
import SequencePair_floorplanning as SPfp
import Gordian_placement as Gordp
import L_Steiner_routing as LStnr
import pprint

"""
#RajaramanWong_clustering
nets = { 'n1':  ['a', 'd', 'f'],
         'n2':  ['b', 'd', 'e'],
         'n3':  ['c', 'e', 'h'],
         'n4':  ['f', 'i'],
         'n5':  ['d', 'i'],
         'n6':  ['e', 'g'],
         'n7':  ['g', 'i', 'j'],
         'n8':  ['h', 'j', 'l'],
         'n9':  ['i', 'k'],
         'n10': ['j', 'k', 'l']}

node_delay = {'a':1,'b': 1,'c': 1,'d': 3,'e': 2,'f': 3,'g': 2,'h': 3,'i': 4,'j': 4,'k': 1,'l': 1}

clustering_size_limit = 4
inter_cluster_delay = 5

max_delay,label_n_cluster,f_clusters=RWc.RajaramanWong_clustering(nets,node_delay,3,3)
# print('The maximum delay is %s which is also the highest label value'%max_delay)
# print('\nLabel and Cluster information : ')
# pprint.pprint(label_n_cluster)
# print('\nFinal clusters are')
# pprint.pprint(f_clusters)
"""

"""
#FlowMap_clustering
nets_f = {'n1':['r','d','e'],'n2':['s','a','b'],'n3':['t','a','e','f'],'n4':['u','b'],'n5': ['v','c'],'n6':['w','c','g'],'n7':['a','d','h'],'n8':['b','i'],'n9':['c','f','g'],'n10':['d','h'],'n11':['e','j'],'n12':['f','i'],'n13':['g','k'],'n14':['i','j','k']}
pins_per_lut = 3
max_delay,label_n_cluster,lut = FMc.FlowMap_clustering(nets_f,pins_per_lut)
print('The maximum delay is %s which is also the highest label value'%max_delay)
print('\nLabel and Cluster information : ')
pprint.pprint(label_n_cluster)
print('\nLUTs are')
pprint.pprint(lut)
"""

"""
#EdgeCoarsensing_clustering
hg = {'n1': ['a', 'c', 'e'],
       'n2': ['b', 'c', 'd'],
       'n3': ['c', 'e', 'f'],
       'n4': ['d', 'f'],
       'n5': ['e', 'g'],
       'n6': ['f', 'g', 'h']}
nod_delay = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}
import pprint
cl_dic, f_clu = ECc.EdgeCoarsening_clustering(hg,nod_delay)
print('The Hypergraph entered by the user is')
pprint.pprint(hg)     
print('\nEdge coarsening result:\n')
pprint.pprint(cl_dic)
print('\nNetlist transformation based on EC result.:\n')
pprint.pprint(f_clu)
"""

"""
#HyperEdge_coarsening
hg  = {'n1': ['a', 'c', 'e'],
       'n2': ['b', 'c', 'd'],
       'n3': ['c', 'e', 'f'],
       'n4': ['d', 'f'],
       'n5': ['e', 'g'],
       'n6': ['f', 'g', 'h']}
nod_delay = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}
import pprint
print('The Hypergraph entered by the user is')
pprint.pprint(hg)                                                                  
cl_dict,f_cl = HECc.HyperEdgeCoarsening_clustering(hg,nod_delay)
print('\nHyperedge coarsening result:\n')
pprint.pprint(cl_dict)
print('\nNetlist transformation based on HEC result.:\n')
pprint.pprint(f_cl)
"""

"""
#ModifiedHyperEdgeCoarsening_clustering
hg  = {'n1': ['a', 'c', 'e'],
       'n2': ['b', 'c', 'd'],
       'n3': ['c', 'e', 'f'],
       'n4': ['d', 'f'],
       'n5': ['e', 'g'],
       'n6': ['f', 'g', 'h']}
import pprint
print('The hypergraph_dict entered by the user is')
pprint.pprint(hg)                                                                  
nod_delay = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}
cl_dict,f_cl = MHECc.ModifiedHyperEdgeCoarsening_clustering(hg,nod_delay)
print('\nModified Hyperedge coarsening result:\n')
pprint.pprint(cl_dict)
print('\nNetlist transformation based on MHEC result.:\n')
pprint.pprint(f_cl)
"""


Hypergraph = {'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['g', 'f', 'h'],'n5': ['d', 'f'],'n6': ['g', 'e']}
size_constr = (3,5)
partition_0 = ['a','c','d','g']
partition_1 = ['b','e','f','h']

f = FMbp.Fiduccia_Mattheyses_bipartitioning(Hypergraph,partition_0,partition_1,size_constr)
print('\nThe final partitions after all passes are %s & %s with minimum cutsize equals to %s'%(f[0],f[1],f[2]))


"""
#EIG_bipartitioning
nets =  {'n1': ['a', 'd', 'f'],
         'n2': ['b', 'd', 'e', 'g', 'h'],
         'n3': ['c', 'e', 'h'],
         'n4': ['d', 'f', 'g'],
         'n5': ['e', 'g', 'h', 'j'],
         'n6': ['f', 'i'],
         'n7': ['g', 'i', 'j'],
         'n8': ['h', 'j']}

partition_size=[['5', '5'],['6','4']] 
bal_part,fin_part = EIGbp.EIG_bipartitioning(nets,partition_size)
"""

"""
#StockmeyerFloorPlanning
pex = '32H6V7V4V185HVH'
d = [(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]
fd,lbc,a,w,h=smfp.StockmeyerFloorPlanning(pex,d,1)
"""

"""
#Stockmeyer_sim_ann_floorplanning
d = [(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]
p, a, d, l, w, h = SMfp_sim_ann.Stockmeyer_sim_ann_floorplanning('25V1H374VH6V8VH', d,lamda=0.95,P=0.99,time_bound=200)
print(p, a, d, l, w, h)
"""

"""
#import SequencePair_floorplanning as spfp
#a,w,h,d,lb,left,right,above,below = spfp.SequencePair_floorplanning(sp,dd)
bsp,a,w,h,d,lb,left,right,above,below = SPfp_sim_ann.SequencePair_sim_ann_floorplanning(sp,dd)
"""

"""
#SequencePair_sim_ann_floorplanning
sp = ('17452638', '84725361')
dd = {'1':(2,4), '2':(1,3), '3':(3,3), '4':(3,5), '5':(3,2), '6':(5,3), '7':(1,2), '8':(2,4)}
"""


"""
#Gordian_placement
nets = {'n1':['w1','a','b'],'n2':['w2','a','e'],'n3':['w3','b','c','d'],'n4':['w4','c','d'],'n5':['a','z1','e','f'],'n6':['b','f'],'n7':['c','f','g'],'n8':['d','j'],'n9':['e','h'],'n10':['f','h','i'],'n11':['g','i','j'],'n12':['h','z2'],'n13':['i','z3'],'n14':['j','z4']}

IO_pin_location = {'w1': (0,1),'w2': (0,2),'w3': (0,3),'w4': (1,4),'z1': (2,0),'z2': (3,0),'z3': (4,1),'z4': (4,2)}

chip_siz = (4,4)
cell_siz_dict = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1 }
balance_factor= 0.5     #Area balance factor

x_pos,y_pos = Gordp.Gordian_placement(nets,IO_pin_location,cell_siz_dict,chip_siz,balance_factor)
"""

"""
#L_Steiner_routing
node_location_dict = {'a': (1,5),'b': (4,4),'c': (2,8),'d': (3,7),'e': (6,9),'f': (7,5),'g': (8,1),'h': (10,2),'i': (10,10)}
LStnr.L_Steiner_routing(node_location_dict)
"""
