import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence


AMS = AdjMatrixSequence("syndata1/syndata1.txt", directed=True)
start_time = time.time()
inf, rec = AMS.unfold_accessibility_sir_random_recovery_single_node(0.005)
print(inf)
print(rec)


print(time.time()-start_time)