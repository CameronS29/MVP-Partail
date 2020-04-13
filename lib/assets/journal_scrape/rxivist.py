import requests
import json
import csv
import collections
import pandas as pd
import numpy as np
from relevance_scorer import get_relevance_score
import time



def get_rxivist(data_queries):

    api_endpoint = 'https://api.rxivist.org/v1/papers'


    all_data = []
    print (data_queries)
    for search_term in data_queries:
        
        data = {
            'q': search_term,
            'metric': 'downloads', 
            'page_size': '25'
        }
        r = requests.get(api_endpoint, params=data)

        print(r.content)
        if r.ok == False:
            results = []
        else:
            results = json.loads(r.content)['results']

        category = []

        for res in results:
       
            title = res['title']
            url = res['biorxiv_url']

            abstract_split = res['abstract'].split('.')
            abstract_full = res['abstract']
            abstract = abstract_split[0] + '. ' + abstract_split[1] + '.'
            
            authors = ''

            if len(res['authors']) == 1:
                authors = res['authors'][0]['name']
            else:
                authors = res['authors'][0]['name'] + ' ... ' + res['authors'][-1]['name']
           

            published = res['first_posted']

            downloads = res['metric']
            score = get_relevance_score(title, abstract_full, search_term)

            category.append([search_term, title, url, abstract, authors, published, downloads, score, "missing"])

        all_data.append(pd.DataFrame(category, columns =["query", "title", "url", "abstract", "authors", "date", "downloads", "score", "journal"]))
        time.sleep(4)

    for cat in all_data:
        cat.sort_values(['score', 'downloads'], ascending=[False, False], inplace=True)

    return pd.concat(all_data).reset_index(drop=True)
    
    
    
    



