import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence
import numpy as np 
from mpi4py import MPI

file_path = "syndata1/syndata1right_format.txt"
sentinel_path = "syndata1/degreebs_sentil.txt"
p_si = 0.9

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_tasks = comm.Get_size()

if rank == 0:
    start_time=time.time()
    AMS = AdjMatrixSequence(file_path, directed= True, write_label_file=True)#create Adjecency Matrix Object
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*365 : sentinels for i in range(1, 4)}
    nodes = np.arange(AMS.number_of_nodes)
    #nodes = np.array_split(nodes, n_tasks)
else:
    AMS = None
    sentinels_dic = None
    nodes = None

AMS = comm.bcast(AMS)
sentinels_dic = comm.bcast(sentinels_dic)
nodes = comm.bcast(nodes)
starts = nodes.tolist()

print("starting")

results = []
for start in starts:
    si_model = AMS.copy()
    si_model.dilute()
    result = si_model.unfold_accessibility_with_sentinels(sentinels_dic, start)
    results.append(result)

if rank == 0: print(time.time()-start_time)

