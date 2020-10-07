from src.AdjacencyMatrixSequence import AdjMatrixSequence
file_path = "syndata1/syndata1.txt"
AMS = AdjMatrixSequence(file_path, directed=True)
result = AMS.unfold_accessibility_single_node(200)
print(result)
AMS.dilute()
result = AMS.unfold_accessibility_single_node(200)
print(result)
AMS.make_sir_model(0.5)
result = AMS.unfold_accessibility_single_node(200)
print(result)