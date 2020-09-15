import numpy as np
import pandas as pd

def read_sentinels(sentinel_path):
    sentinels_old_index = np.genfromtxt(sentinel_path, dtype = int, delimiter = ",")
    sentinels_old_index = sentinels_old_index.tolist()
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    old_to_new = {old : new for old, new in old_to_new_file}
    sentinels = [old_to_new[sentinel] for sentinel in sentinels_old_index if sentinel in old_to_new]
    sentinels_dic = {i*365 : sentinels for i in range(1, 4)}
    return(sentinels_dic)

def format_results(results):
    old_to_new_file = np.genfromtxt("oldindex_matrixfriendly.txt", delimiter="\t")
    old_to_new_file = old_to_new_file.tolist()
    new_to_old = {new : old for old, new in old_to_new_file}
    results_ls = []
    for dic in results:
        ls = [[new_to_old[sent], dic[sent][0], dic[sent][1]] for sent in dic]
        results_ls = results_ls + ls
    df = pd.DataFrame(results_ls, columns = ["sent", "day", "n_infected"])
    result_by_sent = { i : j.drop("sent", axis = 1).to_numpy().tolist() for i, j in df.groupby("sent") }
    df = df.sort_values("sent", axis=0)
    df.to_csv("results.txt", index=False)
    return(result_by_sent)