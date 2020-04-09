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

# BERT
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')

# DistilBERT
# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
# model = DistilBertModel.from_pretrained('distilbert-base-cased')

#Note: To use TensorFlow 2.0 versions of the models, simply prefix the class names with 'TF',
# e.g. `TFRobertaModel` is the TF 2.0 counterpart of the PyTorch model `RobertaModel`

# SciBERT uncased
# tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
# model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')

# SciBERT cased
tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_cased')
model = AutoModel.from_pretrained('allenai/scibert_scivocab_cased')

# Note: cased/uncased refers to the vocabulary used, uncased is generally recommeded: https://github.com/allenai/scibert

# Encode text
input_ids = torch.tensor([tokenizer.encode("Here is some text to encode", add_special_tokens=True)])
# Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for the model.
with torch.no_grad():
    last_hidden_states = model(input_ids)[0]  # Models outputs are now tuples
    print(last_hidden_states)
    print(len(last_hidden_states[0][0]))