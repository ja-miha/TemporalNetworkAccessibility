import time
from src.AdjacencyMatrixSequence import AdjMatrixSequence

start_time = time.time()

AMS = AdjMatrixSequence("syndata1/syndata1.txt", directed=True)
inf, rec = AMS.unfold_accessibility_sir_constant_recovery(50)#, start_node=3604)
print(inf)
print(rec)


print(time.time()-start_time)