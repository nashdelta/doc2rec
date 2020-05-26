# doc2rec: /panfs/pan1.be-md.ncbi.nlm.nih.gov/pmid2rec

## Aims:

### 1) Investigate semantic relationships within the pubmed citation network.

i) Construct 5 graphical representations of local pubmed citation networks centered on "seed" articles. a) edge length is the direct citation distance (e.g. an article in the citeography of an article in the citeography of the seed has edge length 2). The graph is iteratively built as depicted below selecting a single representative next-next neighbor etc.:

![](/graphImage1.jpg)

Distances are signed with an article in the bibliography connected to the seed with edge length -1. b) edge length is the ratio of the union of the bibliographies of the seed and the target and the intersection c) the same ratio with each reference weighted by the inverse of the size of its citeography d) edge length is the ratio of the union of the citeographies of the seed and the target and the intersection e) each citing article is weighted by the size of its bibliography. The graphs are iteratively built as depicted below (b/c shown: get bibliography of seed, get citeographies of bibliography, get bibliographies of citeographies and the size of their respective citeographies, calculate ratios).

![](/graphImage2.jpg)

ii) Retrive the cosine similarities of the state-of-the-art (assumed to be BioBERT) vector representations of pairs of pubmed abstracts.

iii) Compare graph edges and cosine similarities. Open questions: How does the cosine similarity scale with edge length? How wide is the distribution? How much does it vary by seed, by key-word? In general, how much semantic information is provided by a citation?

### 2) Train a binary classifier to predict connections to existing abstracts from a "novel" abstract

i) Generate (+/-) training data based on combinations of cosine similarities and graph distances. (-) training data is not a problem because the goal is not to predict new connections between existing abstracts.

ii) Fine tune BERT starting from the pretrained BioBERT weights for a binary classification problem given two vectors (pairs of abstracts) as input. Output is related/unrelated.

### 3) Train a binary classifier to predict novel connections AMONG existing abstracts

i) As in 2), generate (+/-) training data based on combinations of cosine similarities and graph distances. (-) training data is a challenge. Need to identify pairs of connected but semantically unrelated abstracts (e.g. in the bibliography but low cosine similarity). Not clear what is the best case.

ii) Same as 2)

### 3) Aggregate abstracts by first/corresponding author

i) Construct graphs with authors as nodes in the same manner as was done for 1)

ii) Train a binary classifier to predict connections among authors in the same manner as was done for 2/3

## Progress:

### HAVE:
Basic function to construct cosine similarities

Function returning graph given necessary pmids

### NEED:
Function gathering necessary pmids for given seed/graph structure (currently have case a) more or less)

Improvement of vectorization routine - optimization of hidden layer representation/vector normalization/review of test data

Compilation of pieces into parent script with basic analysis (e.g. scatter plots of edge length vs. cosine similarity)

## References:
### Language models
Original [BERT](https://arxiv.org/abs/1810.04805) paper, GitHub [page](https://github.com/google-research/bert)

[SciBERT](https://arxiv.org/abs/1903.10676), GitHub [page](https://github.com/allenai/scibert)

[BioBERT](https://arxiv.org/abs/1901.08746), GitHub [page](https://github.com/dmis-lab/biobert)

Huggingface (Transformers) [documentation](https://huggingface.co/transformers/) and list of all directly supported [models](https://huggingface.co/models?)



### Related BERT implementations
Pairwise document classification from Wikipedia [articles](https://arxiv.org/abs/2003.09881)

Use of BERT encodings of paper tiles for research paper [recommendation](http://ceur-ws.org/Vol-2431/paper2.pdf)

### Other relevant work

Crowdsourced semi-automated search for analogies between [research papers](https://dl.acm.org/doi/abs/10.1145/3274300)

Representation of scholarly research in a [knowledge graph](https://dl.acm.org/doi/abs/10.1145/3360901.3364435)

Citation intent [classification](https://www.aclweb.org/anthology/N19-1361.pdf)
