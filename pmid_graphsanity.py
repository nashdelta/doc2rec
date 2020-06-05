#import subprocess
#import random
#import json
#import pandas as pd

def pmid_to_citeography_string(pmid):
    """
    For a given pubmed ID, returns a comma separated list of all of the PMIDs of papers that cite it
    
    A comma-separated list of PMIDs can also be passed. Elink automatically removes redundant IDs.
    """

    result = subprocess.run(f"elink -db pubmed -id {pmid} -target pubmed -name pubmed_pubmed_citedin | \
                        efetch -format uid", 
                        capture_output = True,
                        text = True,
                        #check = True,
                        shell = True
                        )
    
    citationstring = result.stdout.replace('\n',',')
    
    return citationstring

def pmid_to_bibliography_string(pmid):
    """
    For a given pubmed ID, returns a dictionary all of the PMIDs of papers
    in the bibliography. Optional date filtering and subsampling.
    """
    result = subprocess.run(f"elink -db pubmed -id {pmid} -target pubmed -name pubmed_pubmed_refs | \
                        efetch -format uid", 
                        capture_output = True,
                        text = True,
                        #check = True,
                        shell = True
                        )
    
    bibstring = result.stdout.replace('\n',',')
    
    return bibstring

def pmid_graphsanity(pmid):
    """
    This program:
    1) Given a pubmed UID seed, generates a primary_citeography
    2) From all the PMIDs in the primary_citeography, generates a primary_bibliography.
    3) From all the PMID in the primary_bibliography, generates a secondary_citeography.
    4) From all the PMID in the secondary citeography, generates a secondary_bibliography
    5) For every PMID in the secondary_citeography, generates a tertiary_citeography
    6) For every PMID in the secondary_bibliography, generates a quaternary_citeography
    """
    
    #1 Given a pubmed UID seed, generates a primary_citeography
    primary_citeography = pmid_to_citeography_string(pmid)
    print(f"primary_citeography is {primary_citeography}")
    
    #2 from all the PMIDs in the primary_citeography, generates a primary_bibliography.
    primary_bibliography = pmid_to_bibliography_string(primary_citeography)
    print(f"primary_bibliography is {primary_bibliography}")
    
    #3 From all the PMIDs in the primary_bibliography, generates a secondary_citeography.
    secondary_citeography = pmid_to_citeography_string(primary_bibliography)
    print(f"secondary_citeography is {secondary_citeography}")
    
    #4 From all the PMID in the secondary citeography, generates a secondary_bibliography
    #secondary_bibliography = pmid_to_bibliography_string(secondary_citeography)
    
    #return primary_bibliography #, secondary_citeography
    
pmid_graphsanity('21219465')
