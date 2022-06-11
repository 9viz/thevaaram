import bs4
import urllib.request as req
import re
from sys import argv
from shlex import quote as shell_quote

# onnulendu ezhu varaikum panna podhum.

UA = { "User-Agent": "Chrome/96.0.4664.110" }
RE = re.compile(r"[0-9][0-9]?\.[0-9]+")
SADHGURU = re.compile(r"சற்குருநாத ஓதுவார்")

def request(url):
    """Request URL."""
    return req.urlopen(req.Request(url, headers=UA))

def post(id):
    return req.urlopen(
        req.Request(
            "https://shaivam.org/odhuvarajax.php",
            f"id={id}".encode("utf8"),
            headers=UA,
        )).read().decode("utf8")

def padigamgal(url):
    soup = bs4.BeautifulSoup(request(url), "html.parser")
    ret = []
    xs = soup.find("ul", class_="sub-page-list").find_all("li")

    for x in xs:
        if y := re.search(RE, x.a.string):
            ret.append((x.a["href"], x.a.string[y.start():]))

    return ret

def audio(padigam):
    soup = bs4.BeautifulSoup(request(padigam), "html.parser")
    opts = soup.find("select")

    if a := opts.find("option", text=SADHGURU):
        return post(a["value"])
    else:
        return soup.find("audio")["src"]


if __name__ == "__main__":
    for i in argv[1:]:
        for padigam, n in padigamgal(i):
            print("wget {} -O {}.mp3".format(shell_quote(audio(padigam)), shell_quote(n)))
