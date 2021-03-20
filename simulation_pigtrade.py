import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import generate_tests, format_results
import random as rn
import pandas as pd 
#import sys

rn.seed(rn.SystemRandom().random())
p_si = 0.5
p_false_neg = 0.1
start_timespan = 4*365 - 30
expert_detection = 30
n_runs = 10000


sen_filenames = ["random", "degree", "betweenness", "kshel", "closeness"]
timepoints_path = "pigtrade/timepoints_pigtrade.txt"
network_path = "pigtrade/pig_trade_2011-2014_temporalnetwork.csv"
sentinel_pattern = "pigtrade/%s_sentil_pigtrade.txt"

#n_array = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

si_model = AdjMatrixSequence(network_path, directed= True, write_label_file=True, rank=rank)
startnodes = range(si_model.number_of_nodes())
for sen_filename in sen_filenames:
    sentinel_path = sentinel_pattern % sen_filename

    # for measuring time
    start_time=time.time()

    # make list of tests
    testfile = generate_tests(sentinel_path, timepoints_path)

    # generate AdjMatrixSequence Object
    #si_model = AdjMatrixSequence(network_path, directed= True, tests=testfile, rank=rank)#create Adjecency Matrix Object
    si_model.add_tests(testfile)

    # choose start nodes randomly
    starts = rn.sample(startnodes, n_runs)

    results = []
    barn_lists = []
    for start in starts:
        inf_time = rn.choice(range(start_timespan))
        result, infected_barns = si_model.unfold_accessibility_with_tests(start_node=start, start_time=inf_time, stop_time=expert_detection, p_false_negative=p_false_neg, p_si=p_si, reindex=False, dereindex=False)
        results.append(result)
        barn_lists.append(infected_barns)

    #format_results(results, barn_lists, "results/"+sen_filename+"_results_timepoint_13oct_"+str(rank)+".txt", rank)

    print(time.time()-start_time)
    print(results[-1])