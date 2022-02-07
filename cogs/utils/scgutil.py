# https://isidore.co/aquinas/ContraGentiles1.htm#13

# imports

import requests
from bs4 import BeautifulSoup

def scg_search_1(p, q):
    url = "SCGfiles/scg" + str(p) + ".html"

    foo = open(url, 'rb')

    soup = BeautifulSoup(foo.read(), 'html.parser')

    result = soup.find('a', {"id": q}).text

    paragraphs = result.split('\n')
    new_paragraphs = []
    for i in paragraphs:
        if len(i) > 5:
            new_paragraphs.append(i)

    for j in range(len(new_paragraphs)):
        print("PARAGRAPH " + str(j))
        print(new_paragraphs[j])

# download the files
url = "https://isidore.co/aquinas/english/ContraGentiles4.htm"
page = requests.get(url)
foo = open('SCGfiles/scg4.html', 'wb')
foo.write(page.content)

# testing
for i in range(84, 94):
    scg_search_1(4, i)
    print('\n\n\n')

