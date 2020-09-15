import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI
from tools import format_results, read_sentinels

file_path = "syndata1/syndata1right_format.txt"
sentinel_path = "syndata1/degreebs_sentil.txt"
p_si = 0.9

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

if rank == 0:
    start_time=time.time()
    AMS = AdjMatrixSequence(file_path, directed= True, write_label_file=True)#create Adjecency Matrix Object
    sentinels= read_sentinels(sentinel_path)
    nodes = np.arange(AMS.number_of_nodes)
else:
    AMS = None
    sentinels = None
    nodes = None

AMS = comm.bcast(AMS)
sentinels = comm.bcast(sentinels)
nodes = comm.bcast(nodes)
starts = nodes.tolist()

print("starting")

results = []
for start in starts:
    si_model = AMS.copy()
    si_model.dilute(p_si)
    result = si_model.unfold_accessibility_with_sentinels(sentinels, start)
    results.append(result)

if rank == 0: format_results(results)

if rank == 0: print(time.time()-start_time)