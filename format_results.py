import numpy as np
import pandas as pd

def format_results(results):
    results_ls = []
    for dic in results:
        ls = [[sent, dic[sent][0], dic[sent][1]] for sent in dic]
        results_ls = results_ls + ls
    df = pd.DataFrame(results_ls, columns = ["sent", "day", "n_infected"])
    result_by_sent = { i : j.drop("sent", axis = 1).to_numpy().tolist() for i, j in df.groupby("sent") }
    return(result_by_sent)