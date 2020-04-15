import time
import requests
import datetime
import re
import os
import csv
import importlib
from urllib.parse import quote
from pprint import pprint
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from relevance_scorer import get_relevance_score

from bs4 import BeautifulSoup

# So many pubmed libaries
from Bio import Entrez #pubmed search

from companysearch import metalist as companylist
from companysearch import LinkedInResult
from configGeneric import config

#default params
PATENT_TIME_DELAY=0.1
RESULTS_LIMIT=100
ENTREZ_TIME_DELAY=0.1


# USPTO tool that's kludgy af
# from uspto.pbd.tasks import UsptoPairBulkDataDownloader

# config = importlib.util.find_spec("config")
# if config is None:
#     config = importlib.util.find_spec("configGengit eric")

if config["ncbi_api_key"]:
    os.environ["NCBI_API_KEY"] = config["ncbi_api_key"]
    # # Tell pubmed who we be
    Entrez.email = config["email"]
    Entrez.api_key = config["ncbi_api_key"]
    ENTREZ_TIME_DELAY=0.101

#have to import these after setting environment variables
from pubmed_lookup import PubMedLookup, Publication
import metapub

class ScimagoRanking:
    def __init__(self, issn):
        self.issn=issn.replace('-','')
        self.get_rankings_per_issn()

    def get_rankings_per_issn(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'resources', 'scimagojr.csv')

        with open(filename,"r") as f:
            rdr = csv.reader(f,delimiter=';')
            found_issn=False
            for row in rdr:
                if self.issn in row[4]:
                    found_issn=True
                    self.sjr=row[5].replace(',','.')
                    self.twoyearif=row[13].replace(',','.')
                    break
        if not found_issn:
            self.sjr='0.0'
            self.twoyearif='0.0'

class PMCSearchResult:

    def __init__(self, pubmed_id, pmc_id, url, title, author_list, journal, issn, pub_date, abstract, relevance_score, relevance_score_rough):
        self.pubmed_id=pubmed_id
        self.pmc_id=pmc_id
        self.url=url
        self.pmc_url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}/".format(pmc_id)
        self.title=title
        self.parse_authors(author_list)
        self.journal=journal
        self.issn=issn
        self.pub_date=pub_date.date() #datetime -> date
        self.abstract=abstract
        self.relevance_score=relevance_score #could do this inside of this function
        self.relevance_score_rough=relevance_score_rough #could do this inside of this function
        self.rankings=ScimagoRanking(self.issn)

    def parse_authors(self, author_list):
        authors_as_list=[]
        for author in author_list:
            author_name='{} {}'.format(author.fore_name, author.last_name)
            authors_as_list.append(author_name)
        self.authors=', '.join(authors_as_list)

# Was tempting to write a PatentSearchResult class, but the pypatent.Patent class is sufficient here

class PatentSearchResult:

    def __init__(self, patent_data, relevance_score, relevance_score_rough):
        self.patent_data = patent_data
        self.relevance_score = relevance_score
        self.relevance_score_rough = relevance_score_rough


def now_as_str():
    return datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M')


# Lil helper function for Entrez efetch/esummary queries
#
def pmc_id_list_to_string(pmc_ids):
    pmc_ids_string=','.join(pmc_ids)
    return pmc_ids_string

  

    #for easy reference, remove when possible
    # search_term0 = "\"hematopoietic stem cells\" AND CRISPR AND AAV AND (\"sickle cell disease\" OR \"beta thalassemia\")"
    # search_term1 = "(\"sickle cell disease\" OR \"beta thalassemia\") AND (\"gene therapy\" OR \"genome editing\" OR \"mRNA therapy\")"
    # search_term2 = "\"cystic fibrosis\" AND (\"gene therapy\" OR \"genome editing\" OR \"mRNA therapy\")"

#search_term7 = "(\"sickle cell disease\" OR \"beta thalassemia\" OR \"beta-thalassemia\") AND (\"gene therapy\" OR \"genome editing\" OR \"mRNA therapy\" OR (\"hematopoietic stem cells\" AND CRISPR AND (AAV OR "adeno-associated virus"))"


# "(\"sickle cell disease\" OR \"beta thalassemia\") AND (\"gene therapy\" OR \"genome editing\" OR \"mRNA therapy\")"

# TODO: This function is the embodied definition of hard coded duct tape.
# Replace it as soon as possible
#
def search_term_text_check(search_term, text):
  #  print(search_term)
  #  print(text)
    if text is None: #empty text handler
        return False
    if isinstance(text, list): #some objects come through as lists - particularly patent claims/desc
        text=' '.join(text)
    if "thalassemia" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "sickle cell disease" in text.lower()
        check2 = "thalassemia" in text.lower()
        check3 = "gene therapy" in text.lower()
        check4 = "genome editing" in text.lower()
        check5 = "mrna therapy" in text.lower()
        check6 = "hematopoietic" in text.lower()
        check7 = "crispr" in text.lower()
        if ((check1 or check2) and (check3 or check4 or check5 or (check6 and check7))):
            return True
        else:
            return False
    if "cystic fibrosis" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "cystic fibrosis" in text.lower()
        check2 = "gene therapy" in text.lower()
        check3 = "genome editing" in text.lower()
        check4 = "mrna therapy" in text.lower()
        if (check1 and (check2 or check3 or check4)):
            return True
        else:
            return False
    if "cellular reprogramming" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "cellular reprogramming" in text.lower()
        check2 = "ageing" in text.lower()
        check3 = "aging" in text.lower()
        check4 = "mtor" in text.lower()
        check5 = "senescence" in text.lower()
        check6 = "lysosome" in text.lower()
        if (check1 and (check2 or check3) and (check4 or check5 or check6)):
            return True
        else:
            return False
    if "regulatory T cells" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "regulatory t cells" in text.lower()
        check2 = "autoimmune" in text.lower()
        check3 = "cancer" in text.lower()
        if (check1 and (check2 or check3)):
            return True
        else:
            return False



    search_term9 = "\"cellular reprogramming\" AND (ageing OR aging) OR mTOR OR senescence OR lysosome"
    search_term10 = "\"cellular reprogramming\" AND ((ageing OR aging) OR (mTOR OR senescence OR lysosome))"
    search_term11 = "\"cellular reprogramming\" AND (ageing OR aging) AND (mTOR OR senescence OR lysosome)"
    search_term12 = "\"regulatory T cells\" AND (autoimmune OR cancer)" 





# TODO: This function is the embodied definition of hard coded duct tape.
# Replace it as soon as possible
#
def search_term_rough_score(search_term, text):
  #  print(search_term)
  #  print(text)
    if text is None: #empty text handler
        return 0
    if isinstance(text, list): #some objects come through as lists - particularly patent claims/desc
        text=' '.join(text)
    text=text.lower()
    search_term_derezzed = re.sub(r'[^a-zA-Z\d\s:]', '', search_term.lower())
    all_words=set(search_term_derezzed.split(' '))
    all_words.discard('and')
    all_words.discard('or')
    #print(all_words)
    total_score=0.0
    for word in all_words:
        if word in text:
            total_score+=1.0
    normalized_score = total_score / len(all_words)
    return normalized_score



def get_relevance_score_pmc(article_raw, search_term):
    relevance_score=0
    highest_possible=4 + 2 + 1
    in_title = 4 if search_term_text_check(search_term, article_raw.title) else 0
    in_abstract = 2 if search_term_text_check(search_term, article_raw.abstract) else 0
    in_text = 1 #full text not available via current means
    relevance_score = in_title+in_abstract+in_text
    normalized_score=round(relevance_score/highest_possible,2)
    return normalized_score



def get_relevance_score_patent(patent_object, search_term):
    relevance_score=0
    highest_possible = 8 + 4 + 2 + 1
    in_title = 8 if search_term_text_check(search_term, patent_object.title) else 0
    in_abstract = 4 if search_term_text_check(search_term, patent_object.abstract) else 0
    in_claims = 2 if search_term_text_check(search_term, patent_object.claims) else 0
    in_description = 1 if search_term_text_check(search_term, patent_object.description) else 0
    relevance_score = in_title + in_abstract + in_claims + in_description
    normalized_score=round(relevance_score/highest_possible,2)
    return normalized_score




def get_relevance_score_rough_pmc(article_raw, search_term):
    relevance_score=0
    highest_possible = 4 + 2 + 1
    in_title = 4 * search_term_rough_score(search_term, article_raw.title)
    in_abstract = 2 * search_term_rough_score(search_term, article_raw.abstract)
    in_text = 1 #full text not available via pmc
    relevance_score = in_title+in_abstract
    normalized_score=round(relevance_score/highest_possible,2)
    return normalized_score



def get_relevance_score_rough_patent(patent_object, search_term):
    relevance_score=0
    highest_possible = 8 + 4 + 2 + 1
    in_title = 8 * search_term_rough_score(search_term, patent_object.title)
    in_abstract = 4 * search_term_rough_score(search_term, patent_object.abstract)
    in_claims = 2 * search_term_rough_score(search_term, patent_object.claims)
    in_description = 1 * search_term_rough_score(search_term, patent_object.description)
    relevance_score = in_title + in_abstract + in_claims + in_description
    normalized_score=round(relevance_score/highest_possible,2)
    return normalized_score




# Query that returns a list of IDs
# 
def pubmed_central_search_return_ids(search_term, results_limit, min_date):
    min_date_as_str=min_date.strftime('%Y/%m/%d')
    max_date_as_str=datetime.datetime.now().strftime('%Y/%m/%d')
    handle = Entrez.esearch(db="pmc", 
                            retmax=results_limit, 
                            datetype='pdat', 
                            mindate=min_date_as_str, 
                            maxdate=max_date_as_str,
                            term=search_term)
    record = Entrez.read(handle)
    handle.close()
    time.sleep(0.4) #rate limit
    pmc_ids=record['IdList']
    return pmc_ids

# Get a PubMed Central article and put it in the PMCSearchResult class
# Sort of kludgy
# These can also be pulled in bulk using the Entrez efetch or esummary functions
# Unfortunately, esummary doesn't include abstracts :( 
# And efetch seems to have some issues with PMC where Entrez parse/read can't
# use the output. I've tried debugging it to no avail.
#
# There are more fields in the metapub article object if we ever need them
#
# The timedelta subtraction is because the metapub package seems to add a day
# 
def get_pmc_article(pmc_id, search_term):
    
    fetch = metapub.PubMedFetcher()
    try:
        article_raw = fetch.article_by_pmcid(pmc_id) 
       
      #  print(vars(article_raw)) #for debugging
        relevance_score = get_relevance_score_pmc(article_raw, search_term) or 0
        relevance_score_rough = get_relevance_score_rough_pmc(article_raw, search_term) or 0
        authors=[]
        article = PMCSearchResult(
                    pubmed_id=article_raw.pmid,
                    pmc_id=article_raw.pmc,
                    url=article_raw.url,
                    title=article_raw.title,
                    author_list=article_raw.author_list,
                    journal=article_raw.journal,
                    issn=article_raw.issn,
                    pub_date=article_raw.history['pubmed']-datetime.timedelta(days=1), 
                    abstract=article_raw.abstract,
                    relevance_score=relevance_score,
                    relevance_score_rough=relevance_score_rough
                      )
    except metapub.exceptions.MetaPubError:
        #TODO: Find some better means of retrieval for articles without a pubmed ID (creates metapub error)
        article = PMCSearchResult(pubmed_id="Unknown - Retrieval Error, only exists in PMIC",
                      pmc_id=pmc_id,
                      url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}/".format(pmc_id),
                      title="Unknown - Retrieval Error",
                      author_list=[],
                      issn="Unknown - Retrieval Error",
                      journal="Unknown - Retrieval Error",
                      pub_date=datetime.datetime(1980,1,1), 
                      abstract="Unknown - Retrieval Error",
                      relevance_score=0,
                      relevance_score_rough=0
                      )
    except:
        article = ""    return article

# Pull all of the pubmed article IDs and then retrieve the article for each.
#
def get_pubmed_articles(search_term, results_limit, min_date):
    pmc_ids=pubmed_central_search_return_ids(search_term, results_limit, min_date)
    time.sleep(ENTREZ_TIME_DELAY) #rate limiter per pubmed api - with an api key this can be 10/s instead of 3/s    
    pmc_articles=[]
    for pmc_id in pmc_ids:
        time.sleep(3)
        article=get_pmc_article(pmc_id, search_term)
        print("Fetching PubMed Article: {}, {}, {}".format(article.title, article.relevance_score, article.relevance_score_rough))
        if (float(article.rankings.twoyearif) >= 7.0):
            pmc_articles.append(article)

    pmc_articles.sort(key=lambda x:(x.relevance_score, x.relevance_score_rough, float(x.rankings.twoyearif)), reverse=True)

    
    return pmc_articles





def get_biorxiv(data_queries): 
    results_limit=RESULTS_LIMIT
    
    min_date=datetime.datetime.now()-relativedelta(years=1)
   
    all_data = []
    
    for i, search_term in enumerate(data_queries):

        requests.get('https://scignal.herokuapp.com/downloads.html')
        print('\n\n\n\n\n\n\n\n\n')

        print('ping......' + search_term)
        print('\n\n\n\n\n\n\n\n\n')

        pubmed_articles = get_pubmed_articles(search_term, results_limit, min_date)

        category = []
        for article in pubmed_articles:
            
            score = get_relevance_score(article.title, article.abstract, search_term)

            if article.title == None:
                continue

            if article.abstract == None:
                continue

            abstract_split = article.abstract.split('.')
            
            if len(abstract_split) == 1:
                abstract = abstract_split[0]
            else:
                abstract = abstract_split[0] + '. ' + abstract_split[1] + '.'


            if len(abstract) > 300:
                abstract = abstract[:300] + ' ....'

            authors_split = article.authors.split(',')

            if len(authors_split) == 1:
                authors = authors_split[0]
            else:
                authors = authors_split[0] + ' ... ' + authors_split[-1]

            
            category.append([search_term, article.title, article.url, abstract, authors, article.pub_date, article.rankings.twoyearif, score, article.journal])
        
        print('sleeeeeping...')
        time.sleep(60)
            
        
        all_data.append(pd.DataFrame(category, columns =["query", "title", "url", "abstract", "authors", "date", "downloads", "score", "journal"]))

    for cat in all_data:
        cat.sort_values(['score', 'downloads'], ascending=[False, False], inplace=True)

    return pd.concat(all_data).reset_index(drop=True)
    
