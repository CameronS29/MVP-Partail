import smtplib
from email.mime.text import MIMEText
from biorxiv import get_biorxiv
from rxivist import get_rxivist
from email_maker import generate_html, generate_static_html
import pandas as pd
import numpy as np
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import datetime

def load_queries():
    data_queries = []
    dirname = os.path.dirname(__file__)

    filename = os.path.join(dirname, 'resources', 'dazzling-lodge-273116-dff40eec25bf.json')

    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)

    gc = gspread.authorize(credentials)

    wks = gc.open_by_key('1detBGVGGIn1XvOWwHlgLYTiuVAkV2U_6rpNsO5uEBKg').sheet1

    cell_list = wks.range('A2:A30')

    #print(cell_list)

    #data = pd.read_csv(filenae)
    for cell in cell_list:
        if cell.value == '':
            break 
        data_queries.append(cell.value)

    return data_queries


if __name__ == '__main__':
    if datetime.datetime.today().weekday() != 4:
        sys.exit(0)
    dirname = os.path.dirname(__file__)
    data_queries = load_queries()

    #try:
    rxivist_df = get_rxivist(data_queries)
    dirname = os.path.dirname(__file__)
    rxcist_filename = os.path.join(dirname, 'output', 'rxivist.csv')
    rxivist_df.to_csv(rxcist_filename, sep=';', index=False)

    biorxiv_df = get_biorxiv(data_queries)

    #biorxiv_filename = os.path.join(dirname, 'output', 'pubmed.csv')
    #rxcist_filename = os.path.join(dirname, 'output', 'rxcist.csv')
    #biorxiv_df = pd.read_csv(biorxiv_filename, sep=';')
    #biorxiv_df.columns =["query", "title", "url", "abstract", "authors", "date", "downloads", "score", "journal"]

    #rxivist_df = pd.read_csv(rxcist_filename, sep=';')
    #rxivist_df.columns =["query", "title", "url", "abstract", "authors", "date", "downloads", "score", "journal"]


    # print('write static html')

    # generate_static_html(rxivist_df, biorxiv_df, data_queries)
    # print('writing email')



    # HTML_MESSAGE = generate_html(rxivist_df, biorxiv_df, data_queries)

    # email_password = 'anicepassword'
    # email_address = 'journal.emailer@gmail.com'
    # reciever = 'graham.cr.baker@gmail.com'
    # #reciever = 'ddshah27@gmail.com'
    

    # msg = MIMEText(HTML_MESSAGE, 'html')
    # msg['Subject'] = 'Journal Scrape'


    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # print('logging in...')
    # server.login(email_address, email_password)
    # server.sendmail(
    #     email_address, 
    #     reciever, 
    #     msg.as_string())

    # server.quit()



#    print('Email sent successfully')
    biorxiv_df.columns = ["query", "title", "url", "abstract", "authors", "date", "if", "score", "journal"]
    biorxiv_filename = os.path.join(dirname, 'output', 'pubmed.csv')

    biorxiv_df.to_csv(biorxiv_filename, sep=';', index=False)


    print('wrote files to csv')



    #except:
    #    email_password = 'anicepassword'
    #    email_address = 'journal.emailer@gmail.com'
    #    reciever = 'graham.cr.baker@gmail.com'

    #    errorHTML = '<h1>problem sending scraping records, check heroku logs</h1>'

    #    msg = MIMEText(errorHTML, 'html')
    #    msg['Subject'] = 'error running scraper'

    #    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #    print('logging in...')
    #    server.login(email_address, email_password)
    #    server.sendmail(
    #        email_address, 
    #        reciever, 
    #        msg.as_string())

    #    server.quit()





    
    

