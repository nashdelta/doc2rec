import pandas as pd
import subprocess

def pmid_to_citeography(pmid):
    """
    For a given pubmed ID, returns a dictionary all of the PMIDs of papers that cite it  
    """
    citation_dict = {}
    result = subprocess.run(f"elink -db pubmed -id {pmid} -target pubmed -cited | \
                        efetch -format uid", 
                        capture_output = True,
                        text = True,
                        #check = True,
                        shell = True
                        )
    
    citationlist = list(result.stdout.split())
    for citation in citationlist:
        citation_dict[citation] = pmid
        
    return citation_dict

def pmid_to_bibliography(pmid, mindate=1900, maxdate=2099):
    """
    For a given pubmed ID, returns a dictionary all of the PMIDs of papers
    in the bibliography. Optional date filtering.
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
        
    return bib_dict

def pubmed_adam_and_eve(seed, max_iterations):
    """
    Given a pubmed seed UID, generate a citeography.
    For each PMID in the citeography, generate a child citeography.
    Repeat.
    Outputs a dictionary of dictionaries in the form of 
    
    {'PMID1': 
        {'citation1': 'PMID1',
        'citation2': 'PMID1'},
    'PMID2'': {'citation1': 'PMID2'},
    'PMID3': {'citation1': 'PMID3'},
    ...
    }
    
  
    """
    
    #initialize a list of pmids to do 
    tbd_pmids = [seed]
    
    #List of PMIDS that have been checked
    done_pmids = []
    
    #initialize an empty dictionary to store results
    citeography_dict = {}
    #bibliography_dict = {}
    
    #Keep things small.
    i = 0
    while i < max_iterations:
        #loop through the list
        for pmid in tbd_pmids:
            print(f"Getting citations from {pmid}")
            #Returns a dictionary of {citation : pmid}
            citation_dict = pmid_to_citeography(pmid)

            #If the paper has been cited
            if len(citation_dict) > 0:
                #Add it to the citeography_dictionary
                #citeography_dict[pmid] = citation_dict
                citeography_dict = {**citeography_dict, **citation_dict}

                #Add the citations to the tbd_set
                for key in citation_dict.keys():
                    #Don't add pmids already checked
                    if key in done_pmids:
                        pass
                    else:
                        tbd_pmids.append(key)

            #Add the pmid to the done_list
            done_pmids.append(pmid)

            i += 1
            
            #Break if the length of the list is too long
            if i > max_iterations:
                break
        


            print(f"Done with {pmid}")
            #print(f"The citeography_dict now looks like {citeography_dict}")
            #print(f"The done_pmids list now looks like {done_pmids}")
            #print(f"The tbd_pmids set now looks like {tbd_pmids}")
            print(f"Round #{i} done")
            num_pmids_left = len(tbd_pmids)
            print(f"There are {num_pmids_left} more PMIDS to go")
            print("========================")
            
    return citeography_dict

def citeography_to_df(dictionary):
    """
    Takes a two-column dictionary and reformats it to two-column dataframe
    that looks like this:
    
    PubmedID Citation
    1234    citation1,citation2,citation3
    5789    citation1,
    ...
    """
    df = pd.DataFrame.from_dict(dictionary, 
                                orient='index', 
                                columns = ['pubmed_id']
                               )
    df2 = (df.reset_index() #Make it a three column table of "entry index pubmed_id"
             .rename(columns={'index' : 'citation'}) #rename the index column to "citation"
             .groupby('pubmed_id')['citation'] #for every pubmed ID, get the citations
             .apply(','.join) #Turn them into a comma-separated list
             .reset_index()  #This turns it back into a dataframe
          )
    
    return df2

#Kira's 2015  nature micro review on CRISPR
citeography_dict = pubmed_adam_and_eve('26411297', 5000)
df = citeography_to_df(citeography_dict)
df.to_csv('Kira_citeography.csv', index = False)
