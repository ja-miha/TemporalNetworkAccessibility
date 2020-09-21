import pandas as pd 

for i in range(100):
    df = pd.read_csv("Synset/syndata"+str(i)+"/dataset.txt", delimiter=",", names=["source", "target", "day", "weight"])
    df.to_csv("Synset/syndata"+str(i)+"/dataset.txt", sep = "\t", header=False, index = False)