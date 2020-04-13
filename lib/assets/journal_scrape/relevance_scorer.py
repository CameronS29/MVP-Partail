

import re

data_queries = [
    '"in vivo gene editing"',
    '"chimeric antigen receptor" OR "CAR" OR "CAR-"', 
    '"AAV" AND "immunogenicity"',
    '"aging"',
    '"cystic fibrosis" ',
    '"cardiac" AND "gene therapy"',
    '"regulatory t cell" AND "therapy"'
]
    


def search_term_gen_text_check(search_term, text):
    if text is None: #empty text handler
        return 0
    split = re.split('OR | AND', search_term)
    count = 0

    for element in split:
        if element.lower().replace('"', '') in text.lower():
            count += 1

    if count == len(split):
        return 4
    elif count > 0:
        return 2
    else:
        return 0
        


def search_term_text_check(search_term, text):
    if text is None: #empty text handler
        return 0
    
    if "in vivo gene editing" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "in vivo gene editing" in text.lower()
        
        if check1:
            return 4
        else:
            return 0


    if "chimeric antigen receptor" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "chimeric antigen receptor" in text.lower()
        check2 = "CAR" in text
        check3 = "CAR-" in text

        if check1 and check2:
            return 4
        elif check1 and check3:
            return 4
        elif check1:
            return 2
        elif check2 or check3:
            return 2
        else:
            return 0


    if "AAV" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "aav" in text.lower()
        check2 = "immunogenicity" in text.lower()
        
        if check1 and check2:
            return 4
        elif check1 or check1:
            return 2
        else:
            return 0


    if "aging" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "aging" in text.lower()
        
        if check1: 
            return 4
        else:
            return 0


    if "cystic fibrosis" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "cystic fibrosis" in text.lower()
        if check1:
            return 4
        else:
            return 0
    

    if "regulatory t cell" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "regulatory t cell" in text.lower()
        check2 = "therapy" in text.lower()
        
        if check1 and check2:
            return 4
        elif check1 or check1:
            return 2
        else:
            return 0
    

    if "cardiac" in search_term: #Aaahhhhh it hurts it hurts noooo hardcoded values
        check1 = "cardiac" in text.lower()
        check2 = "gene therapy" in text.lower()
        
        if check1 and check2:
            return 4
        elif check1 or check1:
            return 2
        else:
            return 0

def get_relevance_score(title, abstract, search_term):
    relevance_score=0
    highest_possible=4 + 2 + 1
    in_title = search_term_gen_text_check(search_term, title) 
   
    in_abstract = search_term_gen_text_check(search_term, abstract) / 2
    in_text = 1 
  
    relevance_score = in_title + in_abstract + in_text

    normalized_score=round(relevance_score / highest_possible, 2)
    return normalized_score