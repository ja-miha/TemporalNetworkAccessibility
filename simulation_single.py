import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import generate_tests, format_results
import random as rn
import pandas as pd 
import sys

rn.seed(rn.SystemRandom().random())
p_si = 0.5
p_false_neg = 0.1
start_timespan = 4*365 - 180
expert_detection = 180
n_runs = 1000
n_nets = 100
first_slaughterhouse_id = 8800 # to exclude slaughterhouses from start nodes. it is assumed the node ids are ordered by type, with slaughterhouses coming last

sen_filenames = ["results_180d/results_9Mar21_180dkmeans_833_0.5_1-30_180_10_initial"]
timepoints_path = "Synset9Mar21/timepoints_17Mar21.txt"
network_pattern = "Synset9Mar21/syndata%i/dataset.txt"
sentinel_path = "jobst_sentinels_6/syndata0/kmeans_833_0.5_1-30_180_10_0.5_1_10000.txt"
barnsize_pattern = "Synset9Mar21/syndata%i/barn_size.txt"
sen_filename = "kmeans_833_0.5_1-30_180_10_0.5_1_10000"

n_array = int(sys.argv[1])

#comm = MPI.COMM_WORLD
#rank = comm.Get_rank()
#n_tasks = comm.Get_size()

rank = n_array #rank + (n_array-1) * 8 # n_tasks

if rank < n_nets:
    network_path = network_pattern % rank
    si_model = AdjMatrixSequence(network_path, directed= True, write_label_file=True, rank=rank)


    # for measuring time
    start_time=time.time()

    # make list of tests
    testfile = generate_tests(sentinel_path, timepoints_path, rank)

    # generate AdjMatrixSequence Object
    #si_model = AdjMatrixSequence(network_path, directed= True, tests=testfile, rank=rank)#create Adjecency Matrix Object
    si_model.add_tests(testfile)

    # choose start nodes randomly
    mx = si_model.newindex(first_slaughterhouse_id)
    starts = rn.choices(range(mx), k=n_runs) # rn.sample(range(mx), n_runs)


    results = []
    barn_lists = []
    for start in starts:
        inf_time = rn.choice(range(start_timespan))
        result, infected_barns = si_model.unfold_accessibility_with_tests(start_node=start, start_time=inf_time, stop_time=expert_detection, p_false_negative=p_false_neg, p_si=p_si)
        results.append(result)
        barn_lists.append(infected_barns)

    format_results(results, barn_lists, barnsize_pattern % rank, "results/"+"results_9Mar21_180d"+sen_filename+"_"+str(rank)+".txt")

    print(time.time()-start_time)