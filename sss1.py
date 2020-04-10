# Block 0 imports necessary packages
import numpy
# Basic scientific computing package

import sklearn
# Basic ML package

import torch
# https://en.wikipedia.org/wiki/PyTorch:
# "PyTorch provides two high-level features:
# Tensor computing (like NumPy) with strong acceleration via graphics processing units (GPU)
# Deep neural networks built on a tape-based autodiff system"

from transformers import *
# https://huggingface.co/transformers/:
# "Transformers...provides general-purpose architectures (BERT,... DistilBert,...) for Natural Language Understanding
# (NLU) and Natural Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep
# interoperability between TensorFlow 2.0 and PyTorch."

# Load tokenizer/model of choice
# tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
# model = model_class.from_pretrained(pretrained_weights)

#Check here for a list of all available models: https://huggingface.co/models?
# BERT
# pretrained_weights = 'bert-base-uncased'

# DistilBERT
# pretrained_weights = 'distilbert-base-cased'

#Note: To use TensorFlow 2.0 versions of the models, simply prefix the class names with 'TF',
# e.g. `TFRobertaModel` is the TF 2.0 counterpart of the PyTorch model `RobertaModel`

# SciBERT uncased/cased
# pretrained_weights = 'allenai/scibert_scivocab_uncased'
# pretrained_weights = 'allenai/scibert_scivocab_cased'
# Note: cased/uncased refers to the vocabulary used, uncased is generally recommeded: https://github.com/allenai/scibert

# BioBERT v1.1 (+PubMed 1M)
tokenizer = BertTokenizer.from_pretrained('monologg/biobert_v1.1_pubmed')
model = BertModel.from_pretrained('monologg/biobert_v1.1_pubmed', output_hidden_states=True)
# Note: output_hidden_states=True is used for getting hidden state activations and not
# callable for all model_class. The suggested model class, AutoModelWithLMHead, does
# not support this, but the weights can be loaded with BertModel anyway.

# Note: Three other sets of pretrained weights are available: BioBERT v1.0 (+PubMed 200K),
# BioBERT v1.0 (+PubMed 200K +PMC 270K), BioBERT v1.0 (+PMC 270K) some of which are also
# directly available through huggingface.

# Block 1 takes the three example abstract texts [a1, a1.1 (nearly identical to a1), a2],
# loads them as strings stripping newline characters (not sure if we should be doing this),
# tokenizes the strings, and feeds the tokenized input to the language model using the
# predefined weights to get network activations as a vector representation of the text.
# The recommended layer (used for bert-as-service) which for this step would be
# equivalent is the second to last hidden layer (because the last hidden layer is to biased
# to training target loss functions) and averaged over all words. The output is a matrix
# of dimension num words x 768 (num tokens). Then the cosine similarity between these
# output vectors is calculated

# Read text as strings
with open('a1.txt', 'r') as file:
    a1 = file.read().replace('\n', '')  # remove newline characters
with open('a1.1.txt', 'r') as file:
    a1_1 = file.read().replace('\n', '')
with open('a2.txt', 'r') as file:
    a2 = file.read().replace('\n', '')

# Tokenize strings
# Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for the model.
input_id1 = torch.tensor([tokenizer.encode(a1, add_special_tokens=True)])
input_id1_1 = torch.tensor([tokenizer.encode(a1_1, add_special_tokens=True)])
input_id2 = torch.tensor([tokenizer.encode(a2, add_special_tokens=True)])

# Get activations from predefined weights torch.no_grad() means no training
# Note: model()[2] should have length 13, 12 BERT layers plus plus the embedding
# output. model()[2][3] should be the second to last hidden layer of length 1
# model()[2][3][0] should be of length num words and each element e.g.
# model()[2][3][N] should be of length 768, the number of tokens.
# Note: I don't know that model()[2][*3*] will be the most successful feature.
# Note: the .detach() function needs to be called to retrieve the matrix from
# the feature without a connection to the gradient backend framework.
with torch.no_grad(): # Take tokenized text as input for the language model using pre-defined weights
                      # to get network activations as a vector representation of the text and take
                      # the mean over all words
                      v1 = numpy.mean(numpy.array(model(input_id1)[2][3][0].detach()), axis=0)
                      v1_1 = numpy.mean(numpy.array(model(input_id1)[2][3][0].detach()), axis=0)
                      v2 = numpy.mean(numpy.array(model(input_id2)[2][3][0].detach()), axis=0)

#Calculate cosine similarities between all pairs of texts
textSim = sklearn.metrics.pairwise.cosine_similarity(numpy.array([v1,v2,v1_1]), Y=None, dense_output=True)
print(textSim)

