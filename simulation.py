import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import format_results, read_tests_interval, read_tests_timepoints
import random as rn
import pandas as pd 
import sys

rn.seed(rn.SystemRandom())
p_si = 0.3
p_false_neg = 0.1

n_array = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

rank = rank + (n_array-1) * 8

if rank < 100:
    file_path = "Synset/syndata"+str(rank)+"/dataset.txt"
    sen_filenames = ["degree_sentil", "betw_sentil", "kshel_sentil"]
    for sen_filename in sen_filenames:
        sentinel_path = "Synset/syndata"+str(rank)+"/"+sen_filename+".txt"
        timepoints_path = "Synset/timepoint.txt"
        #file_path = "syndata1/syndata1.txt"
        #sentinel_path = "syndata1/kshell_sentil.txt"
        #df = pd.read_csv(file_path, delimiter=",", names=["source", "target", "day", "weight"])
        #df.to_csv(file_path, sep = "\t", header=False, index = False)

        start_time=time.time()
        AMS = AdjMatrixSequence(file_path, directed= True, write_label_file=True, mpi_rank=rank)#create Adjecency Matrix Object
        tests = read_tests_timepoints(sentinel_path, timepoints_path, mpi_rank=rank)
        nodes = range(AMS.number_of_nodes)
        starts = rn.sample(nodes, 1000)

        results = []
        for start in starts:
            inf_time = rn.choice(range(365))
            si_model = AMS.copy()
            si_model.dilute(p_si) 
            result = si_model.unfold_accessibility_with_tests(tests, start, start_time=inf_time, p_false_negative=p_false_neg)
            results.append(result)

        format_results(results, "results/"+sen_filename+"_results_timepoints_"+str(rank)+".txt")

        print(time.time()-start_time)