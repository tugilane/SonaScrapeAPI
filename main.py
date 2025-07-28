import requests
import datetime
import zoneinfo
import bs4
import lxml
import string

def scrape_err(sona):

    leht = requests.get('https://err.ee')
    html = leht.text
    soup = bs4.BeautifulSoup(html, 'lxml')

    pealkirjaList = []
    sonuKokku = 0
    for artikkel in soup.find_all(class_="article"):
        pealkiri = artikkel.find("h2")

        if pealkiri is not None:
            artikkelTekst = pealkiri.get_text().lower()
            märgitaTekst = artikkelTekst.translate(str.maketrans('', '', string.punctuation))
            sonadeArv = märgitaTekst.split().count(sona.lower())
            if sonadeArv > 0:
                sonuKokku += sonadeArv
                pealkirjaList.append(artikkelTekst)

    aegEestis = datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Helsinki'))

    print(aegEestis.isoformat())
    print(sonuKokku)
    print(pealkirjaList)




scrape_err('trump')


