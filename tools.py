import numpy as np
import pandas as pd

def read_sentinels(sentinel_path):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*7 : sentinels for i in range(1, 4)}
    return(sentinels_dic)

def format_results(results, filename):
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    new_to_old = {new : old for old, new in old_to_new_file}
    results_ls = []
    for dic in results:
        ls = [dic.items()[0][1][0], dic.items()[0][1][1]]#!!!!! nur eine zeile pro simulation.
        results_ls = results_ls + ls
    df = pd.DataFrame(results_ls, columns = ["day", "n_infected"], dtype=int)
    df.to_csv(filename, index=False)
    return(df)