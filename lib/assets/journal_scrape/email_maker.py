
import pandas as pd
import numpy as np
import os
from datetime import datetime



def unpack_df(df):
    # return array of objects
    # top 3
    to_ret = []

    for index, row in df.iterrows():

        if index == 3:
            break

        obj = {
            'title': row['title'], 
            'url': row['url'], 
            'abstract': row['abstract'], 
            'authors': row['authors'], 
            'date': row['date'], 
            'downloads': row['downloads'], 
            'score': row['score'], 
            'journal': row['journal']
        }

        to_ret.append(obj)


    while len(to_ret) != 3:
        to_ret.append({'title': 'filler'})


    return to_ret

def unpack_df_for_static(df):
    # return array of objects
    # all
    to_ret = []

    for index, row in df.iterrows():

        obj = {
            'title': row['title'], 
            'url': row['url'], 
            'abstract': row['abstract'], 
            'authors': row['authors'], 
            'date': row['date'], 
            'downloads': row['downloads'], 
            'score': row['score'],
            'journal': row['journal']
        }

        to_ret.append(obj)


    while len(to_ret) < 50:
         to_ret.append({'title': 'filler'})


    return to_ret




def generate_col(obj, database, doc_type):

    if obj['title'] == 'filler':
        return '<td></td>'

    html = '<div class="col"><td>'
    html += '<div class="everything-else-head">'
    html += '<h4 class="title">Title: ' + obj['title'] + '</h4>'
    html += '<p><a href="' + obj['url'] + '">Link</a></p>'

    if isinstance(obj['date'], str):
        html += '<p><b>Date:</b> ' + obj['date'] + '</p>'
    else:
        html += '<p><b>Date:</b> ' + obj['date'].strftime("%m/%d/%Y") + '</p>'

    html += '<p><b>Authors:</b> ' + obj['authors'] + '</p>'

    if 'PubMed' in database:
        html +=  '<p><b>Journal:</b> ' + str(obj['journal']) + '</p>'
        html += '<p><b>IF (7 or above):</b> ' + str(obj['downloads']) + '</p>'
    else:
        html += '<p><b>Downloads:</b> ' + str(obj['downloads']) + '</p>'

    if doc_type == 'static':
         html += '<p><b>Relevance Score:</b> ' + str(obj['score']) + '</p>'
    


    html += '</div>'
    html += '<div class="everything-else-tail"><p><b>Abstract:</b> ' + obj['abstract'] + '</p></div>'
    
    ## see more
    # html += '<p><a href="https://journal-scrape.herokuapp.com/' + link_generator(obj['query']) + '">See more</a></p>'
    html += '</td></div>'

    return html



def link_generator(query):
    t = datetime.now()
    today = t.strftime('%m-%d')
    print(today + '-' + query.strip().lower().replace('"', '').replace(' ', '-') + '.html')
    return today + '-' + query.strip().lower().replace('"', '').replace(' ', '-') + '.html'


def generate_static_html(rxivist_df, biorxiv_df, data_queries):
    for query in data_queries:
        html = '<html><head><link rel="stylesheet" type="text/css" href="css/style.css"></head>'
        html += '<body>'

        html += '<div id="main"><h1>Scignal</h1></div>'
        html += ' <div class="container">'

        html += '<div class="row"><div class="search"><h2>All Results for : ' + query + '</a></h2></div>'
        html += '<table>'
  

        rxivist_df_sub = rxivist_df[rxivist_df['query'] == query]
        rxivist_df_sub = rxivist_df_sub.reset_index(drop=True)
        rxivist = unpack_df_for_static(rxivist_df_sub)
        biorxiv_df_sub = biorxiv_df[biorxiv_df['query'] == query]
        biorxiv_df_sub = biorxiv_df_sub.reset_index(drop=True)
        biorxiv = unpack_df_for_static(biorxiv_df_sub)
        html += '<tr><td class="head"><h3>BioRxiv</h3></td><td class="head"><h3>PubMed</h3></td></tr>'
        
        for i, article in enumerate(rxivist):

            if rxivist[i]['title'] == biorxiv[i]['title']:
                break
            html += '<tr>'  
            html += '<div class="row">'
            
            html += generate_col(rxivist[i], 'BioRxiv', 'static')
            html += generate_col(biorxiv[i], 'PubMed', 'static')
            html == '</div>'
            html += '</tr>'

        

        html += '</table>'

        
        ## closes row
        html += '</div>'
        html += '<hr>'
        html += '</div>'

        html += '</body></html>'



        dirname = os.path.dirname(__file__)
        output = os.path.join(dirname, 'output', link_generator(query))


        with open(output, "w") as file:
            file.write(html)



def generate_html(rxivist_df, biorxiv_df, data_queries):
    html = '<html><head><style>  table {table-layout: fixed; width: 100% ;} td {text-align: center;}</style></head>'
    html += '<body>'

  
    for query in data_queries:
        html += '<div class="row"><h1>Search: ' + query + ' <a href="https://scignal.herokuapp.com/' + link_generator(query) + '">(See all results)</a></h1>'
        html += '<table>'

        rxivist_df_sub = rxivist_df[rxivist_df['query'] == query]
        rxivist_df_sub = rxivist_df_sub.reset_index(drop=True)
        rxivist = unpack_df(rxivist_df_sub)

        biorxiv_df_sub = biorxiv_df[biorxiv_df['query'] == query]
        biorxiv_df_sub = biorxiv_df_sub.reset_index(drop=True)
        biorxiv = unpack_df(biorxiv_df_sub)

        html += '<tr><td><h2>BioRxiv</h2></td></tr>'
        for i, article in enumerate(rxivist):
            html += '<tr>'
            html += generate_col(rxivist[i], 'BioRxiv', 'email')
            html += '</tr>'

        html += '<tr><td><h2>PubMed</h2></td></tr>'
        for i, article in enumerate(rxivist):

            html += '<tr>'
            html += generate_col(biorxiv[i], 'PubMed', 'email')
            html += '</tr>'


        

        html += '</table>'

        
        ## closes row
        html += '</div>'
        html += '<hr>'

        html += '</body></html>'


    return html











# search term

#pubmed results         #BioRxiv results
#title
#link
#date

#authors
#abstract

#IF / #downloads
#Relvance 










