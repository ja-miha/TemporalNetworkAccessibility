import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import format_results, read_sentinels
import random as rn
import pandas as pd 

rn.seed(rn.SystemRandom())
p_si = 0.8
p_false_positive = 0.1

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

file_path = "Synset/syndata"+str(rank)+"/dataset.txt"
sentinel_path = "Synset/syndata"+str(rank)+"/betw_sentil.txt"
#file_path = "syndata1/syndata1.txt"
#sentinel_path = "syndata1/degreebs_sentil.txt"
#df = pd.read_csv(file_path, delimiter=",", names=["source", "target", "day", "weight"])
#df.to_csv(file_path, sep = "\t", header=False, index = False)

start_time=time.time()
AMS = AdjMatrixSequence(file_path, directed= True, write_label_file=True, mpi_rank=rank)#create Adjecency Matrix Object
sentinels= read_sentinels(sentinel_path, mpi_rank=rank)
nodes = range(AMS.number_of_nodes)
starts = rn.sample(nodes, 1000)

results = []
for start in starts:
    inf_time = rn.choice(range(365))
    si_model = AMS.copy()
    si_model.dilute(p_si)
    result = si_model.unfold_accessibility_with_sentinels(sentinels, start, start_time=inf_time, stop_at_detection = True, p_false_positive=p_false_positive)
    results.append(result)

format_results(results, "results/results_degreebs_sentil_"+str(rank)+".txt")

print(time.time()-start_time)