import numpy as np
import pandas as pd
import random as rn
from collections import defaultdict

def read_tests_interval(sentinel_path, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*365 : sentinels for i in range(1, 4)}
    mx = old_to_new[8800]
    return sentinels_dic, mx

def read_tests_timepoints(sentinel_path, timepoint_path, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",").tolist()#read sentinel file and convert to new index
    if sentinels_old_index[-1] == -1:
        sentinels_old_index.pop()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel]  if sentinel in old_to_new else -1 for sentinel in sentinels_old_index]
    timepoints = np.genfromtxt(timepoint_path, delimiter = ",", dtype=int).tolist()#read timepoints file
    #test_dic = {t : [] for t in range(5*365)}#create dictionary {time : [premises_to_test]}
    test_dic = defaultdict(list)
    for i in range(len(timepoints)):
        if sentinels[i] > -1:
            for t in timepoints[i]:
                test_dic[t].append(sentinels[i])
        else:
            replacement_sentinel = rn.choice(list(old_to_new.values()))
            for t in timepoints[i]:
                test_dic[t].append(replacement_sentinel)
    #removal_list = []#remove times with no tests
    #for test in test_dic:
        #if not test_dic[test]:
            #removal_list.append(test)
    #for test in removal_list:
        #test_dic.pop(test)
    mx = old_to_new[8800]
    return test_dic, mx

def node_type(nodeid):
    if nodeid < 4600:
        return(1)
    elif nodeid < 8000:
        return(2)
    elif nodeid < 8800:
        return(3)
    else:
        return(4)

def format_results(results, barn_lists, filename, mpi_rank):
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    new_to_old = {new : old for old, new in old_to_new_file}
    barn_sizes = np.genfromtxt("Synset/syndata%i/barn_size.txt" % (mpi_rank), dtype=int, delimiter=",").tolist()
    infected_capacity = [sum([barn_sizes[new_to_old[element]] for element in ls]) for ls in barn_lists]
    df = pd.DataFrame(results, columns = ["start_node", "start_day", "detection_day", "n_infected", "detected"], dtype=int)
    df["start_node"] = df["start_node"].transform(lambda n: new_to_old[n])
    df["start_type"] = df["start_node"].transform(node_type)
    df["infected_capacity"] = np.array(infected_capacity)
    df.to_csv(filename, index=False)
    return(df)