#import pandas as pd 

#for i in range(100):
    #df = pd.read_csv("Synset/syndata"+str(i)+"/dataset.txt", delimiter=",", names=["source", "target", "day", "weight"])
    #df.to_csv("Synset/syndata"+str(i)+"/dataset.txt", sep = "\t", header=False, index = False)

#infile = open("Synset/timepoint_13oct.txt", "r")
#lines = []
#for line in infile:
 #   newline = str()
  #  for i in line:
   #     if i != "(" and i != ")":
    #        newline += i
    #lines.append(newline)
#infile.close()
#outfile = open("Synset/timepoint_13oct.txt", "w")
#for line in lines:
 #   outfile.write(line)
#outfile.close()

import os

src = "SDTC_based11M21/SDTC_sentil%i.txt"
dst = "Synset9Mar21/syndata%i/SDTC_sentil.txt"

for i in range(100):
    os.rename(src % i, dst % i)

src = "SDDC_based11M21/SDDC_sentil%i.txt"
dst = "Synset9Mar21/syndata%i/SDDC_sentil.txt"

for i in range(100):
    os.rename(src % i, dst % i)