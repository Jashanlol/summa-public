# http://www.scborromeo.org/ccc/para/2425.htm

# imports
import requests
from bs4 import BeautifulSoup
import bs4

def ccc_get_url(p):
    url = "http://www.scborromeo.org/ccc/para/" + str(p) + ".htm"
    return url


def ccc(p):
    url = ccc_get_url(p)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    result = soup.find('td', {"class": 'text'})
    print(result.text)

    """
    p = result.contents
    for i in range(2, len(p)):
        if isinstance(p[i], bs4.element.NavigableString):
            print(p[i].strip())
        else:
            print("> " + p[i].text.strip())
    """

# testing
