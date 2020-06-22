import subprocess
import argparse
from transformers import *
import torch
import os
import numpy

ap = argparse.ArgumentParser(description = "For given list of PMIDs collects abstracts and processed BERT output for these abstracts")
ap.add_argument("-f", help = "File with PMIDs", required = True)
ap.add_argument("-d", help = "Directory to store abstracts", required = True)
opts = ap.parse_args()

PMIDsFileName = opts.f
AbstractsFolder = opts.d

## bert initialization
model_class = BertModel
tokenizer_class = BertTokenizer
pretrained_weights = 'bert-base-uncased'

config = BertConfig.from_pretrained(pretrained_weights, output_hidden_states=True)
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights, config = config)

## data processing
PMIDs = [x[:-1] for x in open(PMIDsFileName).readlines()]

for PMID in PMIDs:
    AbstractStorageFileName = AbstractsFolder + "/" + PMID + ".txt"
    if os.path.exists(AbstractStorageFileName):
        continue

    subprocess.call("esummary -db pubmed -format abstract -id " + PMID +
                    " -mode xml | xtract -pattern Article -element AbstractText > " + AbstractStorageFileName, shell = True)
    Abstract = "".join([x[:-1] for x in open(AbstractStorageFileName).readlines()])
    if Abstract != "":
        input_ids = torch.tensor([tokenizer.encode(Abstract, add_special_tokens=True, max_length = 512)])
        outputs = model(input_ids)

        ResVec = numpy.asarray(numpy.mean(numpy.array(outputs[2][3][0].detach()), axis=0))
        ResFileName = PMID + "_" + pretrained_weights + ".tsv"
        with open(AbstractsFolder + "/" + ResFileName, "w") as ResFile:
            ResFile.write("\t".join([str(x) for x in ResVec]))


