import numpy as np
import pandas as pd
import random as rn

def node_type(nodeid):
    if nodeid < 4600:
        return(1)
    elif nodeid < 8000:
        return(2)
    elif nodeid < 8800:
        return(3)
    else:
        return(4)

def generate_tests(nodefile, timefile, mpi_rank=0):
    sentinels_old_index = np.genfromtxt(nodefile, dtype = int, delimiter = ",").tolist()
    timepoints = np.genfromtxt(timefile, delimiter = ",", dtype=int).tolist()
    better_tests = []
    for i in range(len(timepoints)):
        for j in timepoints[i]:
            better_tests.append((int(sentinels_old_index[i]), int(j)))
    better_tests = np.array(better_tests)
    path = "tests%i.txt" % mpi_rank
    np.savetxt(path, better_tests, delimiter="\t", fmt="%i")#, sep="\t")
    return path

def format_results(results, barn_lists, filename, mpi_rank):
    barn_sizes = np.genfromtxt("Synset/syndata%i/barn_size.txt" % (mpi_rank), dtype=int, delimiter=",").tolist()
    infected_capacity = [sum([barn_sizes[element] for element in ls]) for ls in barn_lists]
    df = pd.DataFrame(results, columns = ["start_node", "start_day", "detection_day", "n_infected", "detected"], dtype=int)
    df["start_type"] = df["start_node"].transform(node_type)
    df["infected_capacity"] = np.array(infected_capacity)
    df.to_csv(filename, index=False)
    return(df)