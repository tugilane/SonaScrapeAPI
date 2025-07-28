import requests
import datetime
import zoneinfo
import bs4
import lxml

def scrape_postimees(sona):

    leht = requests.get('https://err.ee')
    html = leht.text
    soup = bs4.BeautifulSoup(html, 'lxml')

    for artikkel in soup.find_all(class_="article"):
        pealkiri = artikkel.find("h2")
        if pealkiri is not None:
            print(pealkiri.get_text())

    aegEestis = datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Helsinki'))
    print(aegEestis.isoformat())



scrape_postimees('tere')


