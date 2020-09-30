#import pandas as pd 

#for i in range(100):
    #df = pd.read_csv("Synset/syndata"+str(i)+"/dataset.txt", delimiter=",", names=["source", "target", "day", "weight"])
    #df.to_csv("Synset/syndata"+str(i)+"/dataset.txt", sep = "\t", header=False, index = False)

infile = open("Synset/timepoint.txt", "r")
lines = []
for line in infile:
    newline = str()
    for i in line:
        if i != "(" and i != ")":
            newline += i
    lines.append(newline)
infile.close()
outfile = open("Synset/timepoint.txt", "w")
for line in lines:
    outfile.write(line)
outfile.close()