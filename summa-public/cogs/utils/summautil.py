"""
This is literally just copied from my old code. Near useless right now.
"""

import requests
from bs4 import BeautifulSoup

def st_search(p, q, a):
    """
    same as sto_search but without objections.
    """

    new_results = []

    for i in sto_search(p, q, a):
        if "objection" not in i.lower():
            new_results.append(i)
    
    return new_results

def sto_search(p, q, a):
    """
    query is in format [part][question].
    returns paragraphs from the summa.
    """

    query = st_int_to_str(p, q, a)
    results = []

    url = "http://summa-theologiae.org/question/" + query + ".htm"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    x = soup.findAll('td', {"class": "textarea"})
    x = x[0].p.text
    e = x.split('\n\n\n')

    for i in e:
        if i != '' and len(i) > 3:
            t = i.split('\n')
            results.append(' '.join(t))
    
    # add the title
    y = soup.find('font', {"class": "desc"})
    results.insert(0, y.text)

    return results

def st_translation(part, question):
    """
    returns the question for st_search based on the part and question given.
    """

    if part == 6:
        return question + 611
    elif part == 5:
        return question + 512
    elif part == 4:
        return question + 422
    elif part == 3:
        return question + 233
    elif part == 2:
        return question + 119
    else:
        return question

def st_int_to_str(part, question, article):
    """
    takes part, question, and article as ints. returns string query for st_search.
    """

    true_question = str(st_translation(part, question))
    while len(true_question) < 3:
        true_question = "0" + true_question
    
    true_article = str(article)
    while len(true_article) < 2:
        true_article = "0" + true_article
    
    return true_question + true_article


# check if each paragraph has the word "objection" in it
# do not use the paragraph in that case
