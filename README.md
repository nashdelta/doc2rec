# doc2rec

## AIMS:

### 1) Investigate semantic relationships within the pubmed citation network.

i) Construct 5 graphical representations of local pubmed citation networks centered on "seed" articles. a) edge length is the direct citation distance (e.g. an article in the citeography of an article in the citeography of the seed has edge length 2). The graph is iteratively built as depicted below:

![](/graphImage1.jpg)

Distances are signed with an article in the bibliography connected to the seed with edge length -1. b) edge length is the ratio of the union of the bibliographies of the seed and the target and the intersection c) the same ratio with each reference weighted by the inverse of the size of its citeography d) edge length is the ratio of the union of the citeographies of the seed and the target and the intersection e) each citing article is weighted by the size of its bibliography. The graphs are iteratively built as depicted below (c/d shown: get bibliography of seed, get citeographies of bibliography, get bibliographies of citeographies and the size of their respective citeographies, calculate ratios).

relationship between the cosine similarities of the state-of-the-art vector representations of pairs of pubmed abstracts (assumed to be BioBERT)
![](/graphImage1.jpg)
![](/graphImage2.jpg)

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
