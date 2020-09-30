from src.AdjacencyMatrixSequence import AdjMatrixSequence
file_path = "syndata1/syndata1.txt"
AMS = AdjMatrixSequence(file_path, directed=True)
AMS.dilute()
AMS.make_sir_model(0.5)