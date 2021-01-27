import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import generate_tests, format_results_better
import random as rn
import pandas as pd 
import sys

rn.seed(rn.SystemRandom().random())
p_si = 0.5
p_false_neg = 0.1
start_timespan = 4*365 - 30
expert_detection = 30
n_runs = 10
n_nets = 100

sen_filenames = ["random_sentil", "degree_sentil", "betw_sentil", "kshel_sentil"]
timepoints_path = "Synset/timepoint_13oct.txt"
network_pattern = "Synset/syndata%i/dataset.txt"
sentinel_pattern = "Synset/syndata%i/%s.txt"

n_array = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

rank = rank + (n_array-1) * 8

if rank < n_nets:
    network_path = network_pattern % rank
    si_model = AdjMatrixSequence(network_path, directed= True, write_label_file=True, mpi_rank=rank)
    for sen_filename in sen_filenames:
        sentinel_path = sentinel_pattern % (rank, sen_filename)

        # for measuring time
        start_time=time.time()

        # make list of tests
        testfile = generate_tests(sentinel_path, timepoints_path, rank)

        # generate AdjMatrixSequence Object
        #si_model = AdjMatrixSequence(network_path, directed= True, tests=testfile, mpi_rank=rank)#create Adjecency Matrix Object
        si_model.add_tests(testfile)

        # choose start nodes randomly
        mx = si_model.newindex(8800)
        starts = rn.sample(range(mx), n_runs)


        results = []
        barn_lists = []
        for start in starts:
            inf_time = rn.choice(range(start_timespan))
            result, infected_barns = si_model.unfold_accessibility_with_tests_better(start_node=start, start_time=inf_time, stop_time=expert_detection, p_false_negative=p_false_neg, p_si=p_si)
            results.append(result)
            barn_lists.append(infected_barns)

        format_results_better(results, barn_lists, "results/"+sen_filename+"_results_timepoint_13oct_"+str(rank)+"_better.txt", rank)

        print(time.time()-start_time)