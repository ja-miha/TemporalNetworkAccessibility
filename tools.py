import numpy as np
import pandas as pd

def read_tests_interval(sentinel_path, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*365 : sentinels for i in range(1, 4)}
    return(sentinels_dic)

def read_tests_timepoints(sentinel_path, timepoint_path, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",").tolist()#read sentinel file and convert to new index
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    timepoints = np.genfromtxt(timepoint_path, delimiter = ",", dtype=int).tolist()#read timepoints file
    test_dic = {i : [] for i in range(5*365)}#create dictionary {time : [premises_to test]}
    for i in range(len(timepoints)):
        for t in timepoints[i]:
            test_dic[t].append(sentinels[i])
    removal_list = []#remove times with no tests
    for test in test_dic:
        if not test_dic[test]:
            removal_list.append(test)
    for test in removal_list:
        test_dic.pop(test)
    return(test_dic)

def node_type(node, new_to_old):
    nodeid = new_to_old[node]
    if nodeid < 4600:
        return(1)
    elif nodeid < 8000:
        return(2)
    elif nodeid < 8800:
        return(3)
    else:
        return(4)


def format_results(results, filename, mpi_rank):
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", dtype=int, delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    new_to_old = {new : old for old, new in old_to_new_file}
    df = pd.DataFrame(results, columns = ["start_type", "start_day", "detection_day", "n_infected", "detected"], dtype=int)
    df["start_type"] = df["start_type"].transform(lambda n: node_type(n, new_to_old))
    df.to_csv(filename, index=False)
    return(df)