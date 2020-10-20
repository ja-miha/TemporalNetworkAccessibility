from src.AdjacencyMatrixSequence import AdjMatrixSequence
import time
start_time = time.time()
file_path = "syndata1/syndata1.txt"
AMS = AdjMatrixSequence(file_path, directed=True)
print(time.time()-start_time)
result = AMS.unfold_accessibility_single_node(200)
print(result)
print(time.time()-start_time)
AMS.dilute()
result = AMS.unfold_accessibility_single_node(200)
print(result)
print(time.time()-start_time)
AMS.make_sir_model_single_node(0.01, 200, keep_track_of_recovered=True)
print(AMS.sir_history)
result = AMS.unfold_accessibility_single_node(200)
print(result)
print(time.time()-start_time)