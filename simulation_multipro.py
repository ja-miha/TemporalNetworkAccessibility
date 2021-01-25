import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
##from mpi4py import MPI
from tools import format_results, read_tests_interval, read_tests_timepoints
import random as rn
import pandas as pd 
import sys
import multiprocessing as mp

rn.seed(rn.SystemRandom())
p_si = 0.5
p_false_neg = 0.1
start_timespan = 4*365 - 30
expert_detection = 30
n_runs = 1000

#n_array = int(sys.argv[1])

#comm = MPI.COMM_WORLD
#rank = comm.Get_rank()
#n_tasks = comm.Get_size()

#rank = rank + (n_array-1) * 8

parts = range(100)


def simulate(rank):
    if rank < 100:
        timepoints_path = "Synset/timepoint_13oct.txt"
        file_path = "Synset/syndata"+str(rank)+"/dataset.txt"
        sen_filenames = ["random_sentil", "degree_sentil", "betw_sentil", "kshel_sentil"]
        #sen_filenames = ["random_sentil"]
        for sen_filename in sen_filenames:
            
            sentinel_path = "Synset/syndata"+str(rank)+"/"+sen_filename+".txt"
            #sentinel_path = "randomplacement/"+sen_filename+str(rank)+".txt"

            start_time=time.time()
            AMS = AdjMatrixSequence(file_path, directed= True, write_label_file=True, mpi_rank=rank)#create Adjecency Matrix Object
            tests, mx = read_tests_timepoints(sentinel_path, timepoints_path, mpi_rank=rank)
            nodes = range(AMS.number_of_nodes)
            starts = rn.sample(range(mx), n_runs)

            results = []
            barn_lists = []
            for start in starts:
                inf_time = rn.choice(range(start_timespan))
                si_model = AMS.copy()
                si_model.dilute(p_si) 
                result, infected_barns = si_model.unfold_accessibility_with_tests(tests, start, start_time=inf_time, stop_time=expert_detection, p_false_negative=p_false_neg)
                results.append(result)
                barn_lists.append(infected_barns)

            format_results(results, barn_lists, "results/"+sen_filename+"_results_timepoint_13oct_"+str(rank)+".txt", rank)

            print(time.time()-start_time)

with mp.Pool(48)as P:
    P.map(simulate, parts)