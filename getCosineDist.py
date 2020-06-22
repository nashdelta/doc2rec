import numpy
from sklearn.metrics.pairwise import cosine_similarity
import os
import argparse

ap = argparse.ArgumentParser(description = "For list of pairs of PMIds gets cosine distances")
ap.add_argument("-f", help = "Tab separated file with PMIDs as first two columns", required = True)
ap.add_argument("-d", help = "Directory where vectors for abstracts are stored", required = True)
opts = ap.parse_args()

PMIDsFileName = opts.f
DataFolder = opts.d

VecPostifix = "_bert-base-uncased.tsv"

for PMIDLine in open(PMIDsFileName):
    LineValues = PMIDLine[:-1].split()
    PMId1VectorFileName = DataFolder + "/" + LineValues[0] + VecPostifix
    PMId2VectorFileName = DataFolder + "/" + LineValues[1] + VecPostifix


    if os.path.exists(PMId1VectorFileName) and os.path.exists(PMId2VectorFileName):
        for Line in open(PMId1VectorFileName):
            PMId1Vec = numpy.asarray([float(x) for x in Line.split("\t")])
        for Line in open(PMId2VectorFileName):
            PMId2Vec = numpy.asarray([float(x) for x in Line.split("\t")])

        print(PMIDLine[:-1] + "\t" + str(cosine_similarity(numpy.array([PMId1Vec]), numpy.array([PMId2Vec]))[0][0]))
    else:
        print(PMIDLine[:-1] + "\t" + "AbsentAbstract")



