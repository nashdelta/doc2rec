import subprocess
import random
import json
from pathlib import Path

def pmid_to_citeography(pmid, sample_size=0):
    """
    For a given pubmed ID, returns a dictionary all of the PMIDs of papers that cite it
    Optional random sampling on the number of citations returned
    """
    citation_dict = {}
    result = subprocess.run(f"elink -db pubmed -id {pmid} -target pubmed -name pubmed_pubmed_citedin | \
                        efetch -format uid", 
                        capture_output = True,
                        text = True,
                        #check = True,
                        shell = True
                        )
    
    citationlist = list(result.stdout.split())
    
    for citation in citationlist:
            citation_dict[citation] = pmid  
    
    if sample_size > 0 and sample_size < len(citationlist):
        citation_dict.clear()
    
        random_citations = random.sample(citationlist, sample_size)

        for citation in random_citations:
            citation_dict[citation] = pmid    
    
    return citation_dict

def pmid_to_bibliography(pmid, sample_size=0, mindate=1900, maxdate=2099):
    """
    For a given pubmed ID, returns a dictionary all of the PMIDs of papers
    in the bibliography. Optional date filtering and subsampling.
    """
    bib_dict = {}
    result = subprocess.run(f"elink -db pubmed -id {pmid} -target pubmed -cites | \
                        efilter -mindate {mindate} -maxdate {maxdate} -datetype PDAT | \
                        efetch -format uid", 
                        capture_output = True,
                        text = True,
                        #check = True,
                        shell = True
                        )
    
    biblist = list(result.stdout.split())
    
    for bib in biblist:
        bib_dict[bib] = pmid
    
    if sample_size > 0 and sample_size < len(biblist):
        bib_dict.clear()
    
        random_bibs = random.sample(biblist, sample_size)

        for bib in random_bibs:
            bib_dict[bib] = pmid    
    
    return bib_dict

def pubmed_third_degree_burn(seed):
    """
    This function:
    1) Given a pubmed UID, generates a primary_citeography, (up to 10 max)
    2) For each PMID in the primary_citeography, generates a second_citeography (1 max).
    3) For each PMID in the second_citeography, generates a tertiary_citeography (1 max).
    Repeats for the bibliography.
    """
    
    #Get the citations
    primary_citeography = pmid_to_citeography(seed, 100)
    
    secondary_citeography = {}
    for primary_citation in primary_citeography.keys():
        secondary_citeography.update(pmid_to_citeography(primary_citation, 1))
        
    tertiary_citeography = {}
    for secondary_citation in secondary_citeography.keys():
        tertiary_citeography.update(pmid_to_citeography(secondary_citation, 1))
     
    #Get the bibliographies
    primary_bibliography = pmid_to_bibliography(seed, 100)
        
    secondary_bibliography = {}
    for primary_bib in primary_bibliography.keys():
        secondary_bibliography.update(pmid_to_bibliography(primary_bib, 1))
        
    tertiary_bibliography = {}
    for secondary_bib in secondary_bibliography.keys():
        tertiary_bibliography.update(pmid_to_bibliography(secondary_bib, 1))
    
    #Spit out the result
    result_dict = {'primary_citeography' : primary_citeography,
                   'secondary_citeography' : secondary_citeography, 
                   'tertiary_citeography' : tertiary_citeography,
                   'primary_bibliography' : primary_bibliography,
                   'secondary_bibliography' : secondary_bibliography,
                   'tertiary_bibliography' : tertiary_bibliography,
                  }
    
    with open(str(seed) + '.json', 'w') as fp:
        json.dump(result_dict, fp, indent=4)
        
def json_to_table(jsonfile):
    
    with open(jsonfile) as f:
        data = json.load(f)

        #We want a comma-separate list of keys from each dictionary
        primary_cite_str = (",".join(data['primary_citeography'].keys()))
        secondary_cite_str = (",".join(data['secondary_citeography'].keys()))
        tertiary_cite_str = (",".join(data['tertiary_citeography'].keys()))
        primary_bib_str = (",".join(data['primary_bibliography'].keys()))
        secondary_bib_str = (",".join(data['secondary_bibliography'].keys()))
        tertiary_bib_str = (",".join(data['tertiary_bibliography'].keys()))

    p = Path(jsonfile)
    PMID = p.stem
    
    with open(PMID + '.tab', 'w') as outfile:
        print(primary_cite_str, 
              primary_bib_str, 
              secondary_cite_str,
              secondary_bib_str,
              tertiary_cite_str,
              tertiary_bib_str,
              sep = '\t',
              file = outfile
             )

with open ('crispr_abstracts.tab') as f:
    accession_list = []
    for line in f:
        try:
            accession, other = line.split(sep = '\t', maxsplit=1)
            accession_list.append(accession)
        except ValueError:
            pass

for accession in accession_list:
    pubmed_third_degree_burn(accession)
    
#!esearch -db pubmed -query crispr[Mesh] | efetch -format xml | xtract -pattern PubmedArticle -element MedlineCitation/PMID -element AbstractText -block Author -sep " " -tab "|" -element Initials,LastName > crispr_abstracts.tab
