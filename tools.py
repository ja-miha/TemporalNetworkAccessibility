import numpy as np
import pandas as pd

def read_sentinels(sentinel_path, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly"+str(mpi_rank)+".txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*365 : sentinels for i in range(1, 4)}
    return(sentinels_dic)

def format_results(results, filename):
    #old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    #old_to_new_file = old_to_new_file.tolist()
    #new_to_old = {new : old for old, new in old_to_new_file}
    results_ls = []
    for dic in results:
        ls = [[dic[sent][0], dic[sent][1]] for sent in dic]
        if ls:
            results_ls.append(ls[0])
    df = pd.DataFrame(results_ls, columns = ["day", "n_infected"], dtype=int)
    df.to_csv(filename, index=False)
    return(df)