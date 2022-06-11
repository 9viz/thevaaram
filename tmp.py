import urllib.request as req
import bs4
import re
from sys import argv

def links(url):
    soup = bs4.BeautifulSoup(req.urlopen(url), "html.parser")
    return [ (re.match(r"[0-9.]+", i.text).group(0), i.text)
             for i in soup.find_all("table")[1].find_all("a") ]

    # return [ (re.match(r"[0-9.]+", i.text).group(0), "https://sivasiva.org/" + i["href"])
             # for i in soup.find_all("table")[1].find_all("a") ]

# def text(link):
#     soup = bs4.BeautifulSoup(req.urlopen(link), "html.parser")
#     return soup.find_all("table")[1].text

# def save(links):
#     for name, link in links:
#         with open(f"aaa/{name}", "w") as f:
#             f.write(text(link))

for i in argv[1:]:
    # save(links(i))
    for f, n in links(i):
        print(f"echo \"{n}\" | cat - aaa/{f}.txt | sponge aaa/{f}.txt")
