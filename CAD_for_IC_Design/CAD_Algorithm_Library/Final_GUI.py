from tkinter import *
import tkinter as tk
from functools import partial
import pprint
import RajaramanWong_clustering as RWc
import ast
import subprocess as sub
import sys

import RajaramanWong_clustering as RWc
import FlowMap_clustering as FMc
import EdgeCoarsening_clustering as ECc
import HyperEdgeCoarsening_clustering as HECc
import ModifiedHyperEdgeCoarsening_clustering as MHECc
import KerninghanLin_Bipartitioning as KLbp
import FiducciaMattheyses_bipartitioning as FMbp
import EIG_bipartitioning as EIGbp
import Stockmeyer_sim_ann_floorplanning as SMfp_sim_ann
import StockmeyerFloorPlanning as SMFP
import Stockmeyer_floorplanning as SMfp
import SequencePair_sim_ann_floorplanning as SPfp_sim_ann
import SequencePairFloorPlanning as SPFP
import SequencePair_floorplanning as SPfp
import Gordian_placement as Gordp
import L_Steiner_routing as LStnr

physical_design_steps = ['CLUSTERING', 'PARTITIONING', 'FLOOPRPLANNING', 'PLACEMENT', 'ROUTING']
menus = [0, 1, 2]

def font_config(widget, fontslant, event):
    widget.configure(font=fontslant)
    return

def cls():
    print('\n'*50)

def clear_ok_previousmenu(window,run_fun,clear_com,previous_com,row_no):
    clear_button = Button(window, text='clear', command =  clear_com)
    clear_button.grid(row=row_no, column=1, sticky=W, pady=4, padx=10)
    
    okRW_button = Button(window, text='OK', command=run_fun)
    okRW_button.grid(row=row_no, column=1, sticky=W, pady=4, padx = 60)

    previousmenuRW_button = Button(window, text='previous MENU', command = previous_com)
    previousmenuRW_button.grid(row=row_no, column=1, sticky=W, pady=4, padx = 110)

    text = Label(window, text="Sample Inputs are provided. To enter New Data press 'clear' &  \n enter input in the 'same format' as Sample Input")
    text.bind("<Enter>", partial(font_config, text, "Helvetica 9 italic"))
    text.bind("<Leave>", partial(font_config, text, "Helvetica 9"))
    text.grid(row=row_no+1, column=1, sticky=W)
    return

def clustering_algorithms():
    def clustering_selection(*args):
        slave = Tk()
        
        if varc.get() == 'Rajaraman-Wong Algorithm':
            def run_RW():
                netsRW = ast.literal_eval(netlistRw_entry.get())
                node_delayRW = ast.literal_eval(nodedelayRW_entry.get())
                clu_size_lim = int(clustering_size_limit_entry.get())
                int_clu_del = int(inter_cluster_delay_entry.get())
                max_delay,label_n_cluster,f_clusters=RWc.RajaramanWong_clustering(netsRW,node_delayRW,clu_size_lim,int_clu_del)
                return
            
            netlistRW_label = Label(slave, text='Enter Netlist: ' )
            netlistRW_label.grid(row=0, sticky=E)
            
            nodedelayRW_label = Label(slave, text='Enter Node delay dictionary: ')
            nodedelayRW_label.grid(row=1, sticky=E)
            
            clustering_size_limit_label = Label(slave, text="Enter Max. clustering size limit: " )
            clustering_size_limit_label.grid(row=2, sticky=E)
            
            inter_cluster_delay_label = Label(slave, text="Enter Inter-cluster delay: ")
            inter_cluster_delay_label.grid(row=3, sticky=E)
            
            netlistRw_entry = Entry(slave, width=125)
            netlistRw_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistRw_entry.insert(0,"{ 'n1':['a','d','f'],'n2':['b','d','e'],'n3': ['c','e','h'],'n4': ['f','i'],'n5':['d','i'],'n6':['e','g'],'n7':['g','i','j'],'n8':['h','j','l'],'n9': ['i','k'],'n10':['j','k','l']}")
            
            nodedelayRW_entry = Entry(slave, width=70)
            nodedelayRW_entry.grid(row=1,column=1, sticky=W, padx=5)
            nodedelayRW_entry.insert(0,"{'a':1,'b': 1,'c': 1,'d': 1,'e': 1,'f': 1,'g': 1,'h': 1,'i': 1,'j': 1,'k': 1,'l': 1}")

            clustering_size_limit_entry = Entry(slave)
            clustering_size_limit_entry.grid(row=2,column=1, sticky=W, padx=5)
            clustering_size_limit_entry.insert(0,'4')

            inter_cluster_delay_entry = Entry(slave)
            inter_cluster_delay_entry.grid(row=3,column=1, sticky=W, padx=5)
            inter_cluster_delay_entry.insert(0,'5')

            clear_comm = lambda:(netlistRw_entry.delete(0,'end'),nodedelayRW_entry.delete(0,'end'),clustering_size_limit_entry.delete(0,'end'),inter_cluster_delay_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 4
            clear_ok_previousmenu(slave,run_RW,clear_comm,previous_comm,row_numb)

        if varc.get() == 'Flowmap Algorithm':
            def run_FMAP():
                netsfmap = ast.literal_eval(netlistfmap_entry.get())
                #node_delay_fmap = ast.literal_eval(nodedelayfmap_entry.get())
                pins_per_lut = int(pins_per_lut_entry.get())
                max_delay,label_n_cluster,LUTs = FMc.FlowMap_clustering(netsfmap,pins_per_lut)
                return
            
            netlistfmap_label = Label(slave, text='Enter Netlist: ' )
            netlistfmap_label.grid(row=0, sticky=E)
            
            #nodedelayfmap_label = Label(slave, text='Enter Node delay dictionary: ')
            #nodedelayfmap_label.grid(row=1, sticky=E)
            
            pins_per_lut_label = Label(slave, text="Enter Max. number of PINs per LUT: " )
            pins_per_lut_label.grid(row=1, sticky=E)
                        
            netlistfmap_entry = Entry(slave, width=125)
            netlistfmap_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistfmap_entry.insert(0,"{'n1':['r','d','e'],'n2':['s','a','b'],'n3':['t','a','e','f'],'n4':['u','b'],'n5': ['v','c'],'n6':['w','c','g'],'n7':['a','d','h'],'n8':['b','i'],'n9':['c','f','g'],'n10':['d','h'],'n11':['e','j'],'n12':['f','i'],'n13':['g','k'],'n14':['i','j','k']}")
            
            #nodedelayfmap_entry = Entry(slave, width=70)
            #nodedelayfmap_entry.grid(row=1,column=1, sticky=W, padx=5)
            #nodedelayfmap_entry.insert(0,"{'a':1,'b': 1,'c': 1,'d': 3,'e': 2,'f': 3,'g': 2,'h': 3,'i': 4,'j': 4,'k': 1,'l': 1}")

            pins_per_lut_entry = Entry(slave)
            pins_per_lut_entry.grid(row=1,column=1, sticky=W, padx=5)
            pins_per_lut_entry.insert(0,'3')

            clear_comm = lambda:(netlistfmap_entry.delete(0,'end'),pins_per_lut_entry.delete(0,'end')) #nodedelayfmap_entry.delete(0,'end')
            previous_comm = lambda:slave.destroy()
            row_numb = 2
            clear_ok_previousmenu(slave,run_FMAP,clear_comm,previous_comm,row_numb)

        if varc.get() == 'Edge Coarsening Algorithm':
            def run_EC():
                netsEC = ast.literal_eval(netlistEC_entry.get())
                node_delayEC = ast.literal_eval(nodedelayEC_entry.get())
                cl_dic, f_clu = ECc.EdgeCoarsening_clustering(netsEC,node_delayEC)
                return
            
            netlistEC_label = Label(slave, text='Enter Netlist: ' )
            netlistEC_label.grid(row=0, sticky=E)
            
            nodedelayEC_label = Label(slave, text='Enter Node delay dictionary: ')
            nodedelayEC_label.grid(row=1, sticky=E)
            
            netlistEC_entry = Entry(slave, width=125)
            netlistEC_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistEC_entry.insert(0,"{'n1':['a','c','e'],'n2':['b','c','d'],'n3':['c','e','f'],'n4':['d','f'],'n5':['e','g'],'n6':['f','g','h']}")
            
            nodedelayEC_entry = Entry(slave, width=70)
            nodedelayEC_entry.grid(row=1,column=1, sticky=W, padx=5)
            nodedelayEC_entry.insert(0,"{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}")

            clear_comm = lambda:(netlistEC_entry.delete(0,'end'),nodedelayEC_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 2
            clear_ok_previousmenu(slave,run_EC,clear_comm,previous_comm,row_numb)
            
        if varc.get() == 'Hyperedge Coarsening Algorithm':
            def run_HEC():
                netsHEC = ast.literal_eval(netlistHEC_entry.get())
                node_delayHEC = ast.literal_eval(nodedelayHEC_entry.get())
                cl_dic, f_clu = HECc.HyperEdgeCoarsening_clustering(netsHEC,node_delayHEC)
                return
            
            netlistHEC_label = Label(slave, text='Enter Netlist: ' )
            netlistHEC_label.grid(row=0, sticky=E)
            
            nodedelayHEC_label = Label(slave, text='Enter Node delay dictionary: ')
            nodedelayHEC_label.grid(row=1, sticky=E)
            
            netlistHEC_entry = Entry(slave, width=125)
            netlistHEC_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistHEC_entry.insert(0,"{'n1':['a','c','e'],'n2':['b','c','d'],'n3':['c','e','f'],'n4':['d','f'],'n5':['e','g'],'n6':['f','g','h']}")
            
            nodedelayHEC_entry = Entry(slave, width=70)
            nodedelayHEC_entry.grid(row=1,column=1, sticky=W, padx=5)
            nodedelayHEC_entry.insert(0,"{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}")

            clear_comm = lambda:(netlistHEC_entry.delete(0,'end'),nodedelayHEC_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 2
            clear_ok_previousmenu(slave,run_HEC,clear_comm,previous_comm,row_numb)

        if varc.get() == 'Modified Hyperedge Coarsening Algorithm':
            def run_MHEC():
                netsMHEC = ast.literal_eval(netlistMHEC_entry.get())
                node_delayMHEC = ast.literal_eval(nodedelayMHEC_entry.get())
                cl_dic, f_clu = MHECc.ModifiedHyperEdgeCoarsening_clustering(netsMHEC,node_delayMHEC)
                return
            
            netlistMHEC_label = Label(slave, text='Enter Netlist: ' )
            netlistMHEC_label.grid(row=0, sticky=E)
            
            nodedelayMHEC_label = Label(slave, text='Enter Node delay dictionary: ')
            nodedelayMHEC_label.grid(row=1, sticky=E)
            
            netlistMHEC_entry = Entry(slave, width=125)
            netlistMHEC_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistMHEC_entry.insert(0,"{'n1':['a','c','e'],'n2':['b','c','d'],'n3':['c','e','f'],'n4':['d','f'],'n5':['e','g'],'n6':['f','g','h']}")
            
            nodedelayMHEC_entry = Entry(slave, width=70)
            nodedelayMHEC_entry.grid(row=1,column=1, sticky=W, padx=5)
            nodedelayMHEC_entry.insert(0,"{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1}")

            clear_comm = lambda:(netlistMHEC_entry.delete(0,'end'),nodedelayMHEC_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 2
            clear_ok_previousmenu(slave,run_MHEC,clear_comm,previous_comm,row_numb)

    algorithmsc = ['Rajaraman-Wong Algorithm', 'Flowmap Algorithm', 'Edge Coarsening Algorithm','Hyperedge Coarsening Algorithm','Modified Hyperedge Coarsening Algorithm', ]
    varc = tk.StringVar(root)
    varc.set(algorithmsc[0])  # default value
    varc.trace("w", clustering_selection)
    menus[0] = tk.OptionMenu(*(root, varc) + tuple(algorithmsc))
    menus[0].grid(row=8, sticky='ew')

def partitioning_algorithms():
    def partitioning_selection(*args):
        slave = Tk()

        if varp.get() == 'Kerninghan & Lin Algorithm':
            def run_KL():
                netlistKL = ast.literal_eval(netlistKL_entry.get())
                ugKL = ast.literal_eval(ugKL_entry.get())
                init_partition_1_KL = ast.literal_eval(partition1KL_entry.get())
                init_partition_2_KL  = ast.literal_eval(partition2KL_entry.get())
                passes_KL = ast.literal_eval(passesKL_entry.get())
                output_KL = KLbp.KerninghanLin_Bipartitioning(ugKL,netlistKL,init_partition_1_KL,init_partition_2_KL,passes_KL)
                return
            
            netlistKL_label = Label(slave, text='Enter Netlist: ' )
            netlistKL_label.grid(row=0, sticky=E)

            ugKL_label = Label(slave, text='Enter graph dictionary: ' )
            ugKL_label.grid(row=1, sticky=E)
            
            partition1KL_label = Label(slave, text='Enter the initial Partition A: ')
            partition1KL_label.grid(row=2, sticky=E)

            partition2KL_label = Label(slave, text='Enter the initial Partition B: ')
            partition2KL_label.grid(row=3, sticky=E)

            passesKL_label = Label(slave, text='Enter the number of passes: ')
            passesKL_label.grid(row=4, sticky=E)
            
            netlistKL_entry = Entry(slave, width=125)
            netlistKL_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistKL_entry.insert(0,"{'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['g', 'f', 'h'],'n5': ['d', 'f'],'n6': ['g', 'e']}")

            ugKL_entry = Entry(slave, width=125)
            ugKL_entry.grid(row=1,column=1, sticky=W, padx=5)
            ugKL_entry.insert(0,"{'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['d', 'f'],'n5': ['e', 'g'],'n6': ['f', 'g', 'h']}")
            
            partition1KL_entry = Entry(slave)
            partition1KL_entry.grid(row=2,column=1, sticky=W, padx=5)
            partition1KL_entry.insert(0,"['a','b','d','e']")

            partition2KL_entry = Entry(slave)
            partition2KL_entry.grid(row=3,column=1, sticky=W, padx=5)
            partition2KL_entry.insert(0,"['c','f','g','h']")
            
            passesKL_entry = Entry(slave)
            passesKL_entry.grid(row=4,column=1, sticky=W, padx=5)
            passesKL_entry.insert(0,'2')
            
            clear_comm = lambda:(netlistKL_entry.delete(0,'end'),ugKL_entry.delete(0,'end'),partition1KL_entry.delete(0,'end'),partition2KL_entry.delete(0,'end'),passesKL_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 5
            clear_ok_previousmenu(slave,run_KL,clear_comm,previous_comm,row_numb)
            
        if varp.get() == 'Fiduccia Mattheyses Algorithm':
            def run_FM():
                netlistFM = ast.literal_eval(netlistFM_entry.get())
                init_partition_1_FM = ast.literal_eval(partition1FM_entry.get())
                init_partition_2_FM  = ast.literal_eval(partition2FM_entry.get())
                size_constraint_FM = ast.literal_eval(size_cnstrntFM_entry.get())
                output_FM = FMbp.Fiduccia_Mattheyses_bipartitioning(netlistFM,init_partition_1_FM,init_partition_2_FM,size_constraint_FM)
                return
            
            netlistFM_label = Label(slave, text='Enter Netlist: ' )
            netlistFM_label.grid(row=0, sticky=E)
            
            partition1FM_label = Label(slave, text='Enter the initial Partition A: ')
            partition1FM_label.grid(row=1, sticky=E)

            partition2FM_label = Label(slave, text='Enter the initial Partition B: ')
            partition2FM_label.grid(row=2, sticky=E)

            size_cnstrntFM_label = Label(slave, text='Enter the size constraint for partitions: ')
            size_cnstrntFM_label.grid(row=3, sticky=E)
            
            netlistFM_entry = Entry(slave, width=125)
            netlistFM_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistFM_entry.insert(0,"{'n1': ['a', 'c', 'e'],'n2': ['b', 'c', 'd'],'n3': ['c', 'e', 'f'],'n4': ['g', 'f', 'h'],'n5': ['d', 'f'],'n6': ['g', 'e']}")
            
            partition1FM_entry = Entry(slave)
            partition1FM_entry.grid(row=1,column=1, sticky=W, padx=5)
            partition1FM_entry.insert(0,"['a','c','d','g']")

            partition2FM_entry = Entry(slave)
            partition2FM_entry.grid(row=2,column=1, sticky=W, padx=5)
            partition2FM_entry.insert(0,"['b','e','f','h']")
            
            size_cnstrntFM_entry = Entry(slave)
            size_cnstrntFM_entry.grid(row=3,column=1, sticky=W, padx=5)
            size_cnstrntFM_entry.insert(0,'(3,5)')
            
            clear_comm = lambda:(netlistFM_entry.delete(0,'end'),partition1FM_entry.delete(0,'end'),partition2FM_entry.delete(0,'end'),size_cnstrntFM_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 4
            clear_ok_previousmenu(slave,run_FM,clear_comm,previous_comm,row_numb)
            
        if varp.get() == 'EIG Algorithm':
            def run_EIG():
                netsEIG = ast.literal_eval(netlistEIG_entry.get())
                partition_size_EIG = ast.literal_eval(partition_sizeEIG_entry.get())
                balanced_partition_EIG,final_partition_EIG = EIGbp.EIG_bipartitioning(netsEIG,partition_size_EIG)
                return
            
            netlistEIG_label = Label(slave, text='Enter Netlist: ' )
            netlistEIG_label.grid(row=0, sticky=E)
            
            partition_sizeEIG_label = Label(slave, text='Enter Node delay dictionary: ')
            partition_sizeEIG_label.grid(row=1, sticky=E)
            
            netlistEIG_entry = Entry(slave, width=125)
            netlistEIG_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistEIG_entry.insert(0,"{'n1': ['a','d','f'],'n2': ['b','d','e','g','h'],'n3': ['c','e','h'],'n4': ['d','f','g'],'n5': ['e','g','h','j'],'n6': ['f','i'],'n7': ['g','i','j'],'n8': ['h','j']}")
            
            partition_sizeEIG_entry = Entry(slave, width=70)
            partition_sizeEIG_entry.grid(row=1,column=1, sticky=W, padx=5)
            partition_sizeEIG_entry.insert(0,"[['5', '5'],['6','4']]")

            clear_comm = lambda:(netlistEIG_entry.delete(0,'end'),partition_sizeEIG_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 2
            clear_ok_previousmenu(slave,run_EIG,clear_comm,previous_comm,row_numb)

        #if varp.get() == 'Flow-Based Bipartitioning Algorithm':

    algorithmsp = ['Kerninghan & Lin Algorithm', 'Fiduccia Mattheyses Algorithm', 'EIG Algorithm','Flow-Based Bipartitioning Algorithm']
    varp = StringVar(root)
    varp.set(algorithmsp[0])  # default value
    varp.trace("w", partitioning_selection)
    menus[1] = OptionMenu(*(root, varp) + tuple(algorithmsp))
    menus[1].grid(row=8, sticky='ew')


def floorplanning_algorithms():
    def floorplanning_selection(*args):
        slave = Tk()

        if varfp.get() == 'Stockmeyer Algorithm':
            def run_SM():
                polish_SM = polish_expSM_entry.get()
                dimension_SM = ast.literal_eval(dimensionSM_entry.get())
                orientation_SM = ast.literal_eval(orientationSM_entry.get())
                fin_dim_list_SM, left_bot_SM, Area_SM, Width_SM, Height_SM = SMFP.StockmeyerFloorPlanning(polish_SM,dimension_SM,orientation_SM)
                return
            
            polish_expSM_label = Label(slave, text='Enter Normalized Polish Expression: ' )
            polish_expSM_label.grid(row=0, sticky=E)

            dimensionSM_label = Label(slave, text='Enter Dimension list: ' )
            dimensionSM_label.grid(row=1, sticky=E)

            orientationSM_label = Label(slave, text='Is changing of orientation of blocks NOT allowed?\n Type True/1 for Yes or False/0 for No', justify=RIGHT )
            orientationSM_label.grid(row=2, sticky=E)

            polish_expSM_entry = Entry(slave, width=50)
            polish_expSM_entry.grid(row=0,column=1, sticky=W, padx=5)
            polish_expSM_entry.insert(0,'37H51V82HV4V6VH')
            
            dimensionSM_entry = Entry(slave, width=50)
            dimensionSM_entry.grid(row=1,column=1, sticky=W, padx=5)
            dimensionSM_entry.insert(0,'[(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]')
            
            orientationSM_entry = Entry(slave)
            orientationSM_entry.grid(row=2,column=1, sticky=W, padx=5)
            orientationSM_entry.insert(0,'True')

            clear_comm = lambda:(polish_expSM_entry.delete(0,'end'),dimensionSM_entry.delete(0,'end'),orientationSM_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 3
            clear_ok_previousmenu(slave,run_SM,clear_comm,previous_comm,row_numb)
            
        if varfp.get() == 'Stockmeyer Algorithm-Simulated Annealing':
            def run_SMsimann():
                polish_SMsimann = polish_expSMsimann_entry.get()
                dimension_SMsimann = ast.literal_eval(dimensionSMsimann_entry.get())
                lamda_SMsimann = lamda_scale_SMsimann.get()
                probability_SMsimann = probability_scale_SMsimann.get()
                time_bound_SMsimann = int(time_bound_SMsimann_entry.get())
                fin_poex_SMsimann,Area_SMsimann,fin_dim_list_SMsimann, left_bot_SMsimann,Width_SMsimann,Height_SMsimann = SMfp_sim_ann.Stockmeyer_sim_ann_floorplanning(polish_SMsimann,dimension_SMsimann,lamda_SMsimann,probability_SMsimann,time_bound_SMsimann)
                return
            
            polish_expSMsimann_label = Label(slave, text='Enter Normalized Polish Expression: ' )
            polish_expSMsimann_label.grid(row=0, sticky=E)

            dimensionSMsimann_label = Label(slave, text='Enter Dimension list: ' )
            dimensionSMsimann_label.grid(row=1, sticky=E)

            lamda_SMsimann_label = Label(slave, text='Enter Lambda (recommended value :0.95, \n 0.95 implies temperature decreases by 5% for each iteration): ', justify=RIGHT)
            lamda_SMsimann_label.grid(row=2, sticky=E)
            
            probability_SMsimann_label = Label(slave, text='What should be the initial probability of \n accepting bad moves? (Recommended value:0.90 to 0.99)', justify=RIGHT)
            probability_SMsimann_label.grid(row=3, sticky=E)

            time_bound_SMsimann_label = Label(slave, text='Enter Maximum time bound in seconds \n (recommended value = 200 seconds)', justify=RIGHT)
            time_bound_SMsimann_label.grid(row=4, sticky=E)
            
            polish_expSMsimann_entry = Entry(slave, width=20)
            polish_expSMsimann_entry.grid(row=0,column=1, sticky=W, padx=5)
            polish_expSMsimann_entry.insert(0,'37H51V82HV4V6VH')
            
            dimensionSMsimann_entry = Entry(slave, width=50)
            dimensionSMsimann_entry.grid(row=1,column=1, sticky=W, padx=5)
            dimensionSMsimann_entry.insert(0,'[(2, 4), (1, 3), (3, 3), (3, 5), (3, 2), (5, 3), (1, 2), (2, 4)]')
            
            lamda_scale_SMsimann = Scale(slave, variable = DoubleVar(), from_=0, to=0.99, length=150, resolution =0.01, orient=HORIZONTAL)
            lamda_scale_SMsimann.grid(row=2, column=1, sticky=W, padx=5)
            lamda_scale_SMsimann.set(0.95)

            probability_scale_SMsimann = Scale(slave, variable = DoubleVar(), from_=0, to=0.99, length=150, resolution =0.01, orient=HORIZONTAL)
            probability_scale_SMsimann.grid(row=3, column=1, sticky=W, padx=5)
            probability_scale_SMsimann.set(0.97)    

            time_bound_SMsimann_entry = Entry(slave)
            time_bound_SMsimann_entry.grid(row=4, column=1, sticky=W, padx=5) 
            time_bound_SMsimann_entry.insert(0,'200')
            
            clear_comm = lambda:(polish_expSMsimann_entry.delete(0,'end'),dimensionSMsimann_entry.delete(0,'end'),lamda_scale_SMsimann.set(0.95),probability_scale_SMsimann.set(0.97),time_bound_SMsimann_entry.delete(0,'end'),)
            previous_comm = lambda:slave.destroy()
            row_numb = 5
            clear_ok_previousmenu(slave,run_SMsimann,clear_comm,previous_comm,row_numb)
        
        if varfp.get() == 'Seqence-Pair Method':
            def run_SP():
                sequence_SP = ast.literal_eval(sequenceSP_entry.get())
                dimension_SP = ast.literal_eval(dimensionSP_entry.get())
                Area_SP, Width_SP, Height_SP, Dim_SP, Left_Bot_Cor_SP, _, _, _, _ = SPFP.SequencePairFloorPlanning(sequence_SP,dimension_SP)
                return
            
            sequenceSP_label = Label(slave, text='Enter Sequence Pair: ' )
            sequenceSP_label.grid(row=0, sticky=E)

            dimensionSP_label = Label(slave, text='Enter Dimension dict: ' )
            dimensionSP_label.grid(row=1, sticky=E)

            sequenceSP_entry = Entry(slave, width=50)
            sequenceSP_entry.grid(row=0,column=1, sticky=W, padx=5)
            sequenceSP_entry.insert(0,"('17452638', '84725361')")
            
            dimensionSP_entry = Entry(slave, width=50)
            dimensionSP_entry.grid(row=1,column=1, sticky=W, padx=5)
            dimensionSP_entry.insert(0,"{'1':(2,4), '2':(1,3), '3':(3,3), '4':(3,5), '5':(3,2), '6':(5,3), '7':(1,2), '8':(2,4)}")

            clear_comm = lambda:(sequenceSP_entry.delete(0,'end'),dimensionSP_entry.delete(0,'end'))
            previous_comm = lambda:slave.destroy()
            row_numb = 3
            clear_ok_previousmenu(slave,run_SP,clear_comm,previous_comm,row_numb)
            


        if varfp.get() == 'Sequence-Pair Method-Simulated Annealing':
            def run_SPsimann():
                sequence_SPsimann = ast.literal_eval(sequenceSPsimann_entry.get())
                dimension_SPsimann = ast.literal_eval(dimensionSPsimann_entry.get())
                lamda_SPsimann = lamda_scale_SPsimann.get()
                probability_SPsimann = probability_scale_SPsimann.get()
                time_bound_SPsimann = int(time_bound_SPsimann_entry.get())
                best_SP,Area_SPsimanm,Width_SPsimann,Height_SPsimann,fin_dim_list_SPsimann,left_bot_SPsimann,_,_,_,_ = SPfp_sim_ann.SequencePair_sim_ann_floorplanning(sequence_SPsimann,dimension_SPsimann,lamda_SPsimann,probability_SPsimann,time_bound_SPsimann)
                return
            
            sequenceSPsimann_label = Label(slave, text='Enter Sequence Pair: ' )
            sequenceSPsimann_label.grid(row=0, sticky=E)

            dimensionSPsimann_label = Label(slave, text='Enter Dimension dict: ' )
            dimensionSPsimann_label.grid(row=1, sticky=E)

            lamda_SPsimann_label = Label(slave, text='Enter Lambda (recommended value :0.95, \n 0.95 implies temperature decreases by 5% for each iteration: ', justify=RIGHT)
            lamda_SPsimann_label.grid(row=2, sticky=E)
            
            probability_scale_SPsimann_label = Label(slave, text='What should be the initial probability of \n accepting bad moves? (Recommended value:0.90 to 0.99)', justify=RIGHT)
            probability_scale_SPsimann_label.grid(row=3, sticky=E)

            time_bound_SPsimann_label = Label(slave, text='Enter Maximum time bound in seconds \n (recommended value = 200 seconds)', justify=RIGHT)
            time_bound_SPsimann_label.grid(row=4, sticky=E)
            
            sequenceSPsimann_entry = Entry(slave, width=20)
            sequenceSPsimann_entry.grid(row=0,column=1, sticky=W, padx=5)
            sequenceSPsimann_entry.insert(0,"('17452638', '84725361')")
            
            dimensionSPsimann_entry = Entry(slave, width=50)
            dimensionSPsimann_entry.grid(row=1,column=1, sticky=W, padx=5)
            dimensionSPsimann_entry.insert(0,"{'1':(2,4), '2':(1,3), '3':(3,3), '4':(3,5), '5':(3,2), '6':(5,3), '7':(1,2), '8':(2,4)}")
            
            lamda_scale_SPsimann = Scale(slave, variable = DoubleVar(), from_=0, to=0.99, length=150, resolution =0.01, orient=HORIZONTAL)
            lamda_scale_SPsimann.grid(row=2, column=1, sticky=W, padx=5)
            lamda_scale_SPsimann.set(0.95)

            probability_scale_SPsimann = Scale(slave, variable = DoubleVar(), from_=0, to=0.99, length=150, resolution =0.01, orient=HORIZONTAL)
            probability_scale_SPsimann.grid(row=3, column=1, sticky=W, padx=5)
            probability_scale_SPsimann.set(0.97)    

            time_bound_SPsimann_entry = Entry(slave)
            time_bound_SPsimann_entry.grid(row=4, column=1, sticky=W, padx=5) 
            time_bound_SPsimann_entry.insert(0,'200')
            
            clear_comm = lambda:(sequenceSPsimann_entry.delete(0,'end'),dimensionSPsimann_entry.delete(0,'end'),lamda_scale_SPsimann.set(0.95),probability_scale_SPsimann.set(0.97),time_bound_SPsimann_entry.delete(0,'end'),)
            previous_comm = lambda:slave.destroy()
            row_numb = 5
            clear_ok_previousmenu(slave,run_SPsimann,clear_comm,previous_comm,row_numb)
            
    algorithmsfp = ['Stockmeyer Algorithm', 'Stockmeyer Algorithm-Simulated Annealing', 'Seqence-Pair Method','Sequence-Pair Method-Simulated Annealing']
    varfp = StringVar(root)
    varfp.set(algorithmsfp[0])  # default value
    varfp.trace("w", floorplanning_selection)
    menus[1] = OptionMenu(*(root, varfp) + tuple(algorithmsfp))
    menus[1].grid(row=8, sticky='ew')

def placement_algorithms():
    def placement_selection(*args):
        slave = Tk()

        if varpl.get() == 'Gordian Algorithm':
            def run_GOR():
                nets_GOR = ast.literal_eval(netlistGOR_entry.get())
                iopin_loc_GOR = ast.literal_eval(iopinlocGORentry.get())
                cell_size_dict_GOR = ast.literal_eval(cell_size_dictGOR_entry.get())
                chip_size_GOR = ast.literal_eval(chip_sizeGOR_entry.get())
                bal_factor_GOR = bal_factorGOR_scale.get()
                x_GOR,y_GOR = Gordp.Gordian_placement(nets_GOR,iopin_loc_GOR,cell_size_dict_GOR,chip_size_GOR,bal_factor_GOR)
                return

            netlistGOR_label = Label(slave, text='Enter Netlist: ' )
            netlistGOR_label.grid(row=0, sticky=E)
            
            iopinlocGOR_label = Label(slave, text='Enter IO Pin Loocation dictionary: ')
            iopinlocGOR_label.grid(row=1, sticky=E)

            cell_size_dictGOR_label = Label(slave, text='Enter Cell size:')
            cell_size_dictGOR_label.grid(row=2, sticky=E)

            chip_sizeGOR_label = Label(slave, text='Enter Chip size:')
            chip_sizeGOR_label.grid(row=3, sticky=E)

            bal_factorGOR_label = Label(slave, text='Choose Balance Factor (recommended:0.5):')
            bal_factorGOR_label.grid(row=4, sticky=E)            
            
            netlistGOR_entry = Entry(slave, width=125)
            netlistGOR_entry.grid(row=0,column=1, sticky=W, padx=5)
            netlistGOR_entry.insert(0,"{'n1':['w1','a','b'],'n2':['w2','a','e'],'n3':['w3','b','c','d'],'n4':['w4','c','d'],'n5':['a','z1','e','f'],'n6':['b','f'],'n7':['c','f','g'],'n8':['d','j'],'n9':['e','h'],'n10':['f','h','i'],'n11':['g','i','j'],'n12':['h','z2'],'n13':['i','z3'],'n14':['j','z4']}")
            
            iopinlocGORentry = Entry(slave, width=80)
            iopinlocGORentry.grid(row=1,column=1, sticky=W, padx=5)
            iopinlocGORentry.insert(0,"{'w1': (0,1),'w2': (0,2),'w3': (0,3),'w4': (1,4),'z1': (2,0),'z2': (3,0),'z3': (4,1),'z4': (4,2)}")
            
            cell_size_dictGOR_entry = Entry(slave, width=80)
            cell_size_dictGOR_entry.grid(row=2,column=1, sticky=W, padx=5)
            cell_size_dictGOR_entry.insert(0,"{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'f': 1, 'g': 1, 'h': 1, 'i': 1, 'j': 1 }")

            chip_sizeGOR_entry = Entry(slave)
            chip_sizeGOR_entry.grid(row=3, column=1, sticky=W, padx=5)
            chip_sizeGOR_entry.insert(0,'(4,4)')

            bal_factorGOR_scale = Scale(slave, variable = DoubleVar(), from_=0, to=0.9, length=150, resolution =0.1, orient=HORIZONTAL)
            bal_factorGOR_scale.grid(row=4, column=1, sticky=W, padx=5)
            bal_factorGOR_scale.set(0.5)
            
            clear_comm = lambda:(netlistGOR_entry.delete(0,'end'),iopinlocGORentry.delete(0,'end'),cell_size_dictGOR_entry.delete(0,'end'),chip_sizeGOR_entry.delete(0,'end'),bal_factorGOR_scale.set(0.5))
            previous_comm = lambda:slave.destroy()
            row_numb = 5
            clear_ok_previousmenu(slave,run_GOR,clear_comm,previous_comm,row_numb)
            
    algorithmspl = ['Min-Cut Algorithm','Gordian Algorithm', 'TimberWolf Algorithm']
    varpl = StringVar(root)
    varpl.set(algorithmspl[1])  # default value
    varpl.trace("w", placement_selection)
    menus[1] = OptionMenu(*(root, varpl) + tuple(algorithmspl))
    menus[1].grid(row=8, sticky='ew')
    
def routing_algorithms():
    def routing_selection(*args):
        slave = Tk()

        if varr.get() == 'L-Steiner Routing Algorithm':
            def run_LSTN():
                node_loc_dict_LSTN = ast.literal_eval(node_loc_dictLSTN_entry.get())
                LStnr.L_Steiner_routing(node_loc_dict_LSTN)
                return
            
            node_loc_dictLSTN_label = Label(slave, text='Enter Node location dictionary: ' )
            node_loc_dictLSTN_label.grid(row=0, sticky=E)           
            
            node_loc_dictLSTN_entry = Entry(slave, width=70)
            node_loc_dictLSTN_entry.grid(row=0,column=1, sticky=W, padx=5)
            node_loc_dictLSTN_entry.insert(0,"{'a': (1,5),'b': (4,4),'c': (2,8),'d': (3,7),'e': (6,9),'f': (7,5),'g': (8,1),'h': (10,2),'i': (10,10)}")
            
            clear_comm = lambda:node_loc_dictLSTN_entry.delete(0,'end')
            previous_comm = lambda:slave.destroy()
            row_numb = 5
            clear_ok_previousmenu(slave,run_LSTN,clear_comm,previous_comm,row_numb)
            
    algorithmsr = ['L-Steiner Routing Algorithm','A-tree Algorithm', 'Elmore Routing Tree Algorithm']
    varr = StringVar(root)
    varr.set(algorithmsr[0])  # default value
    varr.trace("w", routing_selection)
    menus[1] = OptionMenu(*(root, varr) + tuple(algorithmsr))
    menus[1].grid(row=8, sticky='ew')

algorithms = [clustering_algorithms, partitioning_algorithms, floorplanning_algorithms, placement_algorithms,routing_algorithms]



root = tk.Tk()

heading1 = Label(root, text="VLSI CAD ALGORITHMS-GUI")
heading1.bind("<Enter>", partial(font_config, heading1, "Times 25 bold"))
heading1.bind("<Leave>", partial(font_config, heading1, "Times 25 bold"))
heading1.grid(row=0)

tk.Label(root, text="""Choose which PHYSICAL DESIGN STEP you want to try:""", justify=tk.LEFT, padx=20).grid(row=1)

pd_steps = tk.IntVar()
pd_steps.set(6)  # initializing the radiobutton choices to none 

for val, physical_design_step in enumerate(physical_design_steps):
    tk.Radiobutton(root,
                   text=physical_design_step,
                   padx=20,
                   variable=pd_steps,
                   command=algorithms[val], value=val).grid(row = val+2, sticky=W)
    
clearscreen_button = Button(root, text='Clear Screen', command=cls)
clearscreen_button.grid(row=6, sticky=E)

bottom_text = Label(root, text="-Ganesh Prasad B K")
bottom_text.bind("<Enter>", partial(font_config, bottom_text, "Times 10 bold"))
bottom_text.bind("<Leave>", partial(font_config, bottom_text, "Times 10 italic"))
bottom_text.grid(row=9, sticky=E)

root.mainloop()
